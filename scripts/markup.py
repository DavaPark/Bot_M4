from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton)


main_regicter_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Реєстрація', callback_data='register')],
    [InlineKeyboardButton(text='Відгуки', url='https://t.me/hotlinebrius_bot')],
    [InlineKeyboardButton(text='Програма', callback_data='program')],
    [InlineKeyboardButton(text='Навіщо тобі М4 Реді', callback_data='why_need')],
    [InlineKeyboardButton(text='Сайт', url='https://t.me/hotlinebrius_bot')],
    [InlineKeyboardButton(text='Телеграм канал М4 Реді', url='https://t.me/hotlinebrius_bot')],
    [InlineKeyboardButton(text='Підтримка', url='https://t.me/hotlinebrius_bot')]
])


register_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📜Прочитати умови', callback_data='read_conditions')],
    [InlineKeyboardButton(text='✅Прийняти умови', callback_data='accept')],
    [InlineKeyboardButton(text='Назад 🔙', callback_data='go_back_register')]

])


register_accept_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Прийняти умови', callback_data='accept')]
])


accept_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проходження форми', callback_data='form')],
    [InlineKeyboardButton(text='Назад 🔙', callback_data='go_back_accept')]
])


form_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Google Forms', callback_data='Google Forms')],
    [InlineKeyboardButton(text='✅Я заповнив/ла анкету', callback_data='pay')],
    [InlineKeyboardButton(text='Назад 🔙', callback_data='go_back_form')]
])


program_go_back_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅Назад', callback_data='program_go_back')]
])


pay_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💳Сплатити', callback_data='to_pay')]
])


menu_buttons_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Навчання 📚"), KeyboardButton(text="Стань частиною М4")],
        [KeyboardButton(text="Спільнота"), KeyboardButton(text="Питання-відповіді")],
        [KeyboardButton(text="Корисне"), KeyboardButton(text="Підтримка")],
    ],
    resize_keyboard=True
)

back_buttons_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Назад 🔙")]
    ],
    resize_keyboard=True
)


# Меню модулей
modules_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Як навчатись?')],
        [KeyboardButton(text='Модуль 1️⃣')],
        [KeyboardButton(text='Назад🔙')]
    ],
    resize_keyboard=True
)


# Меню уроков (модуль 1)
module_1_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Урок 1️⃣')],
        [KeyboardButton(text='Урок 2️⃣')],
        [KeyboardButton(text='Урок 3️⃣')],
        [KeyboardButton(text='Урок 4️⃣')],
        [KeyboardButton(text='Урок 5️⃣')],
        [KeyboardButton(text='Урок 6️⃣')],
        [KeyboardButton(text='Назад  🔙')]
    ],
    resize_keyboard=True
)


# Кнопки внутри уроков
def lesson_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пройти тест ✅")],
            [KeyboardButton(text="Назад 🔙")]
        ],
        resize_keyboard=True
    )


# Кнопки после сдачи теста
def after_test_menu(passed: bool):
    if passed:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Следующий урок ⏭️")],
                [KeyboardButton(text="Назад 🔙")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Пересдать тест 🔄")],
                [KeyboardButton(text="Назад 🔙")]
            ],
            resize_keyboard=True
        )
