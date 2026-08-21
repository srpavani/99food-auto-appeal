"""
Logger detalhado que salva informações completas de cada contestação.
"""
import os
from datetime import datetime
from typing import Optional


class DetailedLogger:
    """Logger que salva detalhes completos de cada contestação."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
    
    def log_contestation(
        self,
        order_id: str,
        apply_id: str,
        reason: str,
        items: str,
        image_url: Optional[str],
        prompt_sent: str,
        ai_response: str,
        success: bool,
        error: Optional[str] = None
    ):
        """
        Salva detalhes completos de uma contestação.
        
        Args:
            order_id: ID do pedido
            apply_id: ID da solicitação
            reason: Motivo da reclamação
            items: Itens do pedido
            image_url: URL da imagem (se houver)
            prompt_sent: Prompt enviado para IA
            ai_response: Resposta da IA
            success: Se foi enviado com sucesso
            error: Mensagem de erro (se houver)
        """
        timestamp = datetime.now()
        filename = f"contestacoes_{timestamp.strftime('%Y-%m-%d')}.txt"
        filepath = os.path.join(self.log_dir, filename)
        
        separator = "=" * 80
        
        log_entry = f"""
{separator}
CONTESTAÇÃO REGISTRADA
{separator}
Data/Hora: {timestamp.strftime('%d/%m/%Y %H:%M:%S')}
Pedido ID: {order_id}
Apply ID: {apply_id}

{'-' * 80}
DADOS DO PEDIDO
{'-' * 80}
Motivo da Reclamação: {reason}
Itens do Pedido: {items}
Imagem de Prova: {'SIM - ' + image_url if image_url else 'NÃO'}

{'-' * 80}
PROMPT ENVIADO PARA IA
{'-' * 80}
{prompt_sent}

{'-' * 80}
RESPOSTA DA IA
{'-' * 80}
{ai_response}

{'-' * 80}
RESULTADO
{'-' * 80}
Status: {'✅ ENVIADO COM SUCESSO' if success else '❌ FALHA NO ENVIO'}
"""
        
        if error:
            log_entry += f"Erro: {error}\n"
        
        log_entry += f"\n{separator}\n\n"
        
        # Salva no arquivo
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"⚠️ Erro ao salvar log detalhado: {e}")
    
    def log_cycle_summary(
        self,
        cycle_number: int,
        orders_found: int,
        orders_processed: int,
        orders_skipped: int,
        errors: int
    ):
        """
        Salva resumo de um ciclo de execução.
        
        Args:
            cycle_number: Número do ciclo
            orders_found: Pedidos encontrados
            orders_processed: Pedidos processados neste ciclo
            orders_skipped: Pedidos pulados (já processados)
            errors: Quantidade de erros
        """
        timestamp = datetime.now()
        filename = f"ciclos_{timestamp.strftime('%Y-%m-%d')}.txt"
        filepath = os.path.join(self.log_dir, filename)
        
        log_entry = f"""
{'=' * 60}
CICLO #{cycle_number} - {timestamp.strftime('%d/%m/%Y %H:%M:%S')}
{'=' * 60}
📊 Pedidos encontrados: {orders_found}
✅ Processados neste ciclo: {orders_processed}
⏭️  Pulados (já contestados): {orders_skipped}
❌ Erros: {errors}
{'=' * 60}

"""
        
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"⚠️ Erro ao salvar resumo de ciclo: {e}")
