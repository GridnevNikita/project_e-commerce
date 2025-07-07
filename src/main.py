import json
import os
from abc import ABC, abstractmethod
from typing import Any, List, Optional


class ProductZeroRaiseError(Exception):
    """Исключение для товаров с нулевым количеством."""

    def __init__(self, message: str = "Товар с нулевым количеством не может быть добавлен"):
        super().__init__(message)


class BaseCategory(ABC):
    """Абстрактный базовый класс для категории и заказа."""

    @abstractmethod
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def __str__(self) -> str:
        """Вернуть строковое представление продукта."""
        pass


class BaseProduct(ABC):
    """Абстрактный базовый класс для продукта."""

    @abstractmethod
    def __str__(self) -> str:
        """Вернуть строковое представление продукта."""
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, *args: Any, **kwargs: Any) -> Any:
        """Создать новый продукт или обновить существующий."""
        pass


class PrintMixin:
    """Миксин для вывода информации о создании объекта."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Инициализация миксина"""
        super().__init__(*args, **kwargs)
        print(f"Создан объект: {repr(self)}")

    def __repr__(self) -> str:
        """
        Формат: ClassName('name', 'description', price, quantity)
        """
        return f"{self.__class__.__name__}('{self.name}', '{self.description}', {self.price}, {self.quantity})"


class Product(PrintMixin, BaseProduct):
    """Класс, представляющий товар"""

    name: str
    description: str
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализирует объект Product"""
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__()

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


class Category(BaseCategory):
    """Класс, представляющий категорию товаров"""

    name: str
    description: str
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        """Инициализирует объект Category и обновляет счётчики"""
        super().__init__(name)
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
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product")

        try:
            if product.quantity == 0:
                raise ProductZeroRaiseError()
        except ProductZeroRaiseError as e:
            print(e)
        else:
            self.__products.append(product)
            Category.product_count += 1
            print("Товар успешно добавлен")
        finally:
            print("Обработка добавления товара завершена")

    @property
    def products(self) -> List[Product]:
        """Возвращает все товары в формате list"""
        return self.__products

    def middle_price(self) -> float:
        """
        Вычисляет среднюю цену товаров категории.
        Если товаров нет, возвращает 0.
        """
        try:
            return sum([product.price for product in self.products]) / len(self.products)

        except ZeroDivisionError:
            return 0


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


class Order(BaseCategory):
    def __init__(self, product: Product, quantity: int):
        """Инициализация заказа"""
        if quantity == 0:
            raise ProductZeroRaiseError()
        super().__init__(product.name)
        self.product = product
        self.quantity = quantity
        self.total_price = self.product.price * self.quantity

    def __str__(self) -> str:
        """Возвращает строковое представление заказа."""
        return f"Заказ: {self.product.name}, количество: {self.quantity}, сумма: {self.total_price} руб."


if __name__ == '__main__':
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())

    try:
        order = Order(product1, 0)
    except ProductZeroRaiseError as e:
        print(e)
    else:
        print("Заказ успешно создан")
    finally:
        print("Обработка добавления заказа завершена")
