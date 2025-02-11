import random
from datetime import datetime

from sqlalchemy import select, func

from db import async_session
from db_models import Product

CATEGORIES = ["Electronics", "Computers", "Audio", "Home Appliances", "Accessories", "Sports", "Fashion"]
BRANDS = ["TechCorp", "GameTech", "SoundMax", "VisionTech", "BassBoom", "SmartWear", "FitGear"]
COLORS = ["Black", "White", "Gray", "Blue", "Red", "Green", "Silver"]
DESCRIPTIONS = ["High-quality product", "Best in class", "Top-rated item", "Customer favorite", "Advanced features"]
RETURN_POLICIES = ["30-day return", "14-day return", "No return", "60-day return"]

async def create_products():
    print("Генерируются товары")
    async with async_session() as session:
        q = await session.execute(select(func.count(Product.id)))
        c = q.scalar()
        if c and c >= 45:
            print("Товары уже есть")
            return
        products = []
        for i in range(1, 46):
            price = round(random.uniform(10, 1000), 2)
            discount_price = price * 0.8
            new_product = Product(
                name=f"Product {i}",
                description=random.choice(DESCRIPTIONS),
                price=price,
                discount_price=round(discount_price, 2),
                stock=random.randint(1, 200),
                category=random.choice(CATEGORIES),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                brand=random.choice(BRANDS),
                weight=round(random.uniform(0.1, 5.0), 2),
                dimensions="100x100x50 mm",
                color=random.choice(COLORS),
                rating=round(random.uniform(0, 5), 1),
                reviews_count=random.randint(0, 500),
                images=[],  # Заполним после вставки
                seller_id=random.randint(1, 10),
                warranty_period=random.randint(0, 36),
                return_policy=random.choice(RETURN_POLICIES),
                barcode=str(random.randint(1000000000000, 9999999999999))
            )
            products.append(new_product)

        session.add_all(products)
        await session.commit()

        for product in products:
            product.images = [f"/media/{product.id}.jpg"]

        await session.commit()