# app/crud/order.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app.schemas.order import OrderCreateSchema
from app.models.order import (
    Order,
    OrderItem,
    OrderCustomer,
    OrderDelivery,
    OrderStatus,
)


async def get_order_by_id(order_id: str, db: AsyncSession):
    result = await db.execute(
        select(Order)
        .options(
            selectinload(Order.items),
            selectinload(Order.customer),
            selectinload(Order.delivery),
        )
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


async def get_all_orders(db: AsyncSession):
    result = await db.execute(select(Order.id))
    order_ids = [row[0] for row in result.all()]

    orders = []
    for order_id in order_ids:
        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.items),
                selectinload(Order.customer),
                selectinload(Order.delivery)
            )
            .where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()
        if order:
            orders.append(order)

    return orders


async def update_order_status(order_id: str, status: str, db: AsyncSession):
    order = await get_order_by_id(order_id, db)

    # Lógica de validação de mudança de status
    current_status = order.status.value
    if (
        current_status == OrderStatus.CREATED.value
        and status == OrderStatus.CONFIRMED.value
    ):
        order.status = OrderStatus(status)
    elif (
        current_status == OrderStatus.CONFIRMED.value
        and status == OrderStatus.DISPATCHED.value
    ):
        order.status = OrderStatus(status)
    elif (
        current_status == OrderStatus.DISPATCHED.value
        and status == OrderStatus.DELIVERED.value
    ):
        order.status = OrderStatus(status)
    else:
        raise HTTPException(
            status_code=422,
            detail=f"Cannot change status from {current_status} to {status}",
        )

    await db.commit()
    await db.refresh(order)
    return {"message": f"Order status updated to {status}"}


async def create_order(order_data: OrderCreateSchema, db: AsyncSession):
    # Criar o pedido principal
    db_order = Order(
        display_id=order_data.display_id,
        type=order_data.type,
        status=OrderStatus.CREATED,
        total_amount=order_data.total_amount,
    )
    db.add(db_order)
    await db.flush()  # Para obter o ID gerado

    # Criar o cliente
    customer_data = order_data.customer
    db_customer = OrderCustomer(
        order_id=db_order.id,
        name=customer_data.name,
        phone=customer_data.phone,
        email=customer_data.email,
    )
    db.add(db_customer)

    # Criar entrega
    delivery_data = order_data.delivery
    db_delivery = OrderDelivery(
        order_id=db_order.id,
        address=delivery_data.address.dict(),
        estimated_time=delivery_data.estimated_time,
    )
    db.add(db_delivery)

    # Criar itens
    for item_data in order_data.items:
        db_item = OrderItem(
            order_id=db_order.id,
            item_id=item_data.item_id,
            name=item_data.name,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
        )
        db.add(db_item)

    await db.commit()
    await db.refresh(db_order)

    # Carregando relações para o retorno
    result = await db.execute(
        select(Order)
        .options(
            selectinload(Order.items),
            selectinload(Order.customer),
            selectinload(Order.delivery),
        )
        .where(Order.id == db_order.id)
    )
    return result.scalar_one()
