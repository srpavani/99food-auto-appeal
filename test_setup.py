"""
Script de teste para verificar a configuração do sistema.
"""
from config import load_settings
from api_client import APIClient
from llm_client import create_llm_client
from database import OrderDatabase
from detailed_logger import DetailedLogger
import sys


def test_config():
    """Testa se as configurações estão corretas."""
    print("=" * 60)
    print("🧪 TESTE DE CONFIGURAÇÃO")
    print("=" * 60)
    print()
    
    try:
        settings = load_settings()
        print("✅ Configurações carregadas com sucesso!")
        print(f"   - Provedor: {settings.llm_provider}")
        print(f"   - Modelo: {settings.llm_model}")
        print(f"   - API Base: {settings.base_api_url}")
        print()
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar configurações: {e}")
        return False


def test_api_connection():
    """Testa conexão com a API 99Food."""
    print("🌐 Testando conexão com API 99Food...")
    
    try:
        settings = load_settings()
        api_client = APIClient(settings.base_api_url)
        
        # Tenta buscar pedidos
        response = api_client.get_refund_orders(
            start_date=settings.start_date,
            end_date=settings.end_date,
            page_size=1
        )
        
        api_client.close()
        
        if response.get("success"):
            print("✅ API 99Food conectada com sucesso!")
            print()
            return True
        else:
            print("⚠️  API retornou, mas sem sucesso")
            print(f"   Resposta: {response}")
            print()
            return False
            
    except Exception as e:
        print(f"❌ Erro ao conectar com API: {e}")
        print()
        return False


def test_llm_client():
    """Testa criação do cliente LLM."""
    print("🧠 Testando cliente LLM...")
    
    try:
        settings = load_settings()
        llm_client = create_llm_client(settings)
        print(f"✅ Cliente {settings.llm_provider.upper()} criado com sucesso!")
        print()
        return True
    except Exception as e:
        print(f"❌ Erro ao criar cliente LLM: {e}")
        print()
        return False


def test_database():
    """Testa database e logger."""
    print("💾 Testando database e logger...")
    
    try:
        database = OrderDatabase()
        detailed_logger = DetailedLogger()
        
        stats = database.get_stats()
        print(f"   ✓ Database OK - {stats['total_processed']} pedidos processados")
        print(f"   ✓ Logger OK - arquivos em logs/")
        print()
        return True
    except Exception as e:
        print(f"   ✗ Erro: {e}")
        print()
        return False


def main():
    """Executa todos os testes."""
    results = []
    
    results.append(("Configurações", test_config()))
    results.append(("API 99Food", test_api_connection()))
    results.append(("Cliente LLM", test_llm_client()))
    results.append(("Database/Logger", test_database()))
    
    print("=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {test_name}")
    
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print()
        print("🎉 Todos os testes passaram! O sistema está pronto para uso.")
        print("   Execute: python main.py")
        return 0
    else:
        print()
        print("⚠️  Alguns testes falharam. Verifique as configurações no .env")
        return 1


if __name__ == "__main__":
    sys.exit(main())
