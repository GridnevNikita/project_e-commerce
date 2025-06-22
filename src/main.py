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

    @classmethod
    def new_product(cls, data: dict) -> "Product":
        """Класс-метод, создающий объект Product из словаря."""
        return cls(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            quantity=data['quantity']
        )
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

    @property
    def products(self) -> str:
        """Возвращает все товары в формате строки"""
        lines = [
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            for product in self.__products
        ]
        return "\n".join(lines)


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
if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(category1.products)
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print(category1.products)
    print(category1.product_count)

    new_product = Product.new_product(
        {"name": "Samsung Galaxy S23 Ultra", "description": "256GB, Серый цвет, 200MP камера", "price": 180000.0,
         "quantity": 5})
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    new_product.price = 800
    print(new_product.price)

    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)