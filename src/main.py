import json
import os
from typing import Any, List, Optional


class Product:
    """Класс, представляющий товар"""

    name: str
    description: str
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализирует объект Product"""
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Возвращает строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Возвращает общую стоимость двух товаров, учитывая цену и количество каждого."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, data: dict, products: Optional[List["Product"]] = None) -> "Product":
        """Создаёт новый товар или обновляет существующий с таким же именем."""
        if products is None:
            products = []

        for product in products:
            if product.name == data["name"]:
                product.quantity += data["quantity"]
                if data["price"] > product.price:
                    product.price = data["price"]
                return product
        return cls(name=data["name"], description=data["description"], price=data["price"], quantity=data["quantity"])

    @property
    def price(self) -> float:
        """Выводит цены"""
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Сеттер для ввода цены с проверкой"""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif value < self.__price:
            print(f"Вы пытаетесь понизить цену с {self.__price} до {value}.")
            confirm = input("Вы уверены? (y/n): ")
            if confirm.lower() == "y":
                self.__price = value
                print("Цена успешно обновлена.")
            else:
                print("Изменение цены отменено.")
        else:
            self.__price = value


class Category:
    """Класс, представляющий категорию товаров"""

    name: str
    description: str
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        """Инициализирует объект Category и обновляет счётчики"""
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(self.__products) if self.__products else 0

    def __str__(self) -> str:
        """Возвращает строковое представление категории с общим количеством товаров."""
        total_quantity = sum(prod.quantity for prod in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список"""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[Product]:
        """Возвращает все товары в формате list"""
        return self.__products


def read_json_file(path: str) -> List[dict[str, Any]]:
    """Читает JSON-файл по указанному пути и возвращает данные в виде списка словарей"""
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="UTF-8") as file:
        data: List[dict[str, Any]] = json.load(file)
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


class CategoryIterator:
    """Производит итерацию по товарам, которые хранятся в данной категории"""

    def __init__(self, category: Category) -> None:
        self.category = category
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Product:
        if self.index < len(self.category.products):
            result = self.category.products[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)

    iterator = CategoryIterator(category1)
    for product in iterator:
        print(product)
