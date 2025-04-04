from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemSchema


def make_json_serializable(obj):
    if hasattr(obj, "__dict__"):  # Para objetos como HttpUrl
        return str(obj)
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(i) for i in obj]
    return obj


async def get_all_items(db: AsyncSession):
    result = await db.execute(select(Item))
    return [ItemSchema.model_validate(row) for row in result.scalars().all()]


async def get_item_by_id(item_id: str, db: AsyncSession):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemSchema.model_validate(item)


async def create_item(item: ItemCreate, db: AsyncSession):
    item_data = item.model_dump(by_alias=True)

    # Processa campos especiais que podem conter HttpUrl
    if item_data.get("image"):
        item_data["image"] = make_json_serializable(item_data["image"])

    if item_data.get("images"):
        item_data["images"] = make_json_serializable(item_data["images"])

    if item_data.get("nutritionalInfo"):
        item_data["nutritionalInfo"] = make_json_serializable(
            item_data["nutritionalInfo"]
        )

    db_item = Item(**item_data)
    db.add(db_item)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Item with this externalCode already exists",
        )

    await db.refresh(db_item)
    return ItemSchema.model_validate(db_item)


async def update_item(item_id: str, item: ItemCreate, db: AsyncSession):
    result = await db.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item.model_dump(exclude_unset=True)

    if "image" in update_data:
        update_data["image"] = make_json_serializable(update_data["image"])

    if "images" in update_data:
        update_data["images"] = make_json_serializable(update_data["images"])

    if "nutritionalInfo" in update_data:
        update_data["nutritionalInfo"] = make_json_serializable(
            update_data["nutritionalInfo"]
        )

    for field, value in update_data.items():
        setattr(db_item, field, value)

    await db.commit()
    await db.refresh(db_item)
    return ItemSchema.model_validate(db_item)


async def delete_item(item_id: str, db: AsyncSession):
    result = await db.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(db_item)
    await db.commit()
