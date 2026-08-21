# ❓ Perguntas Frequentes (FAQ)

## Configuração e Instalação

### Q: Qual versão do Python preciso?

**R:** Python 3.10 ou superior. Verifique com:

```bash
python --version
```

### Q: Como obtenho uma API key da OpenAI?

**R:** 

1. Acesse https://platform.openai.com/
2. Crie uma conta ou faça login
3. Vá em "API Keys"
4. Clique em "Create new secret key"
5. Copie a chave (começa com `sk-proj-...`)
6. Cole no `.env`:

```env
OPENAI_API_KEY=sk-proj-suachaveaqui
```

### Q: Como obtenho uma API key do Gemini?

**R:**

1. Acesse https://makersuite.google.com/app/apikey
2. Faça login com conta Google
3. Clique em "Create API Key"
4. Copie a chave (começa com `AIzaSy...`)
5. Cole no `.env`:

```env
GOOGLE_API_KEY=AIzaSysuachaveaqui
```

### Q: Posso usar ambos (OpenAI e Gemini)?

**R:** Sim! Deixe ambas as chaves no `.env` e escolha qual usar:

```env
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...

# Para usar OpenAI:
LLM_PROVIDER=openai

# Para usar Gemini:
LLM_PROVIDER=gemini
```

## Uso do Sistema

### Q: O sistema envia as contestações automaticamente?

**R:** SIM. O sistema:
1. Busca pedidos com reembolso
2. Analisa automaticamente
3. Gera defesa com IA
4. **ENVIA** a contestação

Se você quiser apenas ver as defesas sem enviar, comente a linha em `agent_graph.py`:

```python
# Linha ~200
# response = self.api_client.submit_appeal(...)
```

### Q: Quantos pedidos ele processa por vez?

**R:** Processa TODOS os pedidos no período especificado no `.env`:

```env
START_DATE=2026-01-10
END_DATE=2026-01-28
```

Para limitar, mude o `page_size`:

```env
PAGE_SIZE=5  # Processa apenas 5 pedidos
```

### Q: Como sei se funcionou?

**R:** Execute com logs detalhados:

```bash
python main.py
```

Você verá:
- ✅ Sucessos em verde
- ❌ Erros em vermelho
- 📊 Resumo final com quantidade enviada

### Q: Posso processar apenas um pedido específico?

**R:** Sim! Use o `example_usage.py`:

```python
# Edite o arquivo e descomente:
exemplo_manual()

# Mude o order_id para o desejado:
order_id = "5764655711753670171"
```

Execute:

```bash
python example_usage.py
```

## Problemas Comuns

### Q: Erro "OPENAI_API_KEY não configurada"

**R:** Você esqueceu de adicionar a chave no `.env`. Edite:

```bash
# Windows
notepad .env

# Linux/Mac
nano .env
```

Adicione:

```env
OPENAI_API_KEY=sua_chave_aqui
```

### Q: Erro "Connection refused" ou "Failed to connect"

**R:** A API 99Food não está rodando. Verifique:

```bash
curl http://localhost:3002/health
```

Se não funcionar, inicie sua API 99Food primeiro.

### Q: Erro "Rate limit exceeded"

**R:** Você excedeu o limite da sua conta OpenAI/Gemini.

Soluções:
1. Aguarde alguns minutos
2. Adicione créditos na conta
3. Use um modelo mais barato (`gpt-3.5-turbo`)
4. Reduza o `page_size` no `.env`

### Q: Defesa gerada passa de 200 caracteres

**R:** O sistema já limita automaticamente. Se passar, é truncado com "...".

Para ajustar o limite, edite `agent_graph.py`:

```python
# Linha ~168
if len(defense) > 200:  # Mude aqui
    defense = defense[:197] + "..."
```

### Q: A IA está sendo "boazinha" demais com o cliente

**R:** Edite o `system_prompt` em `llm_client.py` para ser mais agressivo:

```python
system_prompt = """Você é um advogado AGRESSIVO da loja.
O cliente SEMPRE está errado e agindo de má fé.
Seja FIRME e DIRETO ao recusar o reembolso."""
```

### Q: Quero que a IA analise a imagem com mais cuidado

**R:** Adicione instruções específicas no prompt em `llm_client.py`:

```python
if image_url:
    user_content[0]["text"] += """

ANALISE A IMAGEM CUIDADOSAMENTE:
- O produto está visível?
- A embalagem está intacta?
- Corresponde ao pedido?
Use esses detalhes na defesa."""
```

## Customização

### Q: Posso adicionar mais campos na contestação?

**R:** Sim! A API aceita `evidences` (array de URLs de imagens).

Edite `api_client.py`:

```python
def submit_appeal(self, order_id, apply_id, comments, evidences=[]):
    payload = {
        "orderId": order_id,
        "applyId": apply_id,
        "comments": comments,
        "reasonId": "",
        "evidences": evidences  # Adicione URLs aqui
    }
```

### Q: Posso salvar as defesas em um arquivo antes de enviar?

**R:** Sim! Adicione em `agent_graph.py`:

```python
def submit_appeal(self, state: AgentState):
    # Salva antes de enviar
    with open("defesas.txt", "a", encoding="utf-8") as f:
        f.write(f"Pedido: {state['current_order_id']}\n")
        f.write(f"Defesa: {state['generated_defense']}\n")
        f.write("-" * 60 + "\n")
    
    # Continua com envio...
```

### Q: Como fazer ele processar pedidos em paralelo?

**R:** Requer refatoração para `async`. Exemplo básico:

```python
# Seria necessário:
# 1. Trocar httpx.Client por httpx.AsyncClient
# 2. Tornar funções async
# 3. Usar asyncio.gather() para paralelo
```

Isso é um projeto mais avançado. O código atual é sequencial por simplicidade.

## Performance e Custos

### Q: Quanto custa usar o GPT-4o?

**R:** Preços aproximados (Jan 2026):
- GPT-4o: $5/milhão de tokens input, $15/milhão output
- Cada contestação: ~500 tokens = $0.01
- 100 pedidos: ~$1.00

### Q: Gemini é mais barato?

**R:** Sim, geralmente:
- Gemini 1.5 Pro: Gratuito até 50 req/dia
- Após isso: ~$7/milhão tokens

Teste ambos e veja qual performa melhor para seu caso.

### Q: Quanto tempo leva para processar 50 pedidos?

**R:** Aproximadamente:
- Buscar pedidos: 2s
- Por pedido:
  - Detalhes: 1s
  - IA: 3-5s (com imagem) ou 2s (sem)
  - Envio: 1s
- **Total**: 50 pedidos × 5s = ~4 minutos

## Segurança

### Q: Minhas API keys estão seguras?

**R:** Desde que:
1. ✅ Nunca commite o `.env` no Git
2. ✅ Use `.gitignore` (já incluído)
3. ✅ Não compartilhe o `.env` publicamente

### Q: O sistema armazena dados dos clientes?

**R:** NÃO. Tudo é processado em memória e descartado após execução.

Se quiser logs permanentes, adicione você mesmo no código.

## Desenvolvimento

### Q: Como contribuir ou reportar bugs?

**R:** 

1. Descreva o problema detalhadamente
2. Inclua os logs (`python main.py`)
3. Mencione:
   - Sistema operacional
   - Versão do Python
   - Provedor LLM usado
   - Mensagem de erro completa

### Q: Posso usar em produção?

**R:** Com cuidado:

1. ✅ Adicione retry logic para falhas de rede
2. ✅ Implemente rate limiting
3. ✅ Adicione monitoramento (ex: Sentry)
4. ✅ Configure timeout adequado
5. ✅ Teste extensivamente antes

### Q: Como atualizar dependências?

**R:**

```bash
pip install --upgrade -r requirements.txt
```

Ou individualmente:

```bash
pip install --upgrade langchain langgraph
```

## Dicas Avançadas

### Q: Posso usar Claude ao invés de GPT/Gemini?

**R:** Sim! Veja `ARQUITETURA.md` seção "Como Adicionar Novo Provedor".

Resumo:
1. Crie `ClaudeLLMClient` em `llm_client.py`
2. Adicione ao factory
3. Configure no `.env`

### Q: Como fazer debug de uma contestação específica?

**R:** Use `example_usage.py` com o `order_id` problemático e adicione `print()` statements.

### Q: Posso integrar com um sistema de notificações?

**R:** Sim! Adicione em `agent_graph.py`:

```python
def submit_appeal(self, state):
    # Após envio bem-sucedido:
    if response.get("success"):
        enviar_notificacao_telegram(
            f"Contestação enviada: {state['current_order_id']}"
        )
```

## Suporte

Se sua dúvida não foi respondida:

1. Leia `ARQUITETURA.md` para entender como funciona
2. Execute `python test_setup.py` para diagnosticar
3. Execute `python test_llm_only.py` para testar só a IA
4. Verifique os logs no terminal

**Nota:** Este é um sistema open-source fornecido "como está". 
Use por sua conta e risco.
