# ⚡ Quickstart - 30 Segundos

## 1. Instalar

```bash
pip install -r requirements.txt
```

## 2. Configurar .env

```bash
notepad .env  # Windows
nano .env     # Linux/Mac
```

Adicione:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-sua-chave-aqui
BASE_API_URL=http://localhost:3002
START_DATE=2026-01-10
END_DATE=2026-01-28
```

## 3. Testar

```bash
python test_setup.py
```

## 4. Executar

```bash
python main.py
```

## Pronto! 🎉

O sistema vai:
- Buscar pedidos com reembolso
- Analisar com IA (incluindo imagens)
- Enviar contestações automaticamente

---

**Deu erro?** Leia `FAQ.md`

**Quer entender melhor?** Leia `GUIA_INSTALACAO.md`

**Quer customizar?** Leia `ARQUITETURA.md`
