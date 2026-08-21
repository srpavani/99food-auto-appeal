"""
Definição do grafo LangGraph para orquestração do fluxo de contestação.
"""
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from api_client import APIClient
from llm_client import LLMClient
from database import OrderDatabase
from detailed_logger import DetailedLogger
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """Estado do agente durante a execução."""
    start_date: str
    end_date: str
    page_size: int
    order_ids: List[str]
    current_order_index: int
    current_order_id: Optional[str]
    current_apply_id: Optional[str]
    current_reason: Optional[str]
    current_items: Optional[str]
    current_image_url: Optional[str]
    current_prompt: Optional[str]
    generated_defense: Optional[str]
    appeals_sent: int
    appeals_skipped: int
    errors: List[str]


class RefundContestationAgent:
    """Agente de contestação de reembolsos usando LangGraph."""
    
    def __init__(
        self, 
        api_client: APIClient, 
        llm_client: LLMClient,
        database: OrderDatabase,
        detailed_logger: DetailedLogger
    ):
        self.api_client = api_client
        self.llm_client = llm_client
        self.database = database
        self.detailed_logger = detailed_logger
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Constrói o grafo de execução."""
        
        workflow = StateGraph(AgentState)
        
        # Adiciona os nós
        workflow.add_node("fetch_refund_orders", self.fetch_refund_orders)
        workflow.add_node("get_order_details", self.get_order_details)
        workflow.add_node("generate_defense", self.generate_defense)
        workflow.add_node("submit_appeal", self.submit_appeal)
        
        # Define o fluxo
        workflow.set_entry_point("fetch_refund_orders")
        
        workflow.add_edge("fetch_refund_orders", "get_order_details")
        workflow.add_conditional_edges(
            "get_order_details",
            self.should_generate_defense,
            {
                "generate": "generate_defense",
                "next_order": "get_order_details",
                "end": END
            }
        )
        workflow.add_edge("generate_defense", "submit_appeal")
        workflow.add_conditional_edges(
            "submit_appeal",
            self.should_continue,
            {
                "continue": "get_order_details",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def fetch_refund_orders(self, state: AgentState) -> AgentState:
        """Nó 1: Busca pedidos com reembolso pendente."""
        logger.info("🔍 Buscando pedidos com reembolso...")
        
        try:
            response = self.api_client.get_refund_orders(
                start_date=state["start_date"],
                end_date=state["end_date"],
                page_size=state["page_size"]
            )
            
            # Extrai os orderIds
            order_list = response.get("data", {}).get("data", {}).get("orderList", [])
            order_ids = [order["orderId"] for order in order_list if "orderId" in order]
            
            logger.info(f"✅ Encontrados {len(order_ids)} pedidos com reembolso")
            
            state["order_ids"] = order_ids
            state["current_order_index"] = 0
            state["appeals_sent"] = 0
            state["appeals_skipped"] = 0
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar pedidos: {e}")
            state["errors"].append(f"fetch_refund_orders: {str(e)}")
            state["order_ids"] = []
        
        return state
    
    def get_order_details(self, state: AgentState) -> AgentState:
        """Nó 2: Busca detalhes de um pedido específico."""
        
        if state["current_order_index"] >= len(state["order_ids"]):
            logger.info("✅ Todos os pedidos foram processados")
            return state
        
        order_id = state["order_ids"][state["current_order_index"]]
        state["current_order_id"] = order_id
        
        logger.info(f"📄 Buscando detalhes do pedido {order_id}...")
        
        try:
            response = self.api_client.get_order_detail(order_id)
            data = response.get("data", {}).get("data", {})
            
            refund_list = data.get("refundDetailList", [])
            
            if not refund_list:
                logger.warning(f"⚠️  Pedido {order_id} sem detalhes de reembolso")
                state["current_order_index"] += 1
                return state
            
            # Pega o primeiro reembolso
            refund = refund_list[0]
            
            # Extrai informações críticas
            state["current_apply_id"] = str(refund.get("applyId", ""))
            
            reason_info = refund.get("applyReasonInfo", {})
            state["current_reason"] = reason_info.get("reasonTag", "")
            
            # Extrai imagem se houver
            images = reason_info.get("img", [])
            state["current_image_url"] = images[0] if images else None
            
            # Extrai itens do pedido
            items = data.get("items", [])
            items_text = ", ".join([f"{item.get('name')} x{item.get('count')}" for item in items])
            state["current_items"] = items_text
            
            # Verifica se já foi processado antes
            if self.database.is_processed(order_id, state["current_apply_id"]):
                logger.info(f"⏭️  Pedido {order_id} já foi contestado anteriormente, pulando...")
                state["appeals_skipped"] += 1
                state["current_order_index"] += 1
                # Limpa estado atual para não processar
                state["current_apply_id"] = None
                state["current_reason"] = None
                return state
            
            logger.info(f"📋 Motivo: {state['current_reason']}")
            logger.info(f"🖼️  Imagem: {'SIM' if state['current_image_url'] else 'NÃO'}")
            if state['current_image_url']:
                logger.info(f"   URL: {state['current_image_url']}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar detalhes do pedido {order_id}: {e}")
            state["errors"].append(f"get_order_details ({order_id}): {str(e)}")
            state["current_order_index"] += 1
        
        return state
    
    def generate_defense(self, state: AgentState) -> AgentState:
        """Nó 3: Gera texto de defesa usando IA (multimodal)."""
        logger.info("🤖 Gerando defesa com IA...")
        
        try:
            # Monta o prompt completo para salvar no log
            prompt_parts = [
                f"Motivo da reclamação: {state['current_reason']}",
                f"Itens do pedido: {state['current_items']}"
            ]
            if state['current_image_url']:
                prompt_parts.append(f"Imagem: {state['current_image_url']}")
            
            state["current_prompt"] = "\n".join(prompt_parts)
            
            defense = self.llm_client.generate_defense(
                reason=state["current_reason"],
                items=state["current_items"],
                image_url=state["current_image_url"]
            )
            
            # Garante que não passe de 200 caracteres
            if len(defense) > 200:
                defense = defense[:197] + "..."
            
            state["generated_defense"] = defense
            logger.info(f"💬 Defesa gerada: {defense}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar defesa: {e}")
            state["errors"].append(f"generate_defense: {str(e)}")
            state["generated_defense"] = None
            state["current_prompt"] = None
        
        return state
    
    def submit_appeal(self, state: AgentState) -> AgentState:
        """Nó 4: Envia a contestação via API."""
        
        if not state["generated_defense"]:
            logger.warning("⚠️  Sem defesa gerada, pulando envio")
            state["current_order_index"] += 1
            return state
        
        logger.info("📤 Enviando contestação...")
        
        success = False
        error_msg = None
        
        try:
            response = self.api_client.submit_appeal(
                order_id=state["current_order_id"],
                apply_id=state["current_apply_id"],
                comments=state["generated_defense"]
            )
            
            if response.get("success"):
                logger.info(f"✅ Contestação enviada com sucesso para pedido {state['current_order_id']}")
                state["appeals_sent"] += 1
                success = True
            else:
                error_msg = str(response)
                logger.error(f"❌ Falha ao enviar contestação: {response}")
                state["errors"].append(f"submit_appeal ({state['current_order_id']}): {response}")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Erro ao enviar contestação: {e}")
            state["errors"].append(f"submit_appeal ({state['current_order_id']}): {str(e)}")
        
        # Salva no database (mesmo se falhou, para não tentar de novo)
        self.database.mark_as_processed(
            order_id=state["current_order_id"],
            apply_id=state["current_apply_id"],
            reason=state["current_reason"],
            defense=state["generated_defense"],
            success=success
        )
        
        # Salva log detalhado
        self.detailed_logger.log_contestation(
            order_id=state["current_order_id"],
            apply_id=state["current_apply_id"],
            reason=state["current_reason"],
            items=state["current_items"],
            image_url=state["current_image_url"],
            prompt_sent=state["current_prompt"],
            ai_response=state["generated_defense"],
            success=success,
            error=error_msg
        )
        
        state["current_order_index"] += 1
        return state
    
    def should_generate_defense(self, state: AgentState) -> str:
        """Decisão condicional após buscar detalhes."""
        
        # Se não há mais pedidos, termina
        if state["current_order_index"] >= len(state["order_ids"]):
            return "end"
        
        # Se não tem apply_id ou reason, pula para o próximo
        if not state.get("current_apply_id") or not state.get("current_reason"):
            return "next_order"
        
        # Caso contrário, gera defesa
        return "generate"
    
    def should_continue(self, state: AgentState) -> str:
        """Decisão condicional após enviar contestação."""
        
        # Se ainda há pedidos, continua
        if state["current_order_index"] < len(state["order_ids"]):
            return "continue"
        
        # Caso contrário, termina
        return "end"
    
    def run(self, start_date: str, end_date: str, page_size: int = 20) -> Dict[str, Any]:
        """Executa o grafo completo."""
        
        initial_state: AgentState = {
            "start_date": start_date,
            "end_date": end_date,
            "page_size": page_size,
            "order_ids": [],
            "current_order_index": 0,
            "current_order_id": None,
            "current_apply_id": None,
            "current_reason": None,
            "current_items": None,
            "current_image_url": None,
            "current_prompt": None,
            "generated_defense": None,
            "appeals_sent": 0,
            "appeals_skipped": 0,
            "errors": []
        }
        
        logger.info("🚀 Iniciando agente de contestação...")
        final_state = self.graph.invoke(initial_state)
        logger.info(f"🏁 Processamento concluído!")
        logger.info(f"📊 Contestações enviadas: {final_state['appeals_sent']}")
        logger.info(f"⏭️  Pedidos pulados (já contestados): {final_state['appeals_skipped']}")
        
        if final_state["errors"]:
            logger.warning(f"⚠️  Erros encontrados: {len(final_state['errors'])}")
            for error in final_state["errors"]:
                logger.error(f"   - {error}")
        
        return final_state
