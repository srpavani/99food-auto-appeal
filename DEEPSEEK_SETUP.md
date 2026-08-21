# 🚀 Como Usar DeepSeek

O DeepSeek está agora integrado ao sistema como opção de IA para análise de imagens e geração de defesas!

## ⚙️ Configuração

### 1. Obtenha sua API Key do DeepSeek

Acesse [https://platform.deepseek.com](https://platform.deepseek.com) e gere sua chave de API.

### 2. Configure o arquivo `.env`

Adicione sua chave de API no arquivo `.env`:

```env
# Configuração do Provedor de LLM
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat

# API Keys
DEEPSEEK_API_KEY=sua_chave_deepseek_aqui
```

### 3. Pronto!

O sistema agora usará o DeepSeek para:
- ✅ Analisar imagens anexadas pelos clientes
- ✅ Gerar defesas inteligentes para contestações
- ✅ Processar pedidos de reembolso

## 🔄 Alternando entre Providers

Você pode alternar facilmente entre os providers editando apenas o `.env`:

### Para usar OpenAI (GPT-4o):
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sua_chave_aqui
```

### Para usar Google Gemini:
```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-pro
GOOGLE_API_KEY=sua_chave_aqui
```

### Para usar DeepSeek:
```env
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=sua_chave_aqui
```

## 📋 Modelos DeepSeek Disponíveis

### Modelos de Texto (SEM suporte a imagens)
- `deepseek-chat` - Modelo principal, **apenas texto** (mais rápido e barato)
- `deepseek-reasoner` - Modelo com raciocínio avançado, apenas texto

### Modelos com Visão (COM suporte a imagens)
- `deepseek-vl-7b-chat` - Modelo Vision-Language 7B (analisa texto + imagens) ⭐ **Recomendado para este projeto**
- `deepseek-vl-1.3b-chat` - Versão menor e mais rápida (1.3B parâmetros)

⚠️ **IMPORTANTE**: O modelo `deepseek-chat` **NÃO analisa imagens**. Se seus pedidos têm fotos anexadas pelos clientes, use `deepseek-vl-7b-chat` para análise completa.

### Qual escolher?

| Situação | Modelo Recomendado |
|----------|-------------------|
| Pedidos COM imagens | `deepseek-vl-7b-chat` |
| Pedidos SEM imagens | `deepseek-chat` |
| Precisa de economia | `deepseek-vl-1.3b-chat` |

## 💡 Vantagens do DeepSeek

- ✅ Suporte nativo a análise de imagens
- ✅ API compatível com OpenAI (fácil integração)
- ✅ Bom custo-benefício
- ✅ Respostas rápidas

## 🐛 Troubleshooting

### Erro: "DEEPSEEK_API_KEY não configurada"
- Verifique se você criou o arquivo `.env` a partir do `env.example.txt`
- Certifique-se de que a variável `DEEPSEEK_API_KEY` está preenchida

### Erro de conexão
- Verifique sua conexão com a internet
- Confirme que sua API key está válida no [dashboard do DeepSeek](https://platform.deepseek.com)

## 📚 Recursos

- [Documentação oficial da API DeepSeek](https://platform.deepseek.com/docs)
- [Pricing do DeepSeek](https://platform.deepseek.com/pricing)
