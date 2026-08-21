"""
Script para executar o sistema de contestação automática UMA VEZ (sem loop).
Use este script se quiser rodar manualmente ou via cron/task scheduler.
"""
import sys
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


def main():
    """Função principal - executa uma vez e termina."""
    
    print("=" * 60)
    print("🤖 SISTEMA DE CONTESTAÇÃO AUTOMÁTICA - 99FOOD")
    print("=" * 60)
    print()
    
    try:
        # 1. Carrega configurações
        logger.info("📋 Carregando configurações...")
        settings = load_settings()
        
        # Usa data dinâmica (últimos 7 dias)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        print(f"🔧 Configurações:")
        print(f"   - Provedor LLM: {settings.llm_provider.upper()}")
        print(f"   - Modelo: {settings.llm_model}")
        print(f"   - API Base: {settings.base_api_url}")
        print(f"   - Período: {start_date_str} até {end_date_str}")
        print()
        
        # 2. Cria cliente API
        logger.info("🌐 Inicializando cliente API...")
        api_client = APIClient(settings.base_api_url)
        
        # 3. Cria cliente LLM
        logger.info(f"🧠 Inicializando {settings.llm_provider.upper()}...")
        llm_client = create_llm_client(settings)
        
        # 4. Cria database e logger detalhado
        logger.info("💾 Inicializando database...")
        database = OrderDatabase()
        detailed_logger = DetailedLogger()
        
        # Mostra estatísticas do database
        stats = database.get_stats()
        print(f"📊 Estatísticas do Database:")
        print(f"   - Total já processado: {stats['total_processed']}")
        print(f"   - Último processamento: {stats['last_processed']}")
        print()
        
        # 5. Cria e executa o agente
        logger.info("🚀 Iniciando agente de contestação...")
        print()
        
        agent = RefundContestationAgent(
            api_client=api_client,
            llm_client=llm_client,
            database=database,
            detailed_logger=detailed_logger
        )
        
        result = agent.run(
            start_date=start_date_str,
            end_date=end_date_str,
            page_size=settings.page_size
        )
        
        # 6. Exibe resumo final
        print()
        print("=" * 60)
        print("📊 RESUMO DA EXECUÇÃO")
        print("=" * 60)
        print(f"📋 Pedidos encontrados: {len(result['order_ids'])}")
        print(f"✅ Contestações enviadas: {result['appeals_sent']}")
        print(f"⏭️  Pedidos pulados (já contestados): {result['appeals_skipped']}")
        print(f"❌ Erros encontrados: {len(result['errors'])}")
        
        # Estatísticas gerais
        stats = database.get_stats()
        today_count = database.get_processed_count_today()
        print()
        print(f"📊 Estatísticas Gerais:")
        print(f"   - Total processado: {stats['total_processed']}")
        print(f"   - Processado hoje: {today_count}")
        
        if result['errors']:
            print()
            print("⚠️  ERROS:")
            for i, error in enumerate(result['errors'], 1):
                print(f"   {i}. {error}")
        
        print("=" * 60)
        print()
        print("✅ Logs salvos em:")
        print("   - data/processed_orders.json (database)")
        print("   - logs/contestacoes_*.txt (detalhes)")
        print("   - logs/ciclos_*.txt (resumos)")
        print()
        
        # Fecha cliente
        api_client.close()
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n⏸️  Execução interrompida pelo usuário")
        return 1
    
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
