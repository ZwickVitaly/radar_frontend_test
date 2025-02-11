from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class ProductOutSchema(BaseModel):
    id: int = Field(description="Уникальный идентификатор продукта", examples=[1, 42, 999])
    name: str = Field(min_length=3, max_length=100, description="Название продукта", examples=["Смартфон X100", "Ноутбук Pro 15", "Умные часы Z"])
    description: Optional[str] = Field(None, max_length=1000, description="Описание продукта", examples=["Флагманский смартфон с OLED-дисплеем", "Мощный игровой ноутбук", "Стильные и удобные умные часы", None])
    price: float = Field(ge=0, description="Цена продукта в рублях", examples=[199.99, 999.50, 1499.00])
    discount_price: float = Field(ge=0, description="Цена продукта в рублях", examples=[199.99, 999.50, 1499.00])
    stock: int = Field(ge=0, description="Количество товара в наличии", examples=[10, 200, 0])
    category: str = Field(description="Категория товара", examples=["Электроника", "Одежда", "Бытовая техника"])
    created_at: datetime = Field(description="Дата добавления товара в каталог", examples=["2023-06-10", "2024-01-01"])
    updated_at: Optional[datetime] = Field(default=None, description="Дата последнего обновления информации о продукте", examples=["2024-02-01", None])
    brand: Optional[str] = Field(default=None, description="Бренд товара", examples=["Apple", "Samsung", "Sony", None])
    weight: Optional[float] = Field(default=None, ge=0, description="Вес продукта в килограммах", examples=[0.5, 1.2, 3.0, None])
    dimensions: Optional[str] = Field(default=None, description="Габариты товара (ДхШхВ) в см", examples=["10x5x2", "30x20x3", "50x40x10", None])
    color: Optional[str] = Field(default=None, description="Цвет продукта", examples=["Черный", "Белый", "Синий", None])
    rating: float = Field(default=0, ge=0, le=5, description="Средняя оценка продукта", examples=[4.5, 3.8, 5.0])
    reviews_count: int = Field(default=0, ge=0, description="Количество отзывов на продукт", examples=[100, 2500, 0])
    images: list[str] = Field(description="Список URL-адресов изображений продукта (ссылки относительные)", examples=[["/media/img1.jpg", "/media/img2.jpg"]])
    seller_id: int = Field(description="Идентификатор продавца", examples=[101, 202, 303])
    warranty_period: Optional[int] = Field(default=None, ge=0, description="Гарантийный срок в месяцах", examples=[12, 24, 36])
    return_policy: Optional[str] = Field(default=None, description="Условия возврата товара", examples=["14 дней на возврат", "Без возврата", None])
    barcode: str= Field( description="Штрихкод товара", examples=["1234567890123", "9876543210987"])

    class Config:
        from_attributes = True

class ProductListOutSchema(BaseModel):
    pages: int = Field(description="Общее количество страниц", examples=[1, 42, 999])
    current_page: int = Field(description="Текущая страница", examples=[1, 42, 999])
    limit: int = Field(description="Выбранный лимит", examples=[1, 5, 10])
    products: list[ProductOutSchema]


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, description="Уникальное имя пользователя", examples=["ivan_petrov", "john_doe", "superman42"])

class UserSignInSchema(UserBaseSchema):
    password: str = Field(min_length=8, description="Пароль пользователя", examples=["$2b$12$", "$argon2id$v=19$"])

class UserSignUpSchema(UserSignInSchema):
    full_name: Optional[str] = Field(default=None, description="Полное имя пользователя", examples=["Иван Петров", "John Doe", "Александр Сергеевич Пушкин"])

class UserOutSchema(UserBaseSchema):
    user_id: int = Field(ge=1, description="Уникальный идентификатор пользователя", examples=[1, 2, 45])
    created_at: date = Field(description="Дата регистрации пользователя в системе", examples=["2023-06-10", "2024-01-01"])
    full_name: Optional[str] = Field(default=None, description="Полное имя пользователя", examples=["Иван Петров", "John Doe", "Александр Сергеевич Пушкин"])
