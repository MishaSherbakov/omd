import pytest
import telegram
from unittest.mock import MagicMock
from telegram import Update
from super_ultra_mega_last import check_game_end, start, game, end, generate_keyboard, won

@pytest.fixture
def update():
    return MagicMock(spec=Update)


@pytest.fixture
def context():
    return MagicMock()


def test_won():
    assert won(['X', 'X', 'X', '.', 'O', 'O', '.', '.', '.']) is True
    assert won(['X', '.', 'O', 'X', '.', 'O', 'X', '.', 'O']) is True
    assert won(['X', 'O', '.', 'O', 'X', '.', 'O', 'X', '.']) is False


def test_generate_keyboard():
    state = [['X', '.', 'O'], ['.', 'X', 'O'], ['O', '.', 'X']]
    keyboard = generate_keyboard(state)
    assert len(keyboard) == 3
    assert len(keyboard[0]) == 3
    assert keyboard[0][0].text == 'X'
    assert keyboard[0][1].text == '.'
    assert keyboard[0][2].text == 'O'


@pytest.mark.asyncio
async def test_check_game_end(update, context):
    update.callback_query = MagicMock()
    update.callback_query.from_user.first_name = 'TestUser'
    context.user_data = {'keyboard_state': [['X', 'O', 'X'], ['O', 'X', 'O'], ['X', 'X', 'O']]}
    update.callback_query.answer = MagicMock()
    assert check_game_end(context.user_data['keyboard_state'], update.callback_query) is True


@pytest.mark.asyncio
async def test_check_game_end_draw(update, context):
    update.callback_query = MagicMock()
    context.user_data = {'keyboard_state': [['X', 'O', 'X'], ['O', 'X', 'X'], ['O', 'X', 'O']]}
    update.callback_query.answer = MagicMock()
    assert check_game_end(context.user_data['keyboard_state'], update.callback_query) is True
