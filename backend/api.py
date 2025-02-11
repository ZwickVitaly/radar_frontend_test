from typing import Optional

from fastapi import APIRouter, Response, Request
from fastapi.params import Body, Query
from sqlalchemy import select, func
from fastapi.responses import JSONResponse

from schemas import ProductListOutSchema
from db import async_session
from jwt_token import create_jwt_token, get_current_user
from schemas import UserSignInSchema, UserSignUpSchema, ProductOutSchema
from db_models import Product, User


router = APIRouter(prefix="/api")


@router.post("/sign_up")
async def sign_up(
    user_data: UserSignUpSchema = Body()
):
    """Эндпоинт для регистрации пользователя"""
    un = user_data.username.lower()

    async with async_session() as session:
        un_q = await session.execute(select(User.username).where(User.username == un))
        user_exists = un_q.scalar()
        if not user_exists:
            new_user = User(
                username=un,
                full_name=user_data.full_name,
                password=user_data.password,
            )
            session.add(new_user)
            await session.commit()
            return JSONResponse(status_code=200, content={"message": "Новый пользователь успешно создан!"})
        else:
            return JSONResponse(status_code=409, content={"message": "Пользователь с таким username уже существует."})


@router.post("/sign_in")
async def sign_in(
    response: Response, user_data: UserSignInSchema = Body()
):
    """Эндпоинт для входа в систему"""
    async with async_session() as session:
        user_q = await session.execute(select(User).where(
            User.username == user_data.username, User.password == user_data.password)
        )
        user = user_q.scalar()
    if not user:
        return JSONResponse(status_code=401, content={"message": "Неверное имя пользователя или пароль"})
    token = create_jwt_token(user.id)

    response.set_cookie(
        key="Authorization",
        value=f"Bearer {token}",
    )

    return {"message": "Пользователь успешно вошёл в систему"}

@router.post("/logout")
async def logout(response: Response, request: Request):
    """Эндпоинт для выхода из системы"""
    _ = get_current_user(request)

    response.delete_cookie("Authorization")

    return {"message": "Пользователь успешно вышел из системы"}

@router.get("/get_products", response_model=ProductListOutSchema)
async def get_products(
    request: Request,
    page: Optional[int] = Query(default=1, ge=1),
    limit: Optional[int] = Query(default=10, ge=1)
):
    """Эндпоинт для получения списка товаров"""
    _ = get_current_user(request)
    if limit not in [1, 5, 10]:
        return JSONResponse(status_code=422, content={"message": "Лимит товаров на странице может быть 1, 5 или 10"})
    async with async_session() as session:
        pages_q = await session.execute(select(func.count(Product.id)))
        p_q = pages_q.scalar()
        if not p_q:
            p_q = 0
        pages = (p_q // limit) + (1 if p_q % limit else 0)
        if page > pages:
            return JSONResponse(status_code=422,
                                content={"message": "Такой страницы нет"})
        products_q = await session.execute(select(Product).limit(limit).offset((page - 1) * limit).order_by(Product.id))
        products = products_q.scalars()
    return {
        "current_page": page,
        "pages": pages,
        "limit": limit,
        "products": [ProductOutSchema.model_validate(product) for product in products],
    }