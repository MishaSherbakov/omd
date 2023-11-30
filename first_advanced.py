import keyword


class ColorizeMixin:
    colors = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34}

    def get_colored_text(self, text, color='yellow'):
        """
        Возвращает строку с цветным текстом для вывода в консоли.

        :param text: Текст для окрашивания.
        :param color: Цвет текста.
        Допустимые значения: 'red', 'green', 'yellow', 'blue'.
        :return: Окрашенная строка текста.
        """
        return f'\033[{self.colors[color]}m{text}\033[0m'


class ObjectDict:
    def __init__(self, data):
        """
        Инициализирует объект типа ObjectDict из словаря.

        :param data: Словарь с данными для инициализации.
        """
        for key, value in data.items():
            key = key + '_' if keyword.iskeyword(key) else key
            setattr(self, key, ObjectDict(value)
                    if isinstance(value, dict)
                    else value)


class Advert(ColorizeMixin):
    def __init__(self, data):
        """
        Инициализирует объект типа Advert из словаря данных.

        :param data: Словарь с данными для инициализации.
          Обязателен ключ 'title'.
        :raise ValueError: Если ключ 'title' отсутствует в данных.
        """
        if 'title' not in data:
            raise ValueError('Title нужен обязательно.')
        for key, value in data.items():
            key = key + '_' if keyword.iskeyword(key) else key
            setattr(self, key, ObjectDict(value)
                    if isinstance(value, dict)
                    else value)

    @property
    def price(self):
        """
        Получает значение атрибута price объекта Advert.

        :return: Значение атрибута price.
        """
        return getattr(self, '_price', 0)

    @price.setter
    def price(self, new_price):
        """
        Устанавливает значение атрибута price объекта Advert.

        :param new_price: Новое значение для атрибута price.
        :raise ValueError: Если новое значение меньше 0.
        """
        self._validate_price(new_price)
        setattr(self, '_price', new_price)

    def _validate_price(self, price):
        """
        Проверяет, что цена не меньше 0.

        :param price: Значение цены для проверки.
        :raise ValueError: Если цена меньше 0.
        """
        if price < 0:
            raise ValueError('Цена должна быть >= 0')

    def __str__(self):
        """
        Возвращает строковое представление объекта Advert.

        :return: Строковое представление объявления с цветным текстом.
        """
        full_text = f'{self.title} | {self.price} ₽'
        return self.get_colored_text(full_text, 'yellow')
