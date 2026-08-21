# 🎯 COMECE AQUI

> **Seu sistema de contestação automática está pronto!**

## ⚡ 3 Passos para Começar

### 1️⃣ Configure suas API Keys

Edite o arquivo `.env`:

```bash
# Windows
notepad .env

# Linux/Mac  
nano .env
```

Adicione sua chave da OpenAI OU Gemini:

```env
# Use OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-sua-chave-aqui

# OU use Gemini
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSy-sua-chave-aqui
```

**Como obter API keys?**
- OpenAI: https://platform.openai.com/api-keys
- Gemini: https://makersuite.google.com/app/apikey

### 2️⃣ Instale as Dependências

```bash
pip install -r requirements.txt
```

**OU** use o instalador automático:

```bash
# Windows
.\install.ps1

# Linux/Mac
bash install.sh
```

### 3️⃣ Execute!

```bash
python main.py
```

Isso vai:
1. Buscar pedidos com reembolso da sua API 99Food
2. Analisar cada reclamação (incluindo fotos!)
3. Gerar defesa com IA
4. Enviar contestação automaticamente

---

## ✅ Antes de Executar

### Verifique se sua API 99Food está rodando:

```bash
curl http://localhost:3002/orders/refunds
```

Se não funcionar, inicie sua API primeiro!

### Teste a configuração:

```bash
python test_setup.py
```

Você deve ver:
```
✅ PASSOU - Configurações
✅ PASSOU - API 99Food
✅ PASSOU - Cliente LLM
```

---

## 📚 Documentação Rápida

### Leia na ordem:

1. **Este arquivo** (você está aqui! 😊)
2. **QUICKSTART.md** - Início em 30 segundos
3. **README.pt-BR.md** - Visão completa do projeto
4. **FAQ.md** - Quando algo der errado

### Se quiser se aprofundar:

- **ARQUITETURA.md** - Como funciona internamente
- **DEPLOYMENT.md** - Colocar em produção
- **CONTRIBUTING.md** - Contribuir com o projeto

### Arquivo mais importante:

**`.env`** - Configure suas chaves aqui! 🔑

---

## 🎓 Exemplos de Uso

### Uso Básico

```bash
# Processar todos os reembolsos do período
python main.py
```

### Testar apenas a IA (sem enviar)

```bash
python test_llm_only.py
```

### Processar pedido específico

Edite `example_usage.py` e descomente `exemplo_manual()`:

```python
if __name__ == "__main__":
    exemplo_manual()  # Descomente esta linha
```

Depois execute:

```bash
python example_usage.py
```

---

## 🔧 Configurações Importantes

### Período de Busca

Edite `.env`:

```env
START_DATE=2026-01-10
END_DATE=2026-01-28
```

### Quantidade de Pedidos

```env
PAGE_SIZE=20  # Processar até 20 pedidos
```

### Trocar de Provedor

```env
# OpenAI
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o

# OU Gemini
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-pro
```

---

## 🎯 O que o Sistema Faz?

```
┌─────────────────────────────────────────────┐
│  1. Busca pedidos com reembolso pendente   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  2. Para cada pedido:                       │
│     - Extrai motivo da reclamação          │
│     - Pega foto de prova (se tiver)        │
│     - Identifica itens do pedido           │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  3. IA analisa:                             │
│     ✓ Lê o motivo do cliente              │
│     ✓ Vê a foto (multimodal!)             │
│     ✓ Considera contexto do pedido        │
│     ✓ Gera defesa profissional            │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  4. Envia contestação automaticamente       │
│     - Texto gerado pela IA                  │
│     - Máximo 200 caracteres                 │
│     - Sempre defende a loja                 │
└─────────────────────────────────────────────┘
```

---

## 🚨 Problemas Comuns

### "OPENAI_API_KEY não configurada"

Você esqueceu de editar o `.env`. Abra e adicione sua chave.

### "Connection refused" 

Sua API 99Food não está rodando. Inicie-a primeiro!

### "Rate limit exceeded"

Você excedeu o limite da sua conta OpenAI/Gemini. Aguarde ou adicione créditos.

### Outros problemas?

Leia o **FAQ.md** - 90% das dúvidas estão lá!

---

## 💡 Dicas Úteis

### 1. Teste com poucos pedidos primeiro

```env
PAGE_SIZE=3  # Apenas 3 pedidos para testar
```

### 2. Verifique os logs

O sistema mostra tudo que está fazendo:

```
🔍 Buscando pedidos...
✅ Encontrados 9 pedidos
📄 Processando pedido #222028...
🖼️  Imagem: SIM
🤖 Gerando defesa...
💬 Defesa: "Consideramos improvável..."
📤 Enviando...
✅ Sucesso!
```

### 3. Salve os logs

```bash
python main.py > logs.txt 2>&1
```

### 4. Use Docker para facilitar

```bash
docker-compose up
```

---

## 📊 Estrutura de Arquivos

```
99LANGCORE/
│
├── 🟢 START_HERE.md         ← VOCÊ ESTÁ AQUI
│
├── 🔴 main.py                ← EXECUTE ESTE
├── 🔴 .env                   ← CONFIGURE ESTE
│
├── test_setup.py             (testar config)
├── test_llm_only.py          (testar IA)
├── example_usage.py          (exemplos)
│
├── README.pt-BR.md           (doc completa)
├── QUICKSTART.md             (início rápido)
├── FAQ.md                    (dúvidas)
├── ARQUITETURA.md            (técnico)
│
└── [outros arquivos...]
```

---

## 🎉 Está Funcionando?

Se sim, parabéns! 🚀

**Próximos passos:**

1. Ajuste o prompt da IA (se quiser) em `llm_client.py`
2. Configure execução automática (cron/task scheduler)
3. Leia `DEPLOYMENT.md` para produção
4. Contribua com melhorias! Leia `CONTRIBUTING.md`

---

## 📞 Precisa de Ajuda?

1. ✅ Leia `FAQ.md` primeiro
2. ✅ Execute `python test_setup.py`
3. ✅ Verifique os logs no terminal
4. ✅ Consulte `GUIA_INSTALACAO.md`

---

## 🌟 Recursos do Sistema

| Recurso | Status |
|---------|--------|
| ✅ OpenAI (GPT-4o) | Pronto |
| ✅ Google Gemini | Pronto |
| ✅ Análise de imagens | Pronto |
| ✅ Contestação automática | Pronto |
| ✅ Logs detalhados | Pronto |
| ✅ Docker support | Pronto |
| ✅ Configuração via .env | Pronto |
| ⏳ Claude (Anthropic) | Planejado |
| ⏳ Dashboard web | Planejado |
| ⏳ Notificações | Planejado |

---

**Versão**: 1.0.0  
**Última atualização**: 2026-01-28

**Feito com ❤️ e Python + LangGraph**

---

## 📢 Importante

⚠️ Este sistema **ENVIA** contestações automaticamente para a API 99Food.

Se você quiser apenas **TESTAR** sem enviar de verdade:

1. Use `python test_llm_only.py` para testar apenas a IA
2. Ou comente a linha de envio em `agent_graph.py`:

```python
# Linha ~200 em agent_graph.py
# response = self.api_client.submit_appeal(...)  # Comente esta linha
```

---

🚀 **Pronto para começar? Execute:** `python main.py`
