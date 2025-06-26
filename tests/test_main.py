import json
from unittest.mock import mock_open, patch

from src.main import Category, Product, create_objects_from_json, read_json_file


def test_product_init(first_product, second_product):
    assert first_product.name == "Samsung Galaxy S23 Ultra"
    assert first_product.description == "256GB, Серый цвет, 200MP камера"
    assert first_product.price == 180000.0
    assert first_product.quantity == 5

    assert second_product.name == "Iphone 15"
    assert second_product.description == "512GB, Gray space"
    assert second_product.price == 210000.0
    assert second_product.quantity == 8


def test_category_init(first_category):
    assert first_category.name == "Смартфоны"
    assert (
        first_category.description
        == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    assert len(first_category.products.split("\n"))

    assert first_category.category_count == 1
    assert first_category.product_count == 2


def test_create_objects_from_json(json_data):
    result = create_objects_from_json(json_data)

    assert isinstance(result, list)
    assert isinstance(result[0], Category)
    assert result[0].name == "Смартфоны"
    assert len(result[0].products.split("\n")) == 1
    assert result[0]._Category__products[0].name == "Iphone"


def test_read_json_file():
    mocked_json = '[{"name": "Смартфоны", "description": "Описание", "products": []}]'

    with patch("builtins.open", mock_open(read_data=mocked_json)):
        with patch("json.load", return_value=json.loads(mocked_json)) as mock_json_load:
            result = read_json_file("dummy_path.json")

    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert result[0]["name"] == "Смартфоны"


def test_new_product_creates_object():
    data = {"name": "Xiaomi", "description": "Redmi Note 12", "price": 30000.0, "quantity": 10}
    product = Product.new_product(data)
    assert product.name == "Xiaomi"
    assert product.description == "Redmi Note 12"
    assert product.price == 30000.0
    assert product.quantity == 10


def test_new_product_if_duplicate(first_product):
    data = {"name": "Samsung Galaxy S23 Ultra", "description": "Обновлённая версия", "price": 190000.0, "quantity": 2}
    result = Product.new_product(data, [first_product])
    assert result is first_product
    assert result.quantity == 7
    assert result.price == 190000.0


def test_price_negative(first_product):
    """Цена не должна устанавливаться, если <= 0"""
    first_product.price = -1000.0
    assert first_product.price == 180000.0


@patch("builtins.input", return_value="n")
def test_price_lowering_rejected(mock_input, first_product):
    """Пользователь отказался снижать цену — цена не меняется"""
    first_product.price = 150000.0
    assert first_product.price == 180000.0


@patch("builtins.input", return_value="y")
def test_price_lowering_accepted(mock_input, first_product):
    """Пользователь подтвердил снижение цены — цена обновляется"""
    first_product.price = 150000.0
    assert first_product.price == 150000.0


def test_add_product_increases_list_and_count(first_category):
    initial_count = Category.product_count
    initial_len = len(first_category.products.split("\n"))

    new_product = Product("New Product", "Описание", 100.0, 10)
    first_category.add_product(new_product)

    assert len(first_category.products.split("\n")) == initial_len + 1
    assert Category.product_count == initial_count + 1
    assert "New Product" in first_category.products
