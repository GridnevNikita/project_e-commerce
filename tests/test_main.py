import json
from unittest.mock import mock_open, patch

from main import Category, create_objects_from_json, read_json_file


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
    assert len(first_category.products) == 2

    assert first_category.category_count == 1
    assert first_category.product_count == 2


def test_create_objects_from_json(json_data):
    result = create_objects_from_json(json_data)

    assert isinstance(result, list)
    assert isinstance(result[0], Category)
    assert result[0].name == "Смартфоны"
    assert len(result[0].products) == 1
    assert result[0].products[0].name == "Iphone"


def test_read_json_file():
    mocked_json = '[{"name": "Смартфоны", "description": "Описание", "products": []}]'

    with patch("builtins.open", mock_open(read_data=mocked_json)):
        with patch("json.load", return_value=json.loads(mocked_json)) as mock_json_load:
            result = read_json_file("dummy_path.json")

    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert result[0]["name"] == "Смартфоны"
