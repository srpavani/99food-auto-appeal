"""
Cliente HTTP para interagir com a API 99Food.
"""
import httpx
from typing import List, Dict, Any
from models import (
    RefundListResponse, 
    OrderDetailResponse, 
    AppealRequest,
    AppealResponse
)


class APIClient:
    """Cliente para comunicação com a API 99Food."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(timeout=30.0)
    
    def get_refund_orders(
        self, 
        start_date: str, 
        end_date: str,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Busca pedidos com solicitação de reembolso.
        
        Args:
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD)
            page: Número da página
            page_size: Tamanho da página
        
        Returns:
            Dict com a resposta da API
        """
        url = f"{self.base_url}/orders/refunds"
        payload = {
            "startDate": start_date,
            "endDate": end_date,
            "page": page,
            "pageSize": page_size,
            "orderType": 0,
            "orderChannel": 0,
            "deliveryType": 0
        }
        
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def get_order_detail(self, order_id: str) -> Dict[str, Any]:
        """
        Busca detalhes completos de um pedido.
        
        Args:
            order_id: ID do pedido
        
        Returns:
            Dict com detalhes do pedido
        """
        url = f"{self.base_url}/orders/detail"
        payload = {"orderId": order_id}
        
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def submit_appeal(
        self,
        order_id: str,
        apply_id: str,
        comments: str
    ) -> Dict[str, Any]:
        """
        Envia uma contestação de reembolso.
        
        Args:
            order_id: ID do pedido
            apply_id: ID da solicitação de reembolso
            comments: Texto de defesa gerado pela IA
        
        Returns:
            Dict com resposta da API
        """
        url = f"{self.base_url}/orders/appeal"
        payload = {
            "orderId": order_id,
            "applyId": apply_id,
            "comments": comments,
            "reasonId": "",
            "evidences": []
        }
        
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def close(self):
        """Fecha a conexão HTTP."""
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
