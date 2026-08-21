# 🚀 Guia de Instalação e Uso

## Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Chave de API da OpenAI OU Google Gemini
- API 99Food rodando em `http://localhost:3002`

## Passo 1: Instalar Dependências

```bash
pip install -r requirements.txt
```

## Passo 2: Configurar Variáveis de Ambiente

Edite o arquivo `.env` e adicione suas credenciais:

```env
# Escolha o provedor: openai ou gemini
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o

# Adicione SUA chave de API
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
# OU
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxx

# URL da API 99Food
BASE_API_URL=http://localhost:3002

# Período para buscar reembolsos
START_DATE=2026-01-10
END_DATE=2026-01-28
```

## Passo 3: Testar Configuração

Antes de rodar o sistema completo, teste se tudo está configurado corretamente:

```bash
python test_setup.py
```

Você deve ver:

```
✅ PASSOU - Configurações
✅ PASSOU - API 99Food
✅ PASSOU - Cliente LLM
```

## Passo 4: Executar o Sistema

```bash
python main.py
```

## O que o Sistema Faz?

1. **Busca Pedidos**: Consulta a API para listar pedidos com reembolso pendente
2. **Analisa Detalhes**: Para cada pedido, extrai:
   - Motivo da reclamação
   - Imagens de prova (se houver)
   - Itens do pedido
3. **Gera Defesa com IA**: Usa GPT-4o ou Gemini para criar um argumento
   - ✅ Analisa texto E imagem (multimodal)
   - ✅ Sempre defende a loja
   - ✅ Máximo 200 caracteres
4. **Envia Contestação**: Submete via API automaticamente

## Exemplo de Execução

```
🚀 SISTEMA DE CONTESTAÇÃO AUTOMÁTICA - 99FOOD
================================================================

🔧 Configurações:
   - Provedor LLM: OPENAI
   - Modelo: gpt-4o
   - API Base: http://localhost:3002
   - Período: 2026-01-10 até 2026-01-28

🔍 Buscando pedidos com reembolso...
✅ Encontrados 9 pedidos com reembolso

📄 Buscando detalhes do pedido 5764655711753670171...
📋 Motivo: Itens incorretos
🖼️  Imagem: SIM
   URL: https://img0.didiglobal.com/static/soda_public/...

🤖 Gerando defesa com IA...
💬 Defesa gerada: Consideramos essa alegação improvável. A imagem comprova a entrega correta dos itens. Nossos pedidos são conferidos cuidadosamente antes do envio.

📤 Enviando contestação...
✅ Contestação enviada com sucesso para pedido 5764655711753670171

================================================================
📊 RESUMO DA EXECUÇÃO
================================================================
✅ Pedidos processados: 9
📤 Contestações enviadas: 9
❌ Erros encontrados: 0
================================================================
```

## Trocar de Provedor

Para usar Gemini ao invés de OpenAI, simplesmente edite o `.env`:

```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-pro
GOOGLE_API_KEY=sua_chave_gemini
```

E execute novamente `python main.py`.

## Troubleshooting

### Erro: "OPENAI_API_KEY não configurada"

Você esqueceu de adicionar a chave no `.env`. Edite o arquivo e adicione sua chave.

### Erro: "Connection refused" ou "Connection error"

A API 99Food não está rodando em `localhost:3002`. Verifique se o servidor está ativo.

### Erro ao instalar dependências

Tente atualizar o pip primeiro:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Estrutura de Arquivos

```
99LANGCORE/
├── main.py              # Script principal - EXECUTE ESTE
├── test_setup.py        # Testa configuração
├── config.py            # Carrega .env
├── models.py            # Schemas Pydantic
├── llm_client.py        # Factory OpenAI/Gemini
├── api_client.py        # Cliente HTTP 99Food
├── agent_graph.py       # Grafo LangGraph
├── requirements.txt     # Dependências
├── .env                 # Configurações (EDITE ESTE)
└── README.md
```

## Ajustes Avançados

### Mudar Período de Busca

Edite no `.env`:

```env
START_DATE=2026-01-20
END_DATE=2026-01-28
```

### Mudar Tom da IA

Edite `llm_client.py`, linha com `system_prompt` para ajustar a "personalidade" do agente.

### Aumentar Limite de Caracteres

Edite `agent_graph.py`, método `generate_defense`:

```python
if len(defense) > 200:  # Mude 200 para o valor desejado
```

## Suporte

Em caso de problemas, verifique os logs no terminal. O sistema exibe:

- 🔍 Ações em andamento
- ✅ Sucessos
- ❌ Erros detalhados
- 📊 Resumo final
