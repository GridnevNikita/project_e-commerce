import pytest
from src.main import Category, Product


@pytest.fixture(autouse=True)
def reset_counters():
    """Сброс глобальных счётчиков перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def first_product():
    return Product(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.0,
        quantity=5,
    )


@pytest.fixture
def second_product():
    return Product(
        name="Iphone 15",
        description="512GB, Gray space",
        price=210000.0,
        quantity=8,
    )


@pytest.fixture
def first_category(first_product, second_product):
    return Category(
        name="Смартфоны",
        description="Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        products=[first_product, second_product],
    )


@pytest.fixture
def json_data():
    return [
        {
            "name": "Смартфоны",
            "description": "Описание категории",
            "products": [
                {
                    "name": "Iphone",
                    "description": "512GB",
                    "price": 200000.0,
                    "quantity": 3,
                }
            ],
        }
    ]