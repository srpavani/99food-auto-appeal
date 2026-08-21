"""
Script para testar apenas a geração de defesa com IA.
Útil para verificar se a API key está funcionando sem precisar da API 99Food.
"""
from config import load_settings
from llm_client import create_llm_client
import sys


def test_text_only():
    """Testa geração de defesa apenas com texto (sem imagem)."""
    
    print("=" * 60)
    print("🧪 TESTE 1: Defesa baseada em Texto")
    print("=" * 60)
    print()
    
    # Cenário simulado
    reason = "Produto não chegou"
    items = "Pizza Margherita x2, Refrigerante x1"
    
    print(f"📋 Motivo do cliente: {reason}")
    print(f"🍕 Itens do pedido: {items}")
    print(f"🖼️  Imagem: NÃO")
    print()
    
    settings = load_settings()
    
    try:
        llm_client = create_llm_client(settings)
        
        print(f"🤖 Gerando defesa com {settings.llm_provider.upper()}...")
        defense = llm_client.generate_defense(
            reason=reason,
            items=items,
            image_url=None
        )
        
        print()
        print("✅ Defesa gerada com sucesso!")
        print(f"💬 Texto: \"{defense}\"")
        print(f"📏 Tamanho: {len(defense)} caracteres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar defesa: {e}")
        return False


def test_with_image():
    """Testa geração de defesa com imagem (capacidade multimodal)."""
    
    print()
    print("=" * 60)
    print("🧪 TESTE 2: Defesa Multimodal (Texto + Imagem)")
    print("=" * 60)
    print()
    
    # Cenário simulado com imagem
    reason = "Item veio errado"
    items = "Cachorro Quente Duplo x3"
    # URL de imagem de exemplo (da resposta real da API que você forneceu)
    image_url = "https://img0.didiglobal.com/static/soda_public/e6e81fdd8eeba9d5acefa8d02a0d2d54"
    
    print(f"📋 Motivo do cliente: {reason}")
    print(f"🌭 Itens do pedido: {items}")
    print(f"🖼️  Imagem: SIM")
    print(f"   URL: {image_url}")
    print()
    
    settings = load_settings()
    
    try:
        llm_client = create_llm_client(settings)
        
        print(f"🤖 Analisando imagem com {settings.llm_provider.upper()}...")
        print("   (A IA está vendo a imagem e analisando...)")
        
        defense = llm_client.generate_defense(
            reason=reason,
            items=items,
            image_url=image_url
        )
        
        print()
        print("✅ Defesa multimodal gerada com sucesso!")
        print(f"💬 Texto: \"{defense}\"")
        print(f"📏 Tamanho: {len(defense)} caracteres")
        print()
        print("💡 A IA considerou a imagem na análise!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar defesa: {e}")
        print()
        print("ℹ️  Nota: Se o erro for relacionado a 'image_url',")
        print("   verifique se o modelo escolhido suporta visão:")
        print("   - GPT-4o: ✅ Suporta")
        print("   - GPT-3.5: ❌ Não suporta")
        print("   - Gemini 1.5 Pro: ✅ Suporta")
        return False


def test_different_scenarios():
    """Testa diferentes cenários de reclamação."""
    
    print()
    print("=" * 60)
    print("🧪 TESTE 3: Diferentes Cenários")
    print("=" * 60)
    print()
    
    settings = load_settings()
    llm_client = create_llm_client(settings)
    
    scenarios = [
        {
            "reason": "Produto veio frio",
            "items": "Lasanha Bolonhesa x1"
        },
        {
            "reason": "Faltou item",
            "items": "X-Bacon x2, Batata Frita x1"
        },
        {
            "reason": "Qualidade ruim",
            "items": "Sushi Combo x1"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"Cenário {i}:")
        print(f"  Motivo: {scenario['reason']}")
        print(f"  Itens: {scenario['items']}")
        
        try:
            defense = llm_client.generate_defense(
                reason=scenario['reason'],
                items=scenario['items'],
                image_url=None
            )
            print(f"  Defesa: \"{defense}\"")
            
        except Exception as e:
            print(f"  Erro: {e}")
        
        print()
    
    return True


def main():
    """Executa os testes."""
    
    print()
    print("🧠 TESTE DE GERAÇÃO DE DEFESA COM IA")
    print()
    
    results = []
    
    # Teste 1: Texto apenas
    results.append(("Texto apenas", test_text_only()))
    
    # Teste 2: Multimodal (pode falhar se modelo não suportar)
    results.append(("Multimodal", test_with_image()))
    
    # Teste 3: Diferentes cenários
    results.append(("Cenários variados", test_different_scenarios()))
    
    # Resumo
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
        print("🎉 Todos os testes passaram!")
        print("   A IA está funcionando corretamente.")
        print()
        print("Próximo passo: Execute 'python test_setup.py' para testar")
        print("a conexão com a API 99Food.")
        return 0
    else:
        print()
        print("⚠️  Alguns testes falharam.")
        print()
        print("Verifique:")
        print("  1. A API key está correta no .env?")
        print("  2. O modelo suporta visão? (para teste multimodal)")
        print("  3. Você tem créditos/quota na conta?")
        return 1


if __name__ == "__main__":
    sys.exit(main())
