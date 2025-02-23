import asyncio
import logging
import re

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile
from scripts.config import TOKEN_API
from scripts.db_manager import AsyncDB, block_inactive_users
from datetime import datetime
from scripts.markup import get_lesson_keyboard
import scripts.markup as sm

bot = Bot(TOKEN_API)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await AsyncDB.update_user(message.from_user.id, last_date=datetime.now().date())
    existing_user = await AsyncDB.get_user_by_telegram_id(message.from_user.id)
    if existing_user:
        await message.answer('✅ C Возвращением!')
        await message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view',
                             reply_markup=sm.menu_buttons_keyboard)
    else:
        video_path = r"D:\PythonProjects\video_2025-02-17_14-08-40.mp4"
        video = FSInputFile(video_path)
        await message.answer_video(video)
        await message.answer(f'Hello {message.from_user.first_name}', reply_markup=sm.main_regicter_inline_markup)


@dp.callback_query(F.data == 'program')
async def program(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view')
    await callback.message.answer_photo(photo='https://ionity.ua/wp-content/uploads/2025/01/m4-cs.jpg.jpg')
    await callback.message.answer('text', reply_markup=sm.program_go_back_inline_markup)


@dp.callback_query(F.data == 'program_go_back')
async def program_go_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view',
                                  caption='text',
                                  reply_markup=sm.main_regicter_inline_markup)


@dp.callback_query(F.data == 'why_need')
async def why_need(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view')
    await callback.message.answer('text', reply_markup=sm.program_go_back_inline_markup)


@dp.callback_query(F.data == 'register')
async def register(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view',
                                  caption='text',
                                  reply_markup=sm.register_inline_markup)


@dp.callback_query(F.data == 'go_back_register')
async def go_back_register(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view')
    await callback.message.answer('text', reply_markup=sm.main_regicter_inline_markup)


@dp.callback_query(F.data == "read_conditions")
async def read_conditions(callback: CallbackQuery):
    await callback.answer('📌 Условия: \n1️⃣ Вы соглашаетесь с правилами. \n'
                          '2️⃣ Данные будут обработаны.\n'
                          '3️⃣ Спам '
                          'запрещён!',
                          show_alert=True)
    await callback.message.answer('Если согласны, нажмите кнопку ниже:',
                                  reply_markup=sm.register_accept_inline_markup)
    await callback.answer()


class RegisterState(StatesGroup):
    waiting_for_email = State()


EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


@dp.callback_query(F.data == 'accept')
async def accept(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegisterState.waiting_for_email)
    existing_user = await AsyncDB.get_user_by_telegram_id(callback.from_user.id)
    if existing_user:
        await callback.message.answer('✅ Вы уже зарегистрированы! Продолжаем...')
        await callback.message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view',
                                      caption='text',
                                      reply_markup=sm.accept_inline_markup)
    else:
        await callback.message.answer('Введите ваш email:')


@dp.message(RegisterState.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    if not re.match(EMAIL_REGEX, email):
        await message.answer('❌ Некорректный email. Введите корректный адрес, например: example@gmail.com')
        return

    await state.update_data(email=email)
    user_data = await state.get_data()
    await AsyncDB.create_user(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name,
        email=user_data["email"]
    )
    await message.answer('✅ Регистрация завершена!')

    await state.clear()

    await message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view',
                         caption='text',
                         reply_markup=sm.accept_inline_markup)


@dp.callback_query(F.data == 'go_back_accept')
async def register(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view',
                                  caption='text',
                                  reply_markup=sm.register_inline_markup)


@dp.callback_query(F.data == 'form')
async def form(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view',
                                  caption='text',
                                  reply_markup=sm.form_inline_markup)


@dp.callback_query(F.data == 'go_back_form')
async def go_back_form(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view',
                                  caption='text',
                                  reply_markup=sm.accept_inline_markup)


@dp.callback_query(F.data == 'pay')
async def pay(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer_photo(
        photo='https://www.apple.com/v/apple-pay/u/images/meta/apple_pay__c08w264834sy_og.png?202502121246',
        caption='text',
        reply_markup=sm.pay_inline_markup)


@dp.callback_query(F.data == 'to_pay')
async def front_of_menu(callback: CallbackQuery):
    await callback.message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view',
                                  reply_markup=sm.menu_buttons_keyboard)


@dp.message(F.text == "Навчання 📚")
async def back_to_main(message: Message):
    user = await AsyncDB.get_user(message.from_user.id)
    print(user)

    if not user:
        await message.answer("Вы не зарегистрированы.")
        return

    keyboard = sm.get_module_keyboard(getattr(user, "current_module", 1))
    await message.answer("Выберите модуль:", reply_markup=keyboard)


@dp.message(F.text == 'Як навчатися?')
async def back_to_main(message: Message):

    await message.answer('text', reply_markup=sm.back_buttons_keyboard)
    # video_url = 'https://drive.google.com/uc?export=download&id=1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9'

    # await message.answer_video(video_url,)


@dp.message(F.text == "Назад")
async def back_to_main(message: Message):
    await message.answer('https://drive.google.com/file/d/1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9/view',
                         reply_markup=sm.menu_buttons_keyboard)


@dp.message(lambda message: message.text.startswith('Модуль'))
async def handle_module(message: Message):

    telegram_id = message.from_user.id
    await AsyncDB.update_current_module(telegram_id, 1)

    # Получаем пользователя из БД по telegram_id
    user = await AsyncDB.get_user_by_telegram_id(message.from_user.id)

    if user:
        # Обновляем поле module_start_date в базе данных
        await AsyncDB.set_module_start_date(message.from_user.id)

        user = await AsyncDB.get_user(message.from_user.id)
        print(user)

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        keyboard = get_lesson_keyboard(getattr(user, "current_lesson", 1))
        await message.answer("Выберите урок:", reply_markup=keyboard)
    else:
        await message.answer("Пользователь не найден в базе данных.")


async def check_modules():
    """Проверяет пользователей и открывает новый модуль, если прошло 15 дней."""
    users = await AsyncDB.get_all_users()  # Получаем всех пользователей

    for user in users:
        if user.module_start_date and user.current_module < 6:
            days_passed = (datetime.now().date() - user.module_start_date).days
            if days_passed >= 15:
                await AsyncDB.update_current_module(user.tel_id, user.current_module + 1)
                await AsyncDB.set_module_start_date(user.tel_id)


async def scheduler():
    while True:
        await block_inactive_users()
        await check_modules()
        await asyncio.sleep(86400)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
try:
    asyncio.run(main())
    asyncio.run(scheduler())
except KeyboardInterrupt:
    print('Exit')
