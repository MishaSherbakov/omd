from copy import deepcopy
import logging
import os
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler
)

# Включение логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# Установка более высокого уровня логгирования для httpx, чтобы избежать логгирования всех GET
# и POST-запросов
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Получение токена через BotFather
TOKEN = os.getenv('TG_TOKEN')

CONTINUE_GAME, FINISH_GAME = range(2)

SPACE = '.'
CROSS = 'X'
ZERO = 'O'

DEFAULT_STATE = [[SPACE for _ in range(3)] for _ in range(3)]


def get_default_state():
    """Вспомогательная функция для получения начального состояния игры"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """Генерация клавиатуры крестики-нолики 3x3 (кнопки телеграма)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отправка сообщения по `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'Х (ваш) ход! Пожалуйста, '
                                    f'поставьте Х на '
                                    f'свободное место', reply_markup=reply_markup)
    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Основная обработка игры"""
    query = update.callback_query
    user = query.from_user
    choice = query.data

    row, col = int(choice[0]), int(choice[1])
    keyboard_state = context.user_data['keyboard_state']

    # Проверка, что выбранная ячейка свободна
    if keyboard_state[row][col] == SPACE:
        # Обновление состояния игры ходом пользователя
        keyboard_state[row][col] = CROSS

        # Проверка, выиграл ли пользователь
        if check_game_end(keyboard_state, query):
            return await end(update, context)

        # Ход противника (простое ИИ: размещение 'O' случайным образом в свободной ячейке)
        empty_cells = [(r, c) for r in range(3) for c in range(3) if keyboard_state[r][c] == SPACE]
        if empty_cells:
            opp_choice = random.choice(empty_cells)
            keyboard_state[opp_choice[0]][opp_choice[1]] = ZERO

            # Проверка, выиграл ли противник
            if check_game_end(keyboard_state, query):
                return await end(update, context)

        # Обновление клавиатуры
        keyboard = generate_keyboard(keyboard_state)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f'Х (ваш) ход! Пожалуйста, поставьте Х на свободное место', reply_markup=reply_markup)

        return CONTINUE_GAME
    else:
        # Ячейка уже занята, попросить пользователя выбрать снова
        await query.answer('Эта ячейка уже занята. Пожалуйста, выберите свободную ячейку.')
        return CONTINUE_GAME


def check_game_end(keyboard_state: list[list[str]], query: CallbackQuery) -> bool:
    """Проверка, завершена ли игра (победа или ничья)"""
    user = query.from_user

    # Проверка, выиграл ли кто-то
    if won([keyboard_state[r][c] for r in range(3) for c in range(3)]):
        return True
    elif all(keyboard_state[r][c] != SPACE for r in range(3) for c in range(3)):
        # Проверка, является ли игра ничьей
        return True

    return False


def won(fields: list[str]) -> bool:
    """Проверка, выиграли ли крестики или нолики"""
    # Проверка строк, столбцов и диагоналей на победу
    for i in range(3):
        if fields[i * 3] == fields[i * 3 + 1] == fields[i * 3 + 2] != SPACE:  # Проверка строк
            return True
        if fields[i] == fields[i + 3] == fields[i + 6] != SPACE:  # Проверка столбцов
            return True
    if fields[0] == fields[4] == fields[8] != SPACE or fields[2] == fields[4] == fields[6] != SPACE:  # Проверка диагоналей
        return True
    return False


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возвращает `ConversationHandler.END`, что говорит
    ConversationHandler, что беседа завершена.
    """
    # сбросить состояние в значения по умолчанию, чтобы можно было сыграть еще раз с /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END


def main() -> None:
    """Запуск бота"""
    # Создание приложения и передача ему токена вашего бота.
    application = Application.builder().token(TOKEN).build()

    # Настройка обработчика разговора с состояниями CONTINUE_GAME и FINISH_GAME
    # Используйте параметр pattern для передачи CallbackQueries с определенным
    # шаблоном данных соответствующим обработчикам.
    # ^ означает "начало строки"
    # $ означает "конец строки"
    # Таким образом, ^ABC$ разрешит только 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Добавление обработчика разговора в приложение, который будет использоваться для обработки обновлений
    application.add_handler(conv_handler)

    # Запуск бота до тех пор, пока пользователь не нажмет Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
