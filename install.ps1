# Script de instalação automática para Windows
# Execute: .\install.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INSTALAÇÃO - Sistema de Contestação" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se Python está instalado
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python não encontrado!" -ForegroundColor Red
    Write-Host "   Instale Python 3.10+ de https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Verifica versão do Python
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$Matches[1]
    $minor = [int]$Matches[2]
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
        Write-Host "   ✗ Python 3.10+ necessário. Versão atual: $pythonVersion" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Instala dependências
Write-Host "2. Instalando dependências..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip | Out-Null
    pip install -r requirements.txt
    Write-Host "   ✓ Dependências instaladas com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Erro ao instalar dependências" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Verifica .env
Write-Host "3. Verificando configuração..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✓ Arquivo .env encontrado" -ForegroundColor Green
    
    $envContent = Get-Content ".env" -Raw
    
    $hasOpenAI = $envContent -match "OPENAI_API_KEY=.+"
    $hasGemini = $envContent -match "GOOGLE_API_KEY=.+"
    
    if (-not $hasOpenAI -and -not $hasGemini) {
        Write-Host "   ⚠ ATENÇÃO: Nenhuma API key configurada no .env" -ForegroundColor Yellow
        Write-Host "   Edite o arquivo .env e adicione pelo menos uma chave:" -ForegroundColor Yellow
        Write-Host "     - OPENAI_API_KEY=sk-..." -ForegroundColor Cyan
        Write-Host "     - GOOGLE_API_KEY=AIza..." -ForegroundColor Cyan
    } else {
        Write-Host "   ✓ API key(s) configurada(s)" -ForegroundColor Green
    }
} else {
    Write-Host "   ✗ Arquivo .env não encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INSTALAÇÃO CONCLUÍDA!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Configure suas API keys no .env:" -ForegroundColor White
Write-Host "   notepad .env" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Teste a configuração:" -ForegroundColor White
Write-Host "   python test_setup.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Execute o sistema:" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para mais informações, leia:" -ForegroundColor White
Write-Host "   - GUIA_INSTALACAO.md" -ForegroundColor Cyan
Write-Host "   - FAQ.md" -ForegroundColor Cyan
Write-Host "   - ARQUITETURA.md" -ForegroundColor Cyan
Write-Host ""
