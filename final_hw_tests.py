from click.testing import CliRunner
from final_hw import order, menu


def test_order_without_delivery():
    """
    order без доставки
    """
    runner = CliRunner()
    result = runner.invoke(order, ['pepperoni'])
    assert result.exit_code == 0
    assert 'Приготовили за' in result.output


def test_order_with_delivery():
    """
    order с доставкой
    """
    runner = CliRunner()
    result = runner.invoke(order, ['margherita', '--delivery'])
    assert result.exit_code == 0
    assert 'Приготовили за' in result.output
    assert 'Доставили за' in result.output


def test_order_invalid_pizza_type():
    """
    Неправильное название пиццы(Pepperoni в таком случае)
    """
    runner = CliRunner()
    result = runner.invoke(order, ['invalid_argument'])
    assert result.exit_code == 0
    assert 'Приготовили за' in result.output


def test_order_invalid_size_argument():
    """
    Неправильный размер пиццы(только XL,L)
    """
    runner = CliRunner()
    result = runner.invoke(order,
                           ['margherita', '--size', 'invalid_argument'])
    assert result.exit_code != 0
    assert "Error: Invalid value for '--size'" in result.output


def test_order_invalid_flag():
    """
    Неправильный флаг
    """
    runner = CliRunner()
    result = runner.invoke(order, ['pepperoni', '--invalid'])
    assert result.exit_code != 0
    assert 'Error: No such option: --invalid' in result.output


def test_order_invalid_full():
    """
    Заказ со всеми флагами
    """
    runner = CliRunner()
    result = runner.invoke(order, ['hawaiian', '--delivery', '--size', 'XL'])
    assert result.exit_code == 0
    assert 'Приготовили за' in result.output
    assert 'Доставили за' in result.output


def test_menu():
    """
    Тестим меню
    """
    runner = CliRunner()
    result = runner.invoke(menu)
    assert result.exit_code == 0
    assert '🧀Margherita : tomato sauce, mozzarella, tomatoes' in result.output
    assert '🍅Pepperoni : tomato sauce, mozzarella, pepperoni' in result.output
    assert '🍍Hawaiian : tomato sauce, mozzarella, chicken, pineapples' \
           in result.output
