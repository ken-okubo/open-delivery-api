from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.menu import MenuCreate, MenuResponse, MenuSchema
from app.crud import menu as menu_crud

router = APIRouter()


@router.get("/", response_model=list[MenuSchema])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await menu_crud.get_all_menus(db)


@router.get("/{menu_id}", response_model=MenuSchema)
async def get(menu_id: str, db: AsyncSession = Depends(get_db)):
    return await menu_crud.get_menu_by_id(menu_id, db)


@router.post("/", response_model=MenuSchema, status_code=201)
async def create(menu: MenuCreate, db: AsyncSession = Depends(get_db)):
    return await menu_crud.create_menu(menu, db)


@router.put("/{menu_id}", response_model=MenuResponse)
async def update(
    menu_id: str, menu: MenuCreate, db: AsyncSession = Depends(get_db)
):
    return await menu_crud.update_menu(menu_id, menu, db)


@router.delete("/{menu_id}", status_code=204)
async def delete(menu_id: str, db: AsyncSession = Depends(get_db)):
    await menu_crud.delete_menu(menu_id, db)
