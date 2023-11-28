import click
from random import randint
from typing import List


def log(template: str):
    """
    Декоратор, чтобы подставлять времея выполнения функции в ф-строку

    """

    def function_time(func):
        """
        Обертка для функции, добавляющая логирование времени выполнения.

        """

        def wrapper(*args, **kwargs):
            """
            Внутренняя обертка с логированием времени выполнения.

            """
            # Вывод названия и времени функции
            print(f'Название функции: {func.__name__}. '
                  f'Время: {template.format(randint(30, 50))}')
            return func(*args, **kwargs)

        return wrapper

    return function_time


class Pizza:
    """
    Класс Pizza - это базовый класс для создания пиццы.

    Attributes:
        size (str): Размер пиццы ('L' по умолчанию).
        ingredients (List[str]): Список ингредиентов пиццы.

    """

    def __init__(self, size: str = 'L'):
        """
        Инициализатор объекта Pizza.

        Args:
            size (str, optional): Размер пиццы ('L' по умолчанию).

        """
        self.size = size
        self.ingredients: List[str] = []

    def add_ingredient(self, ingredient: str):
        """
        Добавление ингредиента к пицце.

        Args:
            ingredient (str): Название ингредиента.

        """
        self.ingredients.append(ingredient)

    @log('🗿Приготовили за : {} минут')
    def cook(self):
        """
        Приготовление пиццы.

        """
        pass

    @log('🛵Доставили за : {} минут')
    def deliver(self):
        """
        Доставка пиццы.

        """
        pass

    def show_ingredients(self) -> str:
        """
        Отображение меню пиццы.

        Returns:
            str: Строка, представляющая меню пиццы.

        """
        return f"{self.__class__.__name__} : {', '.join(self.ingredients)}"


class Margherita(Pizza):
    """
    Класс Margherita представляет пиццу "Маргарита".

    Attributes:
        size (str): Размер пиццы ('L' по умолчанию).

    """

    def __init__(self, size: str = 'L'):
        """
        Инициализатор объекта Margherita.

        Args:
            size (str, optional): Размер пиццы ('L' по умолчанию).

        """
        super().__init__(size)
        self.add_ingredient('tomato sauce')
        self.add_ingredient('mozzarella')
        self.add_ingredient('tomatoes')


class Pepperoni(Pizza):
    """
    Класс Pepperoni представляет пиццу "Пепперони".

    Attributes:
        size (str): Размер пиццы ('L' по умолчанию).

    """

    def __init__(self, size: str = 'L'):
        """
        Инициализатор объекта Pepperoni.

        Args:
            size (str, optional): Размер пиццы ('L' по умолчанию).

        """
        super().__init__(size)
        self.add_ingredient('tomato sauce')
        self.add_ingredient('mozzarella')
        self.add_ingredient('pepperoni')


class Hawaiian(Pizza):
    """
    Класс Hawaiian представляет пиццу "Гавайская".

    Attributes:
        size (str): Размер пиццы ('L' по умолчанию).

    """

    def __init__(self, size: str = 'L'):
        """
        Инициализатор объекта Hawaiian.

        Args:
            size (str, optional): Размер пиццы ('L' по умолчанию).

        """
        super().__init__(size)
        self.add_ingredient('tomato sauce')
        self.add_ingredient('mozzarella')
        self.add_ingredient('chicken')
        self.add_ingredient('pineapples')


@click.group()
def cli():
    """
    Группа команд для управления заказами пиццы.

    """


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.option('--size', type=click.Choice(['L', 'XL']),
              default='L', help='Размер пиццы')
@click.argument('pizza_name', nargs=1)
def order(pizza_name: str, size: str, delivery: bool):
    """
    Размещение заказа на пиццу.

    Args:
        pizza_name (str): Название выбранной пиццы.
        size (str): Размер пиццы ('L' по умолчанию).
        delivery (bool): Флаг для указания доставки.

    """
    if pizza_name not in ['margherita', 'pepperoni', 'hawaiian']:
        print('Нет в меню')
        return
    
    pizza = None
    if pizza_name == 'margherita':
        pizza = Margherita(size)
    elif pizza_name == 'pepperoni':
        pizza = Pepperoni(size)
    elif pizza_name == 'hawaiian':
        pizza = Hawaiian(size)


    pizza.cook()

    if delivery:
        pizza.deliver()


@cli.command()
def menu():
    """
    Отображение меню.

    """
    margherita = Margherita()
    pepperoni = Pepperoni()
    hawaiian = Hawaiian()

    print('🧀' + margherita.show_ingredients())
    print('🍅' + pepperoni.show_ingredients())
    print('🍍' + hawaiian.show_ingredients())


if __name__ == '__main__':
    cli()
