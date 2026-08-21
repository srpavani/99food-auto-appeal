#!/bin/bash
# Script de instalação automática para Linux/Mac
# Execute: bash install.sh

echo "========================================"
echo "  INSTALAÇÃO - Sistema de Contestação"
echo "========================================"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Verifica se Python está instalado
echo -e "${YELLOW}1. Verificando Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "   ${GREEN}✓ Python encontrado: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    echo -e "   ${GREEN}✓ Python encontrado: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python"
else
    echo -e "   ${RED}✗ Python não encontrado!${NC}"
    echo -e "   ${RED}Instale Python 3.10+ de https://www.python.org/downloads/${NC}"
    exit 1
fi

# Verifica versão do Python
VERSION_NUM=$(echo $PYTHON_VERSION | grep -oP '\d+\.\d+' | head -1)
MAJOR=$(echo $VERSION_NUM | cut -d. -f1)
MINOR=$(echo $VERSION_NUM | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
    echo -e "   ${RED}✗ Python 3.10+ necessário. Versão atual: $PYTHON_VERSION${NC}"
    exit 1
fi

echo ""

# Cria virtual environment (opcional mas recomendado)
echo -e "${YELLOW}2. Criando ambiente virtual...${NC}"
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo -e "   ${GREEN}✓ Ambiente virtual criado${NC}"
else
    echo -e "   ${GREEN}✓ Ambiente virtual já existe${NC}"
fi

# Ativa o ambiente virtual
source venv/bin/activate

echo ""

# Instala dependências
echo -e "${YELLOW}3. Instalando dependências...${NC}"
$PYTHON_CMD -m pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✓ Dependências instaladas com sucesso!${NC}"
else
    echo -e "   ${RED}✗ Erro ao instalar dependências${NC}"
    exit 1
fi

echo ""

# Verifica .env
echo -e "${YELLOW}4. Verificando configuração...${NC}"
if [ -f ".env" ]; then
    echo -e "   ${GREEN}✓ Arquivo .env encontrado${NC}"
    
    # Verifica se há API keys
    if grep -q "OPENAI_API_KEY=sk-" .env || grep -q "GOOGLE_API_KEY=AIza" .env; then
        echo -e "   ${GREEN}✓ API key(s) configurada(s)${NC}"
    else
        echo -e "   ${YELLOW}⚠ ATENÇÃO: Nenhuma API key configurada no .env${NC}"
        echo -e "   ${YELLOW}Edite o arquivo .env e adicione pelo menos uma chave:${NC}"
        echo -e "     ${CYAN}- OPENAI_API_KEY=sk-...${NC}"
        echo -e "     ${CYAN}- GOOGLE_API_KEY=AIza...${NC}"
    fi
else
    echo -e "   ${RED}✗ Arquivo .env não encontrado!${NC}"
    exit 1
fi

echo ""
echo "========================================"
echo -e "  ${GREEN}INSTALAÇÃO CONCLUÍDA!${NC}"
echo "========================================"
echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo ""
echo -e "${NC}1. Ative o ambiente virtual:${NC}"
echo -e "   ${CYAN}source venv/bin/activate${NC}"
echo ""
echo -e "${NC}2. Configure suas API keys no .env:${NC}"
echo -e "   ${CYAN}nano .env${NC}  # ou use seu editor favorito"
echo ""
echo -e "${NC}3. Teste a configuração:${NC}"
echo -e "   ${CYAN}python test_setup.py${NC}"
echo ""
echo -e "${NC}4. Execute o sistema:${NC}"
echo -e "   ${CYAN}python main.py${NC}"
echo ""
echo -e "${NC}Para mais informações, leia:${NC}"
echo -e "   ${CYAN}- GUIA_INSTALACAO.md${NC}"
echo -e "   ${CYAN}- FAQ.md${NC}"
echo -e "   ${CYAN}- ARQUITETURA.md${NC}"
echo ""
