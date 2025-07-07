import json
from unittest.mock import mock_open, patch

import pytest

from src.main import Category, CategoryIterator, Product, create_objects_from_json, read_json_file, \
    ProductZeroRaiseError, Order


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
    assert len(first_category.products)

    assert first_category.category_count == 1
    assert first_category.product_count == 2


def test_create_objects_from_json(json_data):
    result = create_objects_from_json(json_data)

    assert isinstance(result, list)
    assert isinstance(result[0], Category)
    assert result[0].name == "Смартфоны"
    assert len(result[0].products) == 1
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
    initial_len = len(first_category.products)

    new_product = Product("New Product", "Описание", 100.0, 10)
    first_category.add_product(new_product)

    assert len(first_category.products) == initial_len + 1
    assert Category.product_count == initial_count + 1
    assert any(p.name == "New Product" for p in first_category.products)


def test_product_str(first_product):
    assert str(first_product) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."


def test_category_str(first_category):
    assert str(first_category) == "Смартфоны, количество продуктов: 13 шт."


def test_product_add(first_product, second_product):
    result = first_product + second_product
    expected = first_product.price * first_product.quantity + second_product.price * second_product.quantity
    assert result == expected


def test_category_products_type(first_category):
    products = first_category.products
    assert isinstance(products, list)
    assert all(isinstance(p, Product) for p in products)


def test_category_iterator(first_category):
    iterator = CategoryIterator(first_category)
    products = list(iterator)

    assert len(products) == 2
    assert products[0].name == "Samsung Galaxy S23 Ultra"
    assert products[1].name == "Iphone 15"


def test_product_add_with_invalid_type(first_product):
    result = first_product.__add__("не продукт")
    assert result is NotImplemented


def test_smartphone_init(first_smartphone):
    assert first_smartphone.name == "Samsung Galaxy S23 Ultra"
    assert first_smartphone.description == "256GB, Серый цвет, 200MP камера"
    assert first_smartphone.price == 180000.0
    assert first_smartphone.quantity == 5
    assert first_smartphone.efficiency == 95.5
    assert first_smartphone.model == "S23 Ultra"
    assert first_smartphone.memory == 256
    assert first_smartphone.color == "Серый"


def test_lewngrass_init(first_lawngrass):
    assert first_lawngrass.name == "Газонная трава"
    assert first_lawngrass.description == "Элитная трава для газона"
    assert first_lawngrass.price == 500.0
    assert first_lawngrass.quantity == 20
    assert first_lawngrass.country == "Россия"
    assert first_lawngrass.germination_period == "7 дней"
    assert first_lawngrass.color == "Зеленый"


def test_smartphone_lawngrass_add(first_smartphone, first_lawngrass):
    with pytest.raises(TypeError):
        result = first_smartphone + first_lawngrass


def test_add_product_type_error(first_category):
    with pytest.raises(TypeError):
        result = first_category.add_product("не продукт")


def test_order_total_price(first_order):
    assert first_order.total_price == first_order.product.price * first_order.quantity


def test_order_str(first_order):
    assert str(first_order) == "Заказ: Samsung Galaxy S23 Ultra, количество: 3, сумма: 540000.0 руб."

def test_product_zero_quantity():
    with pytest.raises(ValueError):
        Product(
            name="Iphone 15",
            description="512GB, Gray space",
            price=210000.0,
            quantity=0,
        )

def test_product_zero_raise_error_init():
    error = ProductZeroRaiseError()
    assert str(error) == "Товар с нулевым количеством не может быть добавлен"

def test_order_zero_raise_error(first_product):
    with pytest.raises(ProductZeroRaiseError):
        Order(first_product, 0)

def test_middle_price(first_category):
    expected = (
        sum(product.price for product in first_category.products) / len(first_category.products)
    )
    assert first_category.middle_price() == expected
    empty_category = Category("Пустая", "Нет товаров", [])
    assert empty_category.middle_price() == 0

def test_add_product_zero_quantity(zero_list_products_category, capsys):
    product_zero = Product("Товар", "Описание", 100.0, 1)
    product_zero.quantity = 0
    zero_list_products_category.add_product(product_zero)

    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    assert lines[-2] == "Товар с нулевым количеством не может быть добавлен"
    assert lines[-1] == "Обработка добавления товара завершена"