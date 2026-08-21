# Sistema de Contestação Automática via IA - 99Food

Sistema autônomo de contestação de reembolsos utilizando LangGraph e modelos de linguagem multimodais (GPT-4o/Gemini).

## Funcionalidades

- 🤖 **Análise Multimodal**: Analisa texto e imagens das reclamações
- 🔄 **Orquestração com LangGraph**: Fluxo de execução robusto e escalável
- 🎯 **Defesa Automática**: Gera argumentações persuasivas pró-loja
- 🔌 **Multi-Provedor**: Suporta OpenAI, Google Gemini e DeepSeek (configurável via .env)
- 📊 **Logs Detalhados**: Acompanhamento completo do processo

## Instalação

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais
```

## Configuração

Edite o arquivo `.env`:

```env
LLM_PROVIDER=openai  # ou gemini | deepseek
LLM_MODEL=gpt-4o     # ou gemini-1.5-pro | deepseek-vl-7b-chat

# API Keys (use apenas a do provider escolhido)
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
DEEPSEEK_API_KEY=sk-...

BASE_API_URL=http://localhost:3002
```

### Modelos DeepSeek:
- `deepseek-chat` - Apenas texto (SEM análise de imagens)
- `deepseek-vl-7b-chat` - Texto + Imagens ⭐ **Recomendado para este projeto**
- `deepseek-vl-1.3b-chat` - Texto + Imagens (versão menor/rápida)

> 📖 Para configurar o DeepSeek, consulte o guia completo em [DEEPSEEK_SETUP.md](DEEPSEEK_SETUP.md)

## Uso

```bash
python main.py
```

## Arquitetura

```
┌─────────────────────┐
│ Buscar Reembolsos   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Obter Detalhes      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Analisar com IA     │◄── Visão Multimodal
│ (Texto + Imagem)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Enviar Contestação  │
└─────────────────────┘
```

## Estrutura do Projeto

```
.
├── main.py                 # Script principal
├── config.py               # Configurações e variáveis de ambiente
├── models.py               # Schemas Pydantic (API responses)
├── llm_client.py           # Factory para OpenAI/Gemini
├── api_client.py           # Cliente HTTP para API 99Food
├── agent_graph.py          # Definição do grafo LangGraph
└── requirements.txt
```

## Fluxo de Execução

1. **Fetch Refunds**: Busca pedidos com solicitação de reembolso
2. **Get Details**: Extrai detalhes, motivos e imagens de prova
3. **Generate Defense**: IA analisa e gera argumentação
4. **Submit Appeal**: Envia contestação via API

## Observações

- O sistema assume que a loja está correta (advogado de defesa)
- Analisa imagens quando disponíveis para fortalecer a defesa
- Limite de 200 caracteres para o comentário de contestação
