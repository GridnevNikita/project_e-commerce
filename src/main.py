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
        if type(self) is not type(other):
            raise TypeError
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


class Smartphone(Product):
    """Класс, представляющий товар «Смартфон»"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        """Инициализирует объект Smartphone"""
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс, представляющий товар «Трава газонная»"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        """Инициализирует объект Smartphone"""
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError

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


# if __name__ == '__main__':
#     smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
#                          "S23 Ultra", 256, "Серый")
#     smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
#     smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")
#
#     print(smartphone1.name)
#     print(smartphone1.description)
#     print(smartphone1.price)
#     print(smartphone1.quantity)
#     print(smartphone1.efficiency)
#     print(smartphone1.model)
#     print(smartphone1.memory)
#     print(smartphone1.color)
#
#     print(smartphone2.name)
#     print(smartphone2.description)
#     print(smartphone2.price)
#     print(smartphone2.quantity)
#     print(smartphone2.efficiency)
#     print(smartphone2.model)
#     print(smartphone2.memory)
#     print(smartphone2.color)
#
#     print(smartphone3.name)
#     print(smartphone3.description)
#     print(smartphone3.price)
#     print(smartphone3.quantity)
#     print(smartphone3.efficiency)
#     print(smartphone3.model)
#     print(smartphone3.memory)
#     print(smartphone3.color)
#
#     grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
#     grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")
#
#     print(grass1.name)
#     print(grass1.description)
#     print(grass1.price)
#     print(grass1.quantity)
#     print(grass1.country)
#     print(grass1.germination_period)
#     print(grass1.color)
#
#     print(grass2.name)
#     print(grass2.description)
#     print(grass2.price)
#     print(grass2.quantity)
#     print(grass2.country)
#     print(grass2.germination_period)
#     print(grass2.color)
#
#     smartphone_sum = smartphone1 + smartphone2
#     print(smartphone_sum)
#
#     grass_sum = grass1 + grass2
#     print(grass_sum)
#
#     try:
#         invalid_sum = smartphone1 + grass1
#     except TypeError:
#         print("Возникла ошибка TypeError при попытке сложения")
#     else:
#         print("Не возникла ошибка TypeError при попытке сложения")
#
#     category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
#     category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])
#
#     category_smartphones.add_product(smartphone3)
#
#     print(category_smartphones.products)
#
#     print(Category.product_count)
#
#     try:
#         category_smartphones.add_product("Not a product")
#     except TypeError:
#         print("Возникла ошибка TypeError при добавлении не продукта")
#     else:
#         print("Не возникла ошибка TypeError при добавлении не продукта")
