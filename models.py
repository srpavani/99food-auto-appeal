"""
Modelos Pydantic para tipar as respostas da API 99Food.
"""
from typing import List, Optional, Any
from pydantic import BaseModel, Field


# ==================== REFUND LIST MODELS ====================

class RefundTag(BaseModel):
    """Tag de status do reembolso."""
    text: str
    style: int


class RefundInfo(BaseModel):
    """Informações de reembolso no listing."""
    status: int
    displayText: str
    applyId: int
    applyCreateTime: int
    tagList: List[RefundTag]


class OrderItem(BaseModel):
    """Item de pedido na listagem."""
    orderId: str
    refundInfo: Optional[RefundInfo] = None


class RefundListData(BaseModel):
    """Dados da listagem de reembolsos."""
    total: int
    totalPage: int
    orderList: List[OrderItem]


class RefundListResponse(BaseModel):
    """Resposta completa da API de listagem."""
    success: bool
    data: dict
    status: int


# ==================== ORDER DETAIL MODELS ====================

class ApplyReasonInfo(BaseModel):
    """Motivo da solicitação de reembolso."""
    reason: str
    img: List[str] = Field(default_factory=list)
    reasonTag: str
    subReasonTag: str = ""


class ApplyItem(BaseModel):
    """Item aplicado para reembolso."""
    name: str
    count: int
    amount: str
    afterTags: List[str] = Field(default_factory=list)


class RefundDetail(BaseModel):
    """Detalhes completos do reembolso."""
    applyId: str
    applyReasonInfo: ApplyReasonInfo
    applyRefundTs: int
    applyItems: List[ApplyItem]
    showAppealButton: bool = False
    canAppeal: bool = False


class OrderDetailData(BaseModel):
    """Dados detalhados do pedido."""
    orderId: str
    orderIndex: int
    displayNum: str
    refundDetailList: Optional[List[RefundDetail]] = Field(default_factory=list)


class OrderDetailResponse(BaseModel):
    """Resposta completa da API de detalhes."""
    success: bool
    data: dict
    status: int


# ==================== APPEAL MODELS ====================

class AppealRequest(BaseModel):
    """Payload para enviar contestação."""
    orderId: str
    applyId: str
    comments: str
    reasonId: str = ""
    evidences: List[str] = Field(default_factory=list)


class AppealResponse(BaseModel):
    """Resposta da API de contestação."""
    success: bool
    data: Optional[dict] = None
    status: int
