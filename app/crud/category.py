from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategorySchema
from app.utils.serializers import make_json_serializable


async def get_all_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return [CategorySchema.model_validate(cat) for cat in categories]


async def get_category_by_id(category_id: str, db: AsyncSession):
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategorySchema.model_validate(category)


async def create_category(category: CategoryCreate, db: AsyncSession):
    category_data = category.model_dump(by_alias=True)

    if category_data.get("image"):
        category_data["image"] = make_json_serializable(category_data["image"])

    db_category = Category(**category_data)
    db.add(db_category)
    try:
        await db.commit()
        await db.refresh(db_category)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="externalCode already exists"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return CategorySchema.model_validate(db_category)


async def update_category(
    category_id: str, category: CategoryCreate, db: AsyncSession
):
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    db_category = result.scalar_one_or_none()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    try:
        update_data = category.model_dump(exclude_unset=True, by_alias=True)

        if "image" in update_data:
            update_data["image"] = make_json_serializable(update_data["image"])

        for field, value in update_data.items():
            setattr(db_category, field, value)

        await db.commit()
        await db.refresh(db_category)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="externalCode already exists"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return CategorySchema.model_validate(db_category)


async def delete_category(category_id: str, db: AsyncSession):
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    db_category = result.scalar_one_or_none()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.delete(db_category)
    await db.commit()
