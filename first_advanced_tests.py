import json
import pytest
from first_advanced import Advert


def test_price_from_json():
    """
    Проверяет, что при создании экземпляра Advert
    из JSON-строки с отсутствующей ценой,
    атрибут price устанавливается в 0.
    """
    lesson_str = '{"title": "python"}'
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    assert lesson_ad.price == 0


def test_create_and_display_advert():
    """
    Проверяет, что создание и вывод объявления
    возвращает корректную строку с цветным текстом.
    """
    iphone_ad = Advert({'title': 'iPhone X', 'price': 100})
    assert str(iphone_ad) == "\033[33miPhone X | 100 ₽\033[0m"


def test_access_price_attribute():
    """
    Проверяет, что доступ к атрибуту price через
    точку возвращает корректное значение цены.
    """
    iphone_ad = Advert({'title': 'iPhone X', 'price': 100})
    assert iphone_ad.price == 100


def test_access_nested_attribute():
    """
    Проверяет, что доступ к вложенному атрибуту (title)
    через точку возвращает корректное значение.
    """
    iphone_ad = Advert({'title': 'iPhone X', 'price': 100})
    assert iphone_ad.title == 'iPhone X'


def test_access_nested_attribute_with_existing_data():
    """
    Проверяет, что доступ к вложенному атрибуту
    (location.address и class_)
    с существующими данными возвращает корректные значения.
    """
    corgi = Advert({'title': 'Вельш-корги', 'price': 1000, 'location':
                    {'address': 'Some Address'}, 'class_': 'dog'})
    assert corgi.location.address == 'Some Address'
    assert corgi.class_ == 'dog'


def test_display_colored_advert():
    """
    Проверяет, что вывод объявления в консоли с использованием
    цветного текста возвращает
    корректную строку с желтым цветом.
    """
    corgi = Advert({'title': 'Вельш-корги', 'price': 1000, 'location':
                    {'address': 'Some Address'}, 'class_': 'dog'})
    assert str(corgi) == '\033[33mВельш-корги | 1000 ₽\033[0m'


def test_missing_title():
    """
    Проверяет, что при создании экземпляра Advert
    без обязательного атрибута title
    выбрасывается исключение ValueError.
    """
    with pytest.raises(ValueError):
        Advert({'description': 'Some description', 'price': 50})


def test_negative_price():
    """
    Проверяет, что при создании экземпляра Advert с
    отрицательной ценой
    или при установке отрицательного значения атрибуту
    price, выбрасывается исключение ValueError.
    """
    with pytest.raises(ValueError):
        advert = Advert({'title': 'Test Ad', 'price': -10})
        advert.price
