from typing import Union
import hashlib
import random


class IdCounter:
    """Класс для счетчика id."""
    def __init__(self) -> None:
        self._id = 0

    def get_id(self) -> int:
        self._id += 1
        return self._id


class Password:
    """Класс для обработки пароля."""

    def get(self):
        """
        Получает и проверяет введенный пароль.
        :return: хэш-значение пароля
        """
        password = input("Введите пароль: ")
        if len(password) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        if not password.isalnum():
            raise ValueError("Пароль должен быть буквенно-цифровой строкой")
        return hashlib.sha256(password.encode()).hexdigest()

    def check(self) -> bool:
        """
        Проверяет соответствие введенного пароля имеющемуся хэш-значению.
        :return: True или False
        """
        password = input()
        return hashlib.sha256(password.encode()).hexdigest() == self.get()


class Product:
    """Класс, описывающий товар."""
    _id_pr_count = IdCounter()  # счетчик id товаров

    def __init__(self, name: str, price: Union[int, float], rating: Union[int, float]) -> None:
        self._id = self._id_pr_count.get_id()
        self._name = None
        self.price = price
        self.rating = rating
        self._init_name(name)

    def _init_name(self, name) -> None:
        if not isinstance(name, str):
            raise TypeError("Название товара должно быть типа str")
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price) -> None:
        if not isinstance(new_price, (int, float)):
            raise TypeError("Цена должна быть типа int или float")
        if not new_price > 0:
            raise ValueError("Цена должна быть больше 0")
        self._price = float(new_price)

    @property
    def rating(self) -> float:
        return self._rating

    @rating.setter
    def rating(self, new_rating) -> None:
        if not isinstance(new_rating, (int, float)):
            raise TypeError("Рейтинг должен быть типа int или float")
        if new_rating < 0:
            raise ValueError("Рейтинг не может быть меньше 0")
        self._rating = float(new_rating)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.price}, {self.rating})"

    def __str__(self) -> str:
        return f"{self.id!r}_{self.name!r}"


class Cart:
    """Класс, описывающий корзину покупателя."""
    def __init__(self) -> None:
        self._products_list = []

    @property
    def products_list(self) -> list:
        return self._products_list

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Добавляемый товар должен быть класса Product")
        self._products_list.append(product)

    def del_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Удаляемый товар должен быть класса Product")
        self._products_list.remove(product)


class User:
    """Класс, описывающий пользователя."""
    _id_us_count = IdCounter()  # счетчик id пользователей

    def __init__(self) -> None:
        self._id = self._id_us_count.get_id()
        self._cart = Cart()
        self._username = None
        self._init_username()
        self._password = Password().get()

    def _init_username(self) -> None:
        username = input("Введите Ваше имя: ")
        if not username.isalpha():
            raise ValueError("Необходимо ввести только свое имя")
        self._username = username

    @property
    def username(self) -> str:
        return self._username

    @property
    def id(self) -> int:
        return self._id

    @property
    def cart(self) -> list:
        return self._cart.products_list

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return f"{self.id!r}_{self.username!r}_'password1'"


class ProductFactory:
    """Класс, описывающий фабрику для создания товаров."""
    def create_product(self) -> Product:
        name = random.choice(('Аспирин', 'Парацетамол', 'Ибупрофен', 'Нимесулид', 'Диклофенак', 'Кетопрофен', 'Мелоксикам',
                              'Амиксин', 'Ингавирин', 'Гриппферон', 'Трикрезан', 'Эргоферон', 'Кагоцел', 'Циклоферон'))
        price = round(random.uniform(0.0, 100.0), 2)
        rating = round(random.uniform(0.0, 5.0), 2)
        return Product(name, price, rating)


class Store:
    """Класс, описывающий магазин."""
    def __init__(self) -> None:
        self._pf = ProductFactory()
        self._product_list = [self._pf.create_product() for _ in range(10)]
        self._user = User()
        self._ch_prod = None

    @property
    def product_list(self) -> list:
        return self._product_list

    def take_product(self) -> None:
        product = input("Введите желаемый продукт: ")
        for index, value in enumerate(self._product_list):
            if value.name == product:
                self._ch_prod = self._product_list.pop(index)
                self._user._cart.add_product(self._ch_prod)
                break
        self._ch_prod = None

    def return_product(self) -> None:
        product = input("Введите возвращаемый продукт: ")
        for index, value in enumerate(self._user._cart.products_list):
            if value.name == product:
                self._ch_prod = self._user._cart.products_list.pop(index)
                self._product_list.append(self._ch_prod)
                break
        self._ch_prod = None

    def user_cart(self) -> list:
        return self._user.cart


if __name__ == "__main__":
    store = Store()
    print(store.product_list)
    print(store.user_cart())
    store.take_product()
    print(store.product_list)
    print(store.user_cart())
    store.return_product()
    print(store.user_cart())
    print(store.product_list)
