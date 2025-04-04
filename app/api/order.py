from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.order import OrderCreateSchema
from app.db.database import get_db
from app.schemas.order import OrderSchema
from app.crud import order as order_crud
from uuid import UUID
from typing import List

router = APIRouter()


@router.get("/", response_model=List[OrderSchema])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    """Obter todos os pedidos"""
    return await order_crud.get_all_orders(db)


@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Obter detalhes de um pedido específico"""
    return await order_crud.get_order_by_id(str(order_id), db)


@router.post("/{order_id}/confirm", status_code=202)
async def confirm_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Confirmar pedido"""
    return await order_crud.update_order_status(str(order_id), "CONFIRMED", db)


@router.post("/{order_id}/dispatch", status_code=202)
async def dispatch_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Despachar pedido para entrega"""
    return await order_crud.update_order_status(
        str(order_id), "DISPATCHED", db
    )


@router.post("/{order_id}/delivered", status_code=202)
async def deliver_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Marcar pedido como entregue"""
    return await order_crud.update_order_status(str(order_id), "DELIVERED", db)


@router.post("/", response_model=OrderSchema, status_code=201)
async def create_order(
    order: OrderCreateSchema, db: AsyncSession = Depends(get_db)
):
    return await order_crud.create_order(order, db)
