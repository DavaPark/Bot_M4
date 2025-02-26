import asyncio
import logging
import re

from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardMarkup, InputFile
from scripts.config import TOKEN_API
from scripts.db_manager import AsyncDB, block_inactive_users, \
    get_lesson_data_json, update_current_video_index, update_current_test_index, update_current_video_index_0, \
    get_videos_by_module_lesson
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
    await AsyncDB.create_user_progress(telegram_id=message.from_user.id)
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
async def study(message: Message):
    user = await AsyncDB.get_user(message.from_user.id)

    if not user:
        await message.answer("Вы не зарегистрированы.")
        return

    keyboard = sm.get_module_keyboard(getattr(user, "current_module", 1))
    await message.answer("Выберите модуль:", reply_markup=keyboard)


@dp.message(F.text == 'Як навчатися?')
async def study_how(message: Message):

    await message.answer('text', reply_markup=sm.module_back_buttons_keyboard)
    # video_url = 'https://drive.google.com/uc?export=download&id=1X3XKbHSVr6j-ljYcoKWvFUSftAwFyqL9'

    # await message.answer_video(video_url,)


@dp.message(lambda message: message.text.startswith('Модуль'))
async def handle_module(message: Message):
    module_number = int(message.text.split(" ")[1])  # Получаем номер модуля
    tel_id = message.from_user.id

    await AsyncDB.update_user_progress_module(tel_id, module_number)

    # Получаем пользователя из БД по telegram_id
    user = await AsyncDB.get_user_by_telegram_id(message.from_user.id)

    if user:
        user = await AsyncDB.get_user(message.from_user.id)

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        keyboard = get_lesson_keyboard(getattr(user, "current_lesson", 1))
        await message.answer("Выберите урок:", reply_markup=keyboard)
    else:
        await message.answer("Пользователь не найден в базе данных.")


# Обработчик для кнопки "Урок"
@dp.message(lambda message: message.text.startswith('Урок'))
async def handle_lesson(message: Message):
    lesson_number = int(message.text.split(" ")[1])  # Получаем номер урока
    tel_id = message.from_user.id
    module_number = await AsyncDB.get_user_progress_current_module(tel_id)
    current_module = await AsyncDB.get_user_current_module(tel_id)
    current_lesson = await AsyncDB.get_current_lesson(tel_id)

    if module_number == current_module and lesson_number == current_lesson:
        await update_current_video_index_0(lesson_number, module_number)

        await AsyncDB.update_user_progress_lesson(tel_id, lesson_number)

        lesson_data = await get_lesson_data_json(module_number, lesson_number)

        if lesson_data:
            first_video = lesson_data["video"][0].get("video_1")  # Первая ссылка на видео
            first_test_link = lesson_data["test_links"][0].get("test_1")  # Первая ссылка на тест

            # Создаем инлайн кнопку для теста
            test_button = InlineKeyboardButton(text="Пройти тест", url=first_test_link)

            # Создаем инлайн клавиатуру
            lesson_keyboard = InlineKeyboardMarkup(inline_keyboard=[[test_button]])

            # Создаем реплай-кнопку для продолжения
            next_button = KeyboardButton(text="Далі")
            lesson_keyboard_reply = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[next_button]])

            # Отправляем сообщение с видео и кнопкой
            await message.answer(
                f"Ваше видео для {lesson_data['title']}:\n{first_video}",
                reply_markup=lesson_keyboard
            )

            if not lesson_data:
                await message.answer("Урок не найден в базе данных.")
                return

            # Получаем индекс текущего видео
            video_index = lesson_data['current_video_index']
            await update_current_video_index(module_number, lesson_number, video_index + 1)
            await update_current_test_index(module_number, lesson_number, video_index + 1)
            await message.answer("Для перехода к следующему шагу, нажмите 'Далі'.",
                                 reply_markup=lesson_keyboard_reply)  # Здесь реплай-кнопка)
        else:
            await message.answer("Не удалось найти данные об уроке.")
    else:
        lesson_data = await get_videos_by_module_lesson(module_number, lesson_number)
        await message.answer(f'Вот усі відео {lesson_data}',
                             reply_markup=sm.lesson_back_buttons_keyboard)


# Обработчик для кнопки "Далі"
@dp.message(lambda message: message.text == 'Далі')
async def handle_next_button(message: Message):
    tel_id = message.from_user.id
    current_module = await AsyncDB.get_user_progress_current_module(tel_id)

    # Получаем текущий урок пользователя
    current_lesson_data = await AsyncDB.get_user_progress_current_lesson(tel_id)
    # Получаем данные урока из JSON
    lesson_data = await get_lesson_data_json(current_module, current_lesson_data)

    if not current_lesson_data:
        await message.answer("Урок не найден.")
        return

    if not lesson_data:
        await message.answer("Урок не найден в базе данных.")
        return

    # Получаем индекс текущего видео
    video_index = lesson_data['current_video_index']

    # Проверяем, есть ли следующее видео
    if video_index < len(lesson_data['video']):
        # Получаем ссылку на следующее видео
        video_url = list(lesson_data['video'][video_index].values())[0]  # получаем ссылку на видео
        test_index = lesson_data['current_test_index']
        if test_index < len(lesson_data['test_links']):
            # Получаем ссылку на следующий тест
            test_url = list(lesson_data['test_links'][test_index].values())[0]  # получаем ссылку на тест
            # Создаем инлайн кнопку для теста
            test_button = InlineKeyboardButton(text="Пройти тест", url=test_url)

            # Создаем инлайн клавиатуру
            lesson_keyboard = InlineKeyboardMarkup(inline_keyboard=[[test_button]])
            # Обновляем индекс видео для пользователя
            await update_current_video_index(current_module, current_lesson_data, video_index + 1)
            await message.answer(f"Смотрите видео: {video_url}",
                                 reply_markup=lesson_keyboard)
        else:
            await message.answer('Ви молодці!')
    else:
        await message.answer("Ви молодці приступайте до наступного уроку",
                             reply_markup=sm.get_next_lesson_keyboard())


@dp.message(lambda message: message.text == "Следующий урок")
async def handle_next_lesson(message: Message):
    tel_id = message.from_user.id
    current_lesson = await AsyncDB.get_current_lesson(tel_id)
    next_lesson = current_lesson + 1

    # Проверяем, что пользователь не пытается перейти на урок, который он уже прошел
    if current_lesson is not None and current_lesson <= 6:  # Например, у нас 6 уроков
        await AsyncDB.update_current_lesson(tel_id, next_lesson)
        await message.answer(f"Вы перешли на {next_lesson}-й урок. Удачи в обучении!")

        # Получаем информацию о пользователе для отправки следующих уроков
        user = await AsyncDB.get_user_by_telegram_id(tel_id)
        if user:
            # Отправляем клавиатуру с новым уроком
            keyboard = get_lesson_keyboard(next_lesson)
            await message.answer("Выберите урок:", reply_markup=keyboard)
        else:
            await message.answer("Пользователь не найден в базе данных.")
    else:
        await message.answer("Поздравляем, вы завершили все уроки этого модуля!")


@dp.message(F.text == "Вернуться к урокам")
async def back_to_lessons(message: Message):
    # Получаем пользователя из БД по telegram_id
    user = await AsyncDB.get_user_by_telegram_id(message.from_user.id)

    if user:
        user = await AsyncDB.get_user(message.from_user.id)

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        keyboard = get_lesson_keyboard(getattr(user, "current_lesson", 1))
        await message.answer("Выберите урок:", reply_markup=keyboard)
    else:
        await message.answer("Пользователь не найден в базе данных.")


@dp.message(F.text == "Головне меню")
async def back_to_lessons(message: Message):
    await message.answer("Ви повернулись у головне меню.",
                         reply_markup=sm.menu_buttons_keyboard)


@dp.message(F.text == "🔙Модулі")
async def back_to_lessons(message: Message):
    user = await AsyncDB.get_user(message.from_user.id)
    keyboard = sm.get_module_keyboard(getattr(user, "current_module", 1))
    await message.answer("Ви повернулись до модулів:", reply_markup=keyboard)


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
