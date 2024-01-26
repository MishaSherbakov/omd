import pytest
from unittest.mock import MagicMock
from telegram import Update
from FP_ADVANCED_NEW_LAST import start, game, end, generate_keyboard, won, check_game_end


@pytest.mark.asyncio
async def test_game(update, context):
    update.callback_query = MagicMock()
    update.callback_query.data = '00'
    context.user_data = {'keyboard_state': [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]}
    update.callback_query.edit_message_text = MagicMock()
    await game(update, context)
    update.callback_query.edit_message_text.assert_called_once()


def test_won():
    assert won(['X', 'X', 'X', '.', 'O', 'O', '.', '.', '.']) is True
    assert won(['X', '.', 'O', 'X', '.', 'O', 'X', '.', 'O']) is True
    assert won(['X', 'O', '.', 'O', 'X', '.', '.', 'O', 'X']) is False


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
    context.user_data = {'keyboard_state': [['X', 'O', 'O'], ['X', 'O', 'O'], ['X', 'X', 'X']]}
    update.callback_query.answer = MagicMock()
    assert await check_game_end(context.user_data['keyboard_state'], update.callback_query) is True
    update.callback_query.answer.assert_called_once_with('Congratulations! You won, TestUser!', show_alert=True)


@pytest.mark.asyncio
async def test_check_game_end_draw(update, context):
    update.callback_query = MagicMock()
    context.user_data = {'keyboard_state': [['X', 'O', 'X'], ['O', 'O', 'X'], ['X', 'X', 'O']]}
    update.callback_query.answer = MagicMock()
    assert await check_game_end(context.user_data['keyboard_state'], update.callback_query) is True
    update.callback_query.answer.assert_called_once_with('It\'s a draw!', show_alert=True)
