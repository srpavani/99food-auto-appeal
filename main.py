import sys
import time
from datetime import datetime, timedelta
from config import load_settings
from api_client import APIClient
from llm_client import create_llm_client
from agent_graph import RefundContestationAgent
from database import OrderDatabase
from detailed_logger import DetailedLogger
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_date_range(days_back: int = 7) -> tuple:
    """
    Retorna o intervalo de datas para buscar pedidos.
    
    Args:
        days_back: Quantos dias para trás buscar (padrão: 7)
    
    Returns:
        Tupla (start_date, end_date) no formato YYYY-MM-DD
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    return (
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )


def run_cycle(
    agent: RefundContestationAgent,
    detailed_logger: DetailedLogger,
    page_size: int,
    cycle_number: int
) -> dict:
    """
    Executa um ciclo de busca e contestação.
    
    Args:
        agent: Agente de contestação
        detailed_logger: Logger detalhado
        page_size: Tamanho da página
        cycle_number: Número do ciclo
    
    Returns:
        Dict com resultado do ciclo
    """
    # Usa data dinâmica (últimos 7 dias)
    start_date, end_date = get_date_range(days_back=1)
    
    logger.info(f"📅 Período: {start_date} até {end_date}")
    
    result = agent.run(
        start_date=start_date,
        end_date=end_date,
        page_size=page_size
    )
    
    # Salva resumo do ciclo
    detailed_logger.log_cycle_summary(
        cycle_number=cycle_number,
        orders_found=len(result['order_ids']),
        orders_processed=result['appeals_sent'],
        orders_skipped=result['appeals_skipped'],
        errors=len(result['errors'])
    )
    
    return result


def main():
    """Função principal com loop contínuo."""
    
    print("=" * 70)
    print("SISTEMA DE CONTESTAÇÃO AUTOMÁTICA")
    print("=" * 70)
    print()
    
    try:
        logger.info("📋 Carregando configurações...")
        settings = load_settings()
        
        print(f"🔧 Configurações:")
        print(f"   - Provedor LLM: {settings.llm_provider.upper()}")
        print(f"   - Modelo: {settings.llm_model}")
        print(f"   - API Base: {settings.base_api_url}")
        print(f"   - Intervalo: A cada 15 minutos")
        print(f"   - Busca: Últimos 7 dias (dinâmico)")
        print()
        
        logger.info("🌐 Inicializando cliente API...")
        api_client = APIClient(settings.base_api_url)
        
        logger.info(f"🧠 Inicializando {settings.llm_provider.upper()}...")
        llm_client = create_llm_client(settings)
        
        logger.info("💾 Inicializando database...")
        database = OrderDatabase()
        detailed_logger = DetailedLogger()
        
        stats = database.get_stats()
        print(f" Estatísticas do Database:")
        print(f"   - Total processado: {stats['total_processed']}")
        print(f"   - Sucessos: {stats['successful']}")
        print(f"   - Falhas: {stats['failed']}")
        print(f"   - Último processamento: {stats['last_processed']}")
        print()
        
        # cria o agente
        agent = RefundContestationAgent(
            api_client=api_client,
            llm_client=llm_client,
            database=database,
            detailed_logger=detailed_logger
        )
        
        # loop infinito
        print("=" * 70)
        print("🔄 MODO CONTÍNUO ATIVADO")
        print("=" * 70)
        print("O sistema irá buscar pedidos a cada 15 minutos.")
        print("Pressione Ctrl+C para parar.")
        print()
        
        cycle_number = 0
        
        while True:
            cycle_number += 1
            
            print()
            print("=" * 70)
            print(f"🔄 CICLO #{cycle_number} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print("=" * 70)
            print()
            
            try:
                result = run_cycle(
                    agent=agent,
                    detailed_logger=detailed_logger,
                    page_size=settings.page_size,
                    cycle_number=cycle_number
                )
                
                print()
                print("─" * 70)
                print(f"📊 RESUMO DO CICLO #{cycle_number}")
                print("─" * 70)
                print(f"📋 Pedidos encontrados: {len(result['order_ids'])}")
                print(f"✅ Contestações enviadas: {result['appeals_sent']}")
                print(f"⏭️  Pedidos pulados (já contestados): {result['appeals_skipped']}")
                print(f"❌ Erros: {len(result['errors'])}")
                
                stats = database.get_stats()
                today_count = database.get_processed_count_today()
                print()
                print(f"📊 Estatísticas Gerais:")
                print(f"   - Total processado: {stats['total_processed']}")
                print(f"   - Processado hoje: {today_count}")
                print("─" * 70)
                
                if result['errors']:
                    print()
                    print("⚠️  Erros neste ciclo:")
                    for i, error in enumerate(result['errors'], 1):
                        print(f"   {i}. {error}")
                
            except Exception as e:
                logger.error(f"❌ Erro no ciclo #{cycle_number}: {e}", exc_info=True)
            
            wait_seconds = 900
            next_run = datetime.now() + timedelta(seconds=wait_seconds)
            
            print()
            print(f"⏰ Próxima execução em 15 minutos ({next_run.strftime('%H:%M:%S')})")
            print(f"   Pressione Ctrl+C para parar.")
            print()
            
            time.sleep(wait_seconds)
        
    except KeyboardInterrupt:
        print()
        print()
        print("=" * 70)
        logger.info("⏸️  Sistema interrompido pelo usuário")
        print("=" * 70)
        
        stats = database.get_stats()
        print()
        print("📊 ESTATÍSTICAS FINAIS:")
        print(f"   - Total processado: {stats['total_processed']}")
        print(f"   - Sucessos: {stats['successful']}")
        print(f"   - Falhas: {stats['failed']}")
        print(f"   - Último processamento: {stats['last_processed']}")
        print()
        print("✅ Todos os dados foram salvos em:")
        print("   - data/processed_orders.json")
        print("   - logs/contestacoes_*.txt")
        print("   - logs/ciclos_*.txt")
        print()
        
        api_client.close()
        return 0
    
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}", exc_info=True)
        api_client.close()
        return 1


if __name__ == "__main__":
    sys.exit(main())
