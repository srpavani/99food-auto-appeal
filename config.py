"""
Configurações do sistema carregadas de variáveis de ambiente.
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # LLM Provider
    llm_provider: str = "openai"  # openai | gemini | deepseek
    llm_model: str = "gpt-4o"
    
    # API Keys
    openai_api_key: str = ""
    google_api_key: str = ""
    deepseek_api_key: str = ""
    
    # API Base URL
    base_api_url: str = "http://localhost:3002"
    
    # Data range para buscar reembolsos
    start_date: str = "2026-01-10"
    end_date: str = "2026-01-28"
    
    # Paginação
    page_size: int = 20
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_settings() -> Settings:
    """Carrega as configurações da aplicação."""
    return Settings()
