import keyword


class ColorizeMixin:
    colors = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34}

    def get_colored_text(self, text, color='yellow'):
        return f'\033[{self.colors[color]}m{text}\033[0m'


class ObjectDict:
    def __init__(self, data):
        for key, value in data.items():
            key = key + '_' if keyword.iskeyword(key) else key
            setattr(self, key, ObjectDict(value)
                    if isinstance(value, dict)
                    else value)


class Advert(ColorizeMixin):
    def __init__(self, data):
        if 'title' not in data:
            raise ValueError('Title нужен обязательно.')
        for key, value in data.items():
            key = key + "_" if keyword.iskeyword(key) else key
            setattr(self, key, ObjectDict(value)
                    if isinstance(value, dict)
                    else value)

    @property
    def price(self):
        return getattr(self, '_price', 0)

    @price.setter
    def price(self, new_price):
        self._validate_price(new_price)
        setattr(self, '_price', new_price)

    def _validate_price(self, price):
        if price < 0:
            raise ValueError('Цена должна быть >= 0')

    def __str__(self):
        full_text = f'{self.title} | {self.price} ₽'
        return self.get_colored_text(full_text, 'yellow')
