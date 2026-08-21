"""
Factory para criar clientes LLM (OpenAI, Gemini ou DeepSeek) com suporte multimodal.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from config import Settings
import logging

logger = logging.getLogger(__name__)


class LLMClient(ABC):
    """Interface abstrata para clientes LLM."""
    
    @abstractmethod
    def generate_defense(
        self, 
        reason: str, 
        items: str,
        image_url: Optional[str] = None
    ) -> str:
        """Gera um texto de defesa baseado no motivo e (opcionalmente) imagem."""
        pass


class OpenAILLMClient(LLMClient):
    """Cliente LLM usando OpenAI (GPT-4o com visão)."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=0.7,
            max_tokens=450
        )
    
    def generate_defense(
        self, 
        reason: str, 
        items: str,
        image_url: Optional[str] = None
    ) -> str:
        """Gera defesa usando GPT-4o (multimodal se houver imagem)."""
        
        system_prompt = """Você é um assistente de contestação para um restaurante no 99Food.
Sua função é SEMPRE defender a loja e argumentar que o cliente está equivocado ou agindo de má fé.

REGRAS IMPORTANTES:
1. A loja SEMPRE está correta
2. Os pedidos são conferidos e embalados com cuidado
3. Se há foto, use-a como prova de que o produto foi entregue corretamente
4. Seja educado mas FIRME
5. MÁXIMO 200 caracteres na resposta
6. Não use quebras de linha

Argumente de forma profissional para recusar o reembolso."""

        user_content = [
            {
                "type": "text",
                "text": f"""Cliente pediu reembolso alegando: "{reason}"
Itens do pedido: {items}

Analise e escreva uma defesa curta (máx 200 chars) recusando o reembolso."""
            }
        ]
        
        # Se houver imagem, adiciona ao conteúdo
        if image_url:
            user_content.append({
                "type": "image_url",
                "image_url": {"url": image_url}
            })
            user_content[0]["text"] += "\n\nImagem de prova anexada pelo cliente. Use-a na argumentação."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        response = self.llm.invoke(messages)
        return response.content.strip()


class GeminiLLMClient(LLMClient):
    """Cliente LLM usando Google Gemini (com visão)."""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0.7,
            max_tokens=350
        )
    
    def generate_defense(
        self, 
        reason: str, 
        items: str,
        image_url: Optional[str] = None
    ) -> str:
        """Gera defesa usando Gemini (multimodal se houver imagem)."""
        
        system_prompt = """Você é um assistente de contestação para um restaurante no 99Food.
Sua função é SEMPRE defender a loja e argumentar que o cliente está equivocado ou agindo de má fé.

REGRAS IMPORTANTES:
1. A loja SEMPRE está correta
2. Os pedidos são conferidos e embalados com cuidado
3. Se há foto, use-a como prova de que o produto foi entregue corretamente
4. Seja educado mas FIRME
5. MÁXIMO 200 caracteres na resposta
6. Não use quebras de linha

Argumente de forma profissional para recusar o reembolso."""

        text_content = f"""Cliente pediu reembolso alegando: "{reason}"
Itens do pedido: {items}

Analise e escreva uma defesa curta (máx 200 chars) recusando o reembolso."""
        
        # Gemini usa formato diferente para imagens
        if image_url:
            text_content += "\n\nImagem de prova anexada pelo cliente. Use-a na argumentação."
            message = HumanMessage(
                content=[
                    {"type": "text", "text": f"{system_prompt}\n\n{text_content}"},
                    {"type": "image_url", "image_url": image_url}
                ]
            )
        else:
            message = HumanMessage(content=f"{system_prompt}\n\n{text_content}")
        
        response = self.llm.invoke([message])
        return response.content.strip()


class DeepSeekLLMClient(LLMClient):
    """Cliente LLM usando DeepSeek via OpenAI SDK.
    
    Nota: O modelo 'deepseek-chat' NÃO suporta visão/imagens.
    Para análise de imagens, use modelos VL como 'deepseek-vl-7b-chat'.
    """
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url="https://api.deepseek.com",
            temperature=0.7,
            max_tokens=300
        )
        self.model = model
        # Modelos que suportam visão
        self.vision_models = ["deepseek-vl-7b-chat", "deepseek-vl-1.3b-chat"]
        self.supports_vision = any(vm in model.lower() for vm in self.vision_models)
    
    def generate_defense(
        self, 
        reason: str, 
        items: str,
        image_url: Optional[str] = None
    ) -> str:
        """Gera defesa usando DeepSeek.
        
        Se o modelo não suportar visão e houver imagem, processa apenas o texto.
        """
        
        system_prompt = """Você é um assistente de contestação para um restaurante no 99Food.
Sua função é SEMPRE defender a loja e argumentar que o cliente está equivocado ou agindo de má fé.

REGRAS IMPORTANTES:
1. A loja SEMPRE está correta
2. Os pedidos são conferidos e embalados com cuidado
3. Se há foto, use-a como prova de que o produto foi entregue corretamente
4. Seja educado mas FIRME
5. MÁXIMO 200 caracteres na resposta
6. Não use quebras de linha

Argumente de forma profissional para recusar o reembolso."""

        text_content = f"""Cliente pediu reembolso alegando: "{reason}"
Itens do pedido: {items}

Analise e escreva uma defesa curta (máx 200 chars) recusando o reembolso."""
        
        # Se há imagem e o modelo suporta visão, usa formato multimodal
        if image_url and self.supports_vision:
            user_content = [
                {
                    "type": "text",
                    "text": text_content + "\n\nImagem de prova anexada pelo cliente. Use-a na argumentação."
                },
                {
                    "type": "image_url",
                    "image_url": {"url": image_url}
                }
            ]
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        else:
            # Modelo não suporta visão ou não há imagem - usa apenas texto
            if image_url and not self.supports_vision:
                logger.warning(f"⚠️  Modelo '{self.model}' não suporta visão. Imagem será ignorada. Use 'deepseek-vl-7b-chat' para análise de imagens.")
                # Avisa que há imagem mas o modelo não suporta
                text_content += f"\n\nObs: Cliente anexou imagem mas nossos registros mostram que o pedido foi preparado corretamente."
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_content}
            ]
        
        response = self.llm.invoke(messages)
        return response.content.strip()


def create_llm_client(settings: Settings) -> LLMClient:
    """Factory para criar o cliente LLM apropriado."""
    
    provider = settings.llm_provider.lower()
    
    if provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY não configurada no .env")
        return OpenAILLMClient(
            api_key=settings.openai_api_key,
            model=settings.llm_model
        )
    
    elif provider == "gemini":
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY não configurada no .env")
        return GeminiLLMClient(
            api_key=settings.google_api_key,
            model=settings.llm_model
        )
    
    elif provider == "deepseek":
        if not settings.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY não configurada no .env")
        return DeepSeekLLMClient(
            api_key=settings.deepseek_api_key,
            model=settings.llm_model
        )
    
    else:
        raise ValueError(f"Provedor '{provider}' não suportado. Use 'openai', 'gemini' ou 'deepseek'")
