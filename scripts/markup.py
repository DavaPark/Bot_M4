from typing import Tuple

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton)


main_regicter_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Реєстрація', callback_data='register')],
    [InlineKeyboardButton(text='Відгуки', url='https://t.me/+FR1_yfv_z8kzOTli')],
    [InlineKeyboardButton(text='Програма', callback_data='program')],
    [InlineKeyboardButton(text='Навіщо тобі М4 Реді', callback_data='why_need')],
    [InlineKeyboardButton(text='Сайт', url='https://t.me/+FR1_yfv_z8kzOTli')],
    [InlineKeyboardButton(text='Телеграм канал М4 Реді', url='https://t.me/+FR1_yfv_z8kzOTli')],
    [InlineKeyboardButton(text='Підтримка', url='https://t.me/+FR1_yfv_z8kzOTli')]
])


register_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📜Прочитати умови', url='https://telegra.ph/Publ%D1%96chna-oferta-na-koristuvannya-poslugami-chat-bota-z-navchalnimi-kursami-02-27')],
    [InlineKeyboardButton(text='✅Прийняти умови', callback_data='accept')],
    # [InlineKeyboardButton(text='Назад 🔙', callback_data='go_back_register')]

])


register_accept_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Прийняти умови', callback_data='accept')]
])


accept_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проходження форми', callback_data='form')],
    [InlineKeyboardButton(text='Назад 🔙', callback_data='go_back_accept')]
])


form_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Google Forms', url='https://docs.google.com/forms/d/e/1FAIpQLSeH3TmTV8R3XsfrYpRO6MeVqr1ytrMzgWinGyxjtTWI9--gTQ/viewform?usp=header')],
    [InlineKeyboardButton(text='✅ Я заповнив/ла анкету', callback_data='check_registration_form')],
    # [InlineKeyboardButton(text='Назад 🔙', callback_data='go_back_form')]
])


program_go_back_inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Реєстрація', callback_data='register')],
    [InlineKeyboardButton(text='⬅Назад', callback_data='program_go_back')]
])


def pay_keyb(link):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💳 Оплатити', url=link)]
    ])


menu_buttons_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Навчання 📚"), KeyboardButton(text="Публічний договір")],
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

lesson_back_buttons_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Повернутися до уроків")]],
    resize_keyboard=True
)

module_back_buttons_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔙Модулі")]],
    resize_keyboard=True
)

next_module_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Наступний модуль")]
    ],
    resize_keyboard=True
)


def get_module_keyboard(current_module: int) -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text="Як навчатися?")]]
    buttons += [[KeyboardButton(text=f"Модуль {i}")] for i in range(1, current_module + 1)]
    buttons.append([KeyboardButton(text="Головне меню")])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def get_lesson_keyboard(current_lesson: int) -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text=f"Урок {i}")] for i in range(1, current_lesson + 1)]
    buttons.append([KeyboardButton(text="🔙Модулі")])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# Функция для создания клавиатуры с кнопками для уроков
def get_lesson_study_keyboard(lesson_title: str, test_link: str, video: str) -> tuple[ReplyKeyboardMarkup, str, str]:
    buttons = [
        [KeyboardButton(text=f"Тест ({lesson_title})")],
        [KeyboardButton(text="Далі")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    # Возвращаем клавиатуру, видео и ссылку на тест
    return keyboard, video, test_link


# Функция для создания кнопок "Тест" и "Далі"
def get_lesson_more_keyboard(test_url):
    buttons = [
        [KeyboardButton(text=f"Тест", url=test_url)],
        [KeyboardButton(text="Далі")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


# Функция для кнопки "Пройти знову"
def get_retry_keyboard():
    buttons = [
        [KeyboardButton(text="Пройти знову")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


# Функция для создания клавиатуры с кнопкой "Следующий урок"
def get_next_lesson_keyboard():
    buttons = [
        [KeyboardButton(text="Наступний урок")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


