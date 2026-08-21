"""
Script de teste para validar a integração com DeepSeek.
"""
from config import load_settings
from llm_client import create_llm_client

def test_deepseek_text_only():
    """Testa DeepSeek apenas com texto (sem imagem)."""
    print("🧪 Testando DeepSeek - Análise de Texto")
    print("=" * 60)
    
    settings = load_settings()
    
    if settings.llm_provider.lower() != "deepseek":
        print("❌ Erro: Configure LLM_PROVIDER=deepseek no arquivo .env")
        return
    
    if not settings.deepseek_api_key:
        print("❌ Erro: DEEPSEEK_API_KEY não configurada no .env")
        return
    
    print(f"✅ Provider: {settings.llm_provider}")
    print(f"✅ Model: {settings.llm_model}")
    print()
    
    # Cria o cliente
    try:
        llm_client = create_llm_client(settings)
        print("✅ Cliente DeepSeek criado com sucesso!")
        print()
    except Exception as e:
        print(f"❌ Erro ao criar cliente: {e}")
        return
    
    # Teste 1: Produto faltando
    print("📝 Teste 1: Cliente alega produto faltando")
    print("-" * 60)
    try:
        defense = llm_client.generate_defense(
            reason="Veio faltando 1 refrigerante",
            items="X-Bacon x1, Batata Frita x1, Coca-Cola 2L x2"
        )
        print(f"🤖 Defesa gerada: {defense}")
        print(f"📏 Tamanho: {len(defense)} caracteres")
        print()
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # Teste 2: Produto errado
    print("📝 Teste 2: Cliente alega produto errado")
    print("-" * 60)
    try:
        defense = llm_client.generate_defense(
            reason="Pedi X-Salada mas veio X-Bacon",
            items="X-Bacon x1, Batata Frita x1"
        )
        print(f"🤖 Defesa gerada: {defense}")
        print(f"📏 Tamanho: {len(defense)} caracteres")
        print()
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    print("=" * 60)
    print("✅ Todos os testes passaram com sucesso!")


def test_deepseek_with_image():
    """Testa DeepSeek com análise de imagem."""
    print("🧪 Testando DeepSeek - Análise de Imagem")
    print("=" * 60)
    
    settings = load_settings()
    
    if settings.llm_provider.lower() != "deepseek":
        print("❌ Erro: Configure LLM_PROVIDER=deepseek no arquivo .env")
        return
    
    if not settings.deepseek_api_key:
        print("❌ Erro: DEEPSEEK_API_KEY não configurada no .env")
        return
    
    print(f"✅ Provider: {settings.llm_provider}")
    print(f"✅ Model: {settings.llm_model}")
    print()
    
    # Cria o cliente
    try:
        llm_client = create_llm_client(settings)
        print("✅ Cliente DeepSeek criado com sucesso!")
        print()
    except Exception as e:
        print(f"❌ Erro ao criar cliente: {e}")
        return
    
    # Teste com imagem de exemplo
    print("📝 Teste: Cliente alega hambúrguer queimado com foto")
    print("-" * 60)
    
    # URL de exemplo de uma imagem de hambúrguer (use uma real para testar)
    test_image_url = "https://example.com/burger.jpg"
    
    print(f"🖼️  URL da imagem: {test_image_url}")
    print()
    
    try:
        defense = llm_client.generate_defense(
            reason="Hambúrguer veio queimado",
            items="X-Bacon x1, Batata Frita x1",
            image_url=test_image_url
        )
        print(f"🤖 Defesa gerada: {defense}")
        print(f"📏 Tamanho: {len(defense)} caracteres")
        print()
    except Exception as e:
        print(f"❌ Erro: {e}")
        print()
        print("💡 Dica: Se o erro for de URL inválida, substitua 'test_image_url'")
        print("   no código por uma URL real de imagem para testar.")
        return
    
    print("=" * 60)
    print("✅ Teste com imagem passou com sucesso!")


if __name__ == "__main__":
    print()
    print("🚀 Iniciando testes do DeepSeek")
    print()
    
    # Executa testes
    test_deepseek_text_only()
    print()
    print()
    
    # Pergunta se quer testar com imagem
    print("⚠️  O teste com imagem requer uma URL válida.")
    resposta = input("Deseja executar teste com análise de imagem? (s/n): ")
    
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        print()
        test_deepseek_with_image()
    else:
        print()
        print("⏭️  Teste com imagem pulado.")
    
    print()
    print("🏁 Testes finalizados!")
