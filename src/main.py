import json
import os
from typing import Any, List


class Product:
    """Класс, представляющий товар"""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализирует объект Product"""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс, представляющий категорию товаров"""

    name: str
    description: str
    products: list[Product]
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        """Инициализирует объект Category и обновляет счётчики"""
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(self.__products) if self.__products else 0

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список"""
        self.__products.append(product)
        Category.product_count += 1

def read_json_file(path: str) -> List[dict[str, Any]]:
    """Читает JSON-файл по указанному пути и возвращает данные в виде списка словарей"""
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


def create_objects_from_json(data: List[dict[str, Any]]) -> List[Category]:
    """Преобразует список словарей из JSON в список объектов Category и Product"""
    categories_json = []
    for categories in data:
        products_json = []
        for products in categories["products"]:
            products_json.append(Product(**products))
        categories["products"] = products_json
        categories_json.append(Category(**categories))

    return categories_json


# if __name__ == "__main__":
# data_json = read_json_file("../data/products.json")
# objects = create_objects_from_json(data_json)
#
# for obj in objects:
#     print(obj.name)
#     print(obj.description)
#     print(len(obj.products))
#     print(obj.products)
#
#     for product in obj.products:
#         print(product.name)
#         print(product.description)
#         print(product.price)
#         print(product.quantity)
#
# print("Всего категорий:", Category.category_count)
# print("Всего товаров:", Category.product_count)
#
# product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
# product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
# product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
# print(product1.name)
# print(product1.description)
# print(product1.price)
# print(product1.quantity)
#
# print(product2.name)
# print(product2.description)
# print(product2.price)
# print(product2.quantity)
#
# print(product3.name)
# print(product3.description)
# print(product3.price)
# print(product3.quantity)
#
# category1 = Category("Смартфоны",
# "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#                      [product1, product2, product3])
#
# print(category1.name == "Смартфоны")
# print(category1.description)
# print(len(category1.products))
# print(category1.category_count)
# print(category1.product_count)
#
# product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
# category2 = Category("Телевизоры",
# "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
#                      [product4])
#
# print(category2.name)
# print(category2.description)
# print(len(category2.products))
# print(category2.products)
#
# print(Category.category_count)
# print(Category.product_count)
