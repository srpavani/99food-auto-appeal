"""
Gerenciamento de banco de dados JSON para controle de pedidos processados.
"""
import json
import os
from typing import Set, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class OrderDatabase:
    """Gerencia pedidos já processados em arquivo JSON."""
    
    def __init__(self, db_path: str = "data/processed_orders.json"):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Garante que o diretório e arquivo existem."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        if not os.path.exists(self.db_path):
            self._save_db({"processed_orders": {}, "stats": {"total_processed": 0}})
            logger.info(f"📁 Database criado em {self.db_path}")
    
    def _load_db(self) -> Dict[str, Any]:
        """Carrega o database do arquivo."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar database: {e}")
            return {"processed_orders": {}, "stats": {"total_processed": 0}}
    
    def _save_db(self, data: Dict[str, Any]):
        """Salva o database no arquivo."""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Erro ao salvar database: {e}")
    
    def is_processed(self, order_id: str, apply_id: str) -> bool:
        """
        Verifica se um pedido já foi processado.
        
        Args:
            order_id: ID do pedido
            apply_id: ID da solicitação de reembolso
        
        Returns:
            True se já foi processado, False caso contrário
        """
        db = self._load_db()
        key = f"{order_id}_{apply_id}"
        return key in db["processed_orders"]
    
    def mark_as_processed(
        self, 
        order_id: str, 
        apply_id: str,
        reason: str,
        defense: str,
        success: bool
    ):
        """
        Marca um pedido como processado.
        
        Args:
            order_id: ID do pedido
            apply_id: ID da solicitação de reembolso
            reason: Motivo da reclamação
            defense: Defesa gerada
            success: Se a contestação foi enviada com sucesso
        """
        db = self._load_db()
        key = f"{order_id}_{apply_id}"
        
        db["processed_orders"][key] = {
            "order_id": order_id,
            "apply_id": apply_id,
            "reason": reason,
            "defense": defense,
            "success": success,
            "processed_at": datetime.now().isoformat(),
            "timestamp": datetime.now().timestamp()
        }
        
        db["stats"]["total_processed"] = len(db["processed_orders"])
        
        self._save_db(db)
        logger.info(f"✅ Pedido {order_id} marcado como processado")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do database."""
        db = self._load_db()
        
        total = db["stats"]["total_processed"]
        successful = sum(1 for order in db["processed_orders"].values() if order["success"])
        failed = total - successful
        
        return {
            "total_processed": total,
            "successful": successful,
            "failed": failed,
            "last_processed": self._get_last_processed(db)
        }
    
    def _get_last_processed(self, db: Dict) -> str:
        """Retorna timestamp do último pedido processado."""
        if not db["processed_orders"]:
            return "Nenhum"
        
        orders = list(db["processed_orders"].values())
        orders.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return orders[0]["processed_at"]
    
    def get_processed_count_today(self) -> int:
        """Retorna quantidade de pedidos processados hoje."""
        db = self._load_db()
        today = datetime.now().date()
        
        count = 0
        for order in db["processed_orders"].values():
            order_date = datetime.fromisoformat(order["processed_at"]).date()
            if order_date == today:
                count += 1
        
        return count
