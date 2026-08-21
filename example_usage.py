"""
Exemplo de uso programático do sistema de contestação.

Este arquivo mostra como usar o sistema em seus próprios scripts.
"""
from config import load_settings
from api_client import APIClient
from llm_client import create_llm_client
from agent_graph import RefundContestationAgent


def exemplo_basico():
    """Exemplo básico: Processar todos os reembolsos."""
    
    print("=== EXEMPLO 1: Uso Básico ===\n")
    
    # Carregar configurações
    settings = load_settings()
    
    # Criar clientes
    api_client = APIClient(settings.base_api_url)
    llm_client = create_llm_client(settings)
    
    # Criar e executar agente
    agent = RefundContestationAgent(api_client, llm_client)
    
    result = agent.run(
        start_date="2026-01-10",
        end_date="2026-01-28",
        page_size=20
    )
    
    print(f"\n✅ Processados: {len(result['order_ids'])} pedidos")
    print(f"📤 Enviados: {result['appeals_sent']} contestações")
    
    api_client.close()


def exemplo_manual():
    """Exemplo manual: Processar pedido específico."""
    
    print("\n=== EXEMPLO 2: Processar Pedido Específico ===\n")
    
    settings = load_settings()
    
    # Criar clientes
    api_client = APIClient(settings.base_api_url)
    llm_client = create_llm_client(settings)
    
    # ID do pedido que você quer contestar
    order_id = "5764655711753670171"
    
    print(f"📄 Buscando detalhes do pedido {order_id}...")
    
    # 1. Buscar detalhes
    details = api_client.get_order_detail(order_id)
    data = details.get("data", {}).get("data", {})
    
    refund_list = data.get("refundDetailList", [])
    
    if not refund_list:
        print("❌ Pedido não tem reembolso pendente")
        return
    
    # 2. Extrair informações
    refund = refund_list[0]
    apply_id = str(refund.get("applyId", ""))
    reason_info = refund.get("applyReasonInfo", {})
    reason = reason_info.get("reasonTag", "")
    images = reason_info.get("img", [])
    image_url = images[0] if images else None
    
    items = data.get("items", [])
    items_text = ", ".join([f"{item.get('name')} x{item.get('count')}" for item in items])
    
    print(f"📋 Motivo: {reason}")
    print(f"🖼️  Imagem: {'SIM' if image_url else 'NÃO'}")
    
    # 3. Gerar defesa com IA
    print("\n🤖 Gerando defesa...")
    defense = llm_client.generate_defense(
        reason=reason,
        items=items_text,
        image_url=image_url
    )
    
    print(f"💬 Defesa: {defense}")
    
    # 4. Enviar contestação
    print("\n📤 Enviando contestação...")
    response = api_client.submit_appeal(
        order_id=order_id,
        apply_id=apply_id,
        comments=defense
    )
    
    if response.get("success"):
        print("✅ Contestação enviada com sucesso!")
    else:
        print(f"❌ Erro: {response}")
    
    api_client.close()


def exemplo_custom_prompt():
    """Exemplo: Usar prompt customizado para a IA."""
    
    print("\n=== EXEMPLO 3: Defesa Customizada ===\n")
    
    settings = load_settings()
    
    # Criar cliente LLM
    llm_client = create_llm_client(settings)
    
    # Simular dados de um pedido
    reason = "Produto veio errado"
    items = "Pizza Calabresa x1"
    image_url = None  # Sem imagem neste exemplo
    
    print(f"📋 Motivo do cliente: {reason}")
    print(f"🍕 Itens: {items}")
    
    # Gerar defesa
    defense = llm_client.generate_defense(
        reason=reason,
        items=items,
        image_url=image_url
    )
    
    print(f"\n💬 Defesa gerada pela IA:")
    print(f"   \"{defense}\"")
    print(f"\n📏 Tamanho: {len(defense)} caracteres")


def exemplo_listar_pedidos():
    """Exemplo: Apenas listar pedidos sem processar."""
    
    print("\n=== EXEMPLO 4: Listar Pedidos ===\n")
    
    settings = load_settings()
    api_client = APIClient(settings.base_api_url)
    
    # Buscar pedidos
    response = api_client.get_refund_orders(
        start_date="2026-01-10",
        end_date="2026-01-28",
        page_size=20
    )
    
    order_list = response.get("data", {}).get("data", {}).get("orderList", [])
    
    print(f"📋 Encontrados {len(order_list)} pedidos com reembolso:\n")
    
    for i, order in enumerate(order_list, 1):
        order_id = order.get("orderId")
        order_index = order.get("orderIndex", {}).get("displayText", "N/A")
        receiver = order.get("receiverInfo", {}).get("name", "N/A")
        
        refund_info = order.get("refundInfo", {})
        status = refund_info.get("status", "N/A")
        tags = refund_info.get("tagList", [])
        tag_text = tags[0].get("text") if tags else "Sem tag"
        
        print(f"{i}. Pedido {order_index}")
        print(f"   ID: {order_id}")
        print(f"   Cliente: {receiver}")
        print(f"   Status: {status} - {tag_text}")
        print()
    
    api_client.close()


if __name__ == "__main__":
    # Descomente o exemplo que deseja executar:
    
    # exemplo_basico()
    # exemplo_manual()
    exemplo_custom_prompt()
    # exemplo_listar_pedidos()
