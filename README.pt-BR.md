# 🤖 Sistema de Contestação Automática - 99Food

> Sistema inteligente que usa IA para contestar reembolsos automaticamente no 99Food.

## 🎯 O que esse sistema faz?

1. **Busca** pedidos com solicitação de reembolso na sua API 99Food
2. **Analisa** o motivo da reclamação e a foto de prova (se tiver)
3. **Gera** uma defesa profissional usando IA (GPT-4o ou Gemini)
4. **Envia** a contestação automaticamente

**Tudo isso em segundos, sem intervenção manual!**

## ⚡ Instalação Rápida

### Windows

```powershell
# 1. Clone ou baixe este projeto
cd H:\99LANGCORE

# 2. Execute o instalador
.\install.ps1

# 3. Configure suas chaves no .env
notepad .env

# 4. Teste
python test_setup.py

# 5. Execute!
python main.py
```

### Linux/Mac

```bash
# 1. Clone ou baixe este projeto
cd ~/99LANGCORE

# 2. Execute o instalador
bash install.sh

# 3. Configure suas chaves no .env
nano .env

# 4. Teste
python test_setup.py

# 5. Execute!
python main.py
```

## 🔑 Configuração do .env

Edite o arquivo `.env` e adicione suas credenciais:

```env
# Escolha: openai ou gemini
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o

# Adicione SUA chave (pegue em platform.openai.com)
OPENAI_API_KEY=sk-proj-xxxxx

# OU use Gemini (pegue em makersuite.google.com)
GOOGLE_API_KEY=AIzaSyxxxxx

# URL da sua API 99Food
BASE_API_URL=http://localhost:3002

# Período para buscar reembolsos
START_DATE=2026-01-10
END_DATE=2026-01-28
```

## 📸 Exemplo de Uso

```bash
python main.py
```

**Saída:**

```
🚀 SISTEMA DE CONTESTAÇÃO AUTOMÁTICA - 99FOOD
================================================================

🔧 Configurações:
   - Provedor LLM: OPENAI
   - Modelo: gpt-4o
   - API Base: http://localhost:3002

🔍 Buscando pedidos com reembolso...
✅ Encontrados 9 pedidos

📄 Processando pedido #222028...
📋 Motivo: Itens incorretos
🖼️  Imagem: SIM (analisando com IA...)

🤖 Gerando defesa...
💬 "Consideramos improvável. A imagem mostra produtos corretos. 
    Pedidos são conferidos antes do envio."

📤 Enviando contestação...
✅ Enviada com sucesso!

================================================================
📊 RESUMO
================================================================
✅ Pedidos processados: 9
📤 Contestações enviadas: 9
❌ Erros: 0
================================================================
```

## 🧠 Como Funciona?

O sistema usa **LangGraph** para orquestrar um fluxo inteligente:

```
┌─────────────────┐
│ Buscar Pedidos  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Obter Detalhes  │◄──┐
└────────┬────────┘   │
         │            │
         ▼            │
┌─────────────────┐   │
│  Analisar c/ IA │   │
│  (texto+imagem) │   │
└────────┬────────┘   │
         │            │
         ▼            │
┌─────────────────┐   │
│ Enviar Contest. │   │
└────────┬────────┘   │
         │            │
         └────────────┘
         (próximo pedido)
```

### Capacidade Multimodal 🖼️

A IA **VÊ** as imagens enviadas pelos clientes e analisa junto com o texto:

- ✅ Identifica se o produto está visível
- ✅ Verifica se corresponde ao pedido
- ✅ Usa essas informações na defesa

## 🛠️ Scripts Úteis

| Script | Função |
|--------|--------|
| `main.py` | **Execute este** para rodar o sistema completo |
| `test_setup.py` | Testa configuração e conexão com APIs |
| `test_llm_only.py` | Testa apenas a IA (sem precisar da API 99Food) |
| `example_usage.py` | Exemplos de uso programático |

## 📁 Estrutura do Projeto

```
99LANGCORE/
├── main.py              ⭐ EXECUTE ESTE
├── config.py            Carrega configurações do .env
├── models.py            Schemas das respostas da API
├── llm_client.py        OpenAI + Gemini (multimodal)
├── api_client.py        Cliente HTTP para 99Food
├── agent_graph.py       Orquestração com LangGraph
├── .env                 🔐 Suas configurações
└── requirements.txt     Dependências Python
```

## 🎓 Documentação Completa

| Arquivo | Conteúdo |
|---------|----------|
| `GUIA_INSTALACAO.md` | Instalação passo a passo detalhada |
| `FAQ.md` | Perguntas frequentes e troubleshooting |
| `ARQUITETURA.md` | Como funciona internamente (técnico) |
| `README.md` | Documentação em inglês |

## 💡 Dicas

### Trocar de OpenAI para Gemini

Edite apenas 2 linhas no `.env`:

```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-pro
```

### Processar Apenas Pedidos Recentes

```env
START_DATE=2026-01-27
END_DATE=2026-01-28
```

### Ajustar Tom da IA

Edite `llm_client.py` linha ~40 (system_prompt) para mudar a personalidade.

## ⚠️ Observações Importantes

- 🔐 **Nunca** commite o `.env` no Git (já está no `.gitignore`)
- 💰 Usar GPT-4o tem custo (~$0.01 por contestação)
- 🧪 Teste com poucos pedidos primeiro (`PAGE_SIZE=5`)
- 📊 Sempre verifique os logs para garantir que enviou corretamente

## 🐛 Problemas?

1. Execute `python test_setup.py` para diagnosticar
2. Leia `FAQ.md` - provavelmente sua dúvida está lá
3. Verifique os logs no terminal quando executar `main.py`

## 📊 Performance

- **Velocidade**: ~5 segundos por pedido
- **Custo**: ~$0.01 por pedido (GPT-4o)
- **Precisão**: IA analisa texto E imagem

## 🔮 Recursos

- ✅ Suporta OpenAI (GPT-4o) e Google Gemini
- ✅ Análise multimodal (texto + imagem)
- ✅ Logs detalhados
- ✅ Tratamento de erros
- ✅ Configuração via .env
- ✅ Extensível (fácil adicionar novos provedores)

## 📝 Licença

Use como quiser, por sua conta e risco.

---

**Feito com ❤️ e Python**

Dúvidas? Leia `FAQ.md` ou `GUIA_INSTALACAO.md`
