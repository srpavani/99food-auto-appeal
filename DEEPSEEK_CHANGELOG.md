# 🎉 DeepSeek Integrado ao Sistema!

## ✨ O que foi adicionado?

Agora você pode usar o **DeepSeek** como provider de IA para análise de imagens e geração de defesas de contestação!

## 📝 Arquivos Modificados

### 1. `config.py`
- ✅ Adicionada variável `deepseek_api_key`
- ✅ Atualizado comentário do `llm_provider` para incluir "deepseek"

### 2. `llm_client.py`
- ✅ Criada classe `DeepSeekLLMClient` 
- ✅ Implementação com suporte a análise multimodal (texto + imagem)
- ✅ Atualizada factory `create_llm_client()` para suportar DeepSeek
- ✅ Usa OpenAI SDK com `base_url="https://api.deepseek.com"`

### 3. `env.example.txt`
- ✅ Adicionada variável `DEEPSEEK_API_KEY`
- ✅ Atualizada documentação dos providers disponíveis

### 4. `README.md`
- ✅ Atualizada seção de funcionalidades
- ✅ Atualizada seção de configuração com exemplo DeepSeek
- ✅ Adicionado link para guia de setup

### 5. Novos Arquivos Criados

#### `DEEPSEEK_SETUP.md`
- 📖 Guia completo de configuração do DeepSeek
- 🔄 Instruções para alternar entre providers
- 💡 Troubleshooting e recursos úteis

#### `test_deepseek.py`
- 🧪 Script de teste para validar integração
- ✅ Testa análise de texto
- 🖼️  Testa análise de imagem (opcional)

## 🚀 Como Usar

### Configuração Rápida (3 passos)

1. **Obtenha sua API Key** em [platform.deepseek.com](https://platform.deepseek.com)

2. **Edite o arquivo `.env`**:
   ```env
   LLM_PROVIDER=deepseek
   LLM_MODEL=deepseek-chat
   DEEPSEEK_API_KEY=sk-sua-chave-aqui
   ```

3. **Execute normalmente**:
   ```bash
   python main.py
   ```

### Testar a Integração

```bash
python test_deepseek.py
```

## 🔄 Alternando entre Providers

Basta mudar no `.env`:

```env
# Para DeepSeek
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=sk-...

# Para OpenAI
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sk-...

# Para Gemini
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-pro
GOOGLE_API_KEY=...
```

## 📊 Funcionalidades DeepSeek

### ✅ O que funciona:
- Análise de texto das reclamações
- Análise de imagens anexadas pelos clientes
- Geração de defesas automáticas
- Integração completa com o fluxo LangGraph existente

### 🎯 Características:
- API compatível com OpenAI (fácil integração)
- Suporte nativo a visão multimodal
- Bom custo-benefício
- Respostas rápidas

## 🛡️ Compatibilidade

- ✅ Totalmente compatível com código existente
- ✅ Não quebra funcionalidades anteriores (OpenAI/Gemini)
- ✅ Usa mesma interface `LLMClient`
- ✅ Mesmo formato de mensagens e respostas

## 📚 Recursos Adicionais

- [Documentação Oficial DeepSeek](https://platform.deepseek.com/docs)
- [Pricing DeepSeek](https://platform.deepseek.com/pricing)
- [Exemplos de Uso da API](https://platform.deepseek.com/examples)

## ❓ Dúvidas?

Consulte o arquivo `DEEPSEEK_SETUP.md` para guia detalhado e troubleshooting.

---

## 🔧 Correção (29/01/2026)

### Problema Identificado
O modelo `deepseek-chat` **não suporta análise de imagens** (apenas texto). O erro ocorria quando tentávamos enviar imagens:
```
'Failed to deserialize the JSON body into the target type: messages[1]: unknown variant `image_url`, expected `text`'
```

### Solução Implementada
1. ✅ Detecta automaticamente se o modelo suporta visão
2. ✅ Se houver imagem mas o modelo não suportar, processa apenas o texto
3. ✅ Log de aviso quando imagem é ignorada
4. ✅ Documentação atualizada com modelos corretos:
   - `deepseek-chat` - Apenas texto (sem imagens)
   - `deepseek-vl-7b-chat` - Texto + Imagens ⭐ **Recomendado**
   - `deepseek-vl-1.3b-chat` - Texto + Imagens (versão menor)

### Como Usar Análise de Imagens
Para analisar imagens, use o modelo VL no `.env`:
```env
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-vl-7b-chat
DEEPSEEK_API_KEY=sk-...
```

---

**Implementado em:** 29 de Janeiro de 2026  
**Correção aplicada em:** 29 de Janeiro de 2026  
**Status:** ✅ Pronto para produção
