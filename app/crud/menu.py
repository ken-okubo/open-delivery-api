from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.menu import Menu
from app.schemas.menu import MenuCreate, MenuSchema
from app.models.category import Category


async def get_all_menus(db: AsyncSession):
    result = await db.execute(
        select(Menu).options(selectinload(Menu.categories))
    )
    return result.scalars().all()


async def get_menu_by_id(menu_id: str, db: AsyncSession):
    result = await db.execute(
        select(Menu)
        .options(selectinload(Menu.categories))
        .where(Menu.id == menu_id)
    )
    menu = result.scalar_one_or_none()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu


async def create_menu(menu: MenuCreate, db: AsyncSession):
    from app.utils.serializers import make_json_serializable

    menu_data = menu.model_dump(by_alias=True)

    if menu_data.get("disclaimerURL"):
        menu_data["disclaimerURL"] = make_json_serializable(
            menu_data["disclaimerURL"]
        )

    category_ids = menu_data.pop("category_ids", [])

    db_menu = Menu(**menu_data)

    try:
        if category_ids:
            result = await db.execute(
                select(Category).where(Category.id.in_(category_ids))
            )
            db_menu.categories = result.scalars().all()

        db.add(db_menu)
        await db.commit()
        await db.refresh(db_menu, attribute_names=["categories"])

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="externalCode already exists"
        )
    except Exception:
        await db.rollback()
        raise

    return MenuSchema.model_validate(db_menu)


async def update_menu(menu_id: str, menu: MenuCreate, db: AsyncSession):
    result = await db.execute(select(Menu).where(Menu.id == menu_id))
    db_menu = result.scalar_one_or_none()

    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    try:
        for field, value in menu.model_dump(exclude_unset=True).items():
            if field == "category_ids":
                result = await db.execute(
                    select(Category).where(Category.id.in_(value))
                )
                db_menu.categories = result.scalars().all()
            else:
                setattr(db_menu, field, value)

        await db.commit()
        await db.refresh(db_menu, attribute_names=["categories"])

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="externalCode already exists"
        )
    except Exception:
        await db.rollback()
        raise

    return MenuSchema.model_validate(db_menu)


async def delete_menu(menu_id: str, db: AsyncSession):
    result = await db.execute(select(Menu).where(Menu.id == menu_id))
    db_menu = result.scalar_one_or_none()

    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    await db.delete(db_menu)
    await db.commit()
