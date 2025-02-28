import asyncio
import json
import logging
import re

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardMarkup
from scripts.config import TOKEN_API, W4P_KEY, DOMAIN_NAME, MERCHANT_ACCOUNT
from scripts.db_manager import AsyncDB, block_inactive_users, \
    get_lesson_data_json, update_current_video_index, update_current_test_index, update_current_video_index_0, \
    get_current_video_index, update_current_test_index_0, get_current_test_index
from datetime import datetime
from scripts.markup import get_lesson_keyboard

import scripts.markup as sm
from scripts.texts import *
from scripts.way4pay import WayForPay

bot = Bot(TOKEN_API, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await AsyncDB.update_user(message.chat.id, last_date=datetime.now().date())
    existing_user = await AsyncDB.get_user_by_telegram_id(message.chat.id)
    if existing_user:
        video_id = 'BAACAgIAAxkBAAPFZ8Bu8ajHtoaignWxQ97udddTYCwAAq5hAAJXDAhKFdXY_cFCbyE2BA'
        await message.answer_video(video_id,
                                   reply_markup=sm.menu_buttons_keyboard)
    else:

        video_id = "BAACAgIAAxkBAAMDZ8BKn5Cuc8QAAb0ce2k7QJdqiP9aAAKlcgACVwwAAUpvyyB6gghfJjYE"
        await message.answer_video(video_id)
        await message.answer("👋 Привіт! <b>Раді, що ти тут!</b> Якщо ти дивишся це відео, значить, прагнеш зрозуміти свій поклик. І це чудово! 🎯\n"
                             "\n<b>М4 Інтенсив</b> – це 90 днів практичного навчання, що допоможе тобі знайти своє місце в служінні. Ми підтримаємо тебе на цьому шляху та дамо інструменти для впевненого старту.\n"
                             "\n<b>Як почати?</b>\n"
                             "\n🔹 <b>Щоб впевнитися, що це для тебе</b> – переглянь інформацію під відео: про нас, програму курсу, відгуки учасників. Досліджуй та приймай рішення!\n"
                             "🔹 <b>Готовий зробити крок?</b> Натискай 'Зареєструватися', заповнюй форму та ставай частиною нашої спільноти! 🚀",
                             reply_markup=sm.main_regicter_inline_markup)


@dp.callback_query(F.data == 'program')
async def program(callback: CallbackQuery):
    await callback.answer()
    video_id = "BAACAgIAAxkBAANWZ8BbIwP5xhYxSdZo52GR4QVaj6MAAsdzAAJXDAABStl7xdfRNRl-NgQ"
    await callback.message.answer_video(video_id)
    await callback.message.answer_photo(photo='AgACAgIAAxkBAANaZ8BbkqdO-1QYenBcyDJ3RqdnzrwAAkDmMRtApwABSsqe1imkYgvmAQADAgADeQADNgQ')
    await callback.message.answer("\n<b>Що ти отримаєш під час навчання?</b>\n"
                                  "M4 Ready – це 90-денний інтерактивний онлайн-курс у Telegram, який допоможе тобі зрозуміти, чи кличе тебе Бог до заснування церкви, та дасть чіткий план подальших кроків у служінні.\n"
                                  "\n<b>🔹 Що включає навчання?</b>\n"
                                  "✅ <b>6 ключових модулів</b> – усе, що потрібно для розвитку лідерства, команди та бачення церкви.\n"
                                  "✅ <b>Практичні відеоуроки</b> – стисла, структурована інформація без води.\n"
                                  "✅ <b>Інтерактивні завдання</b> – не просто слухай, а застосовуй знання в реальних ситуаціях.\n"
                                  "✅ <b>Онлайн-спільнота</b> – підтримка та натхнення від інших учасників курсу.\n"
                                  "✅ <b>Регіональні зустрічі</b> – живе спілкування, обмін досвідом і натхнення.\n"
                                  "✅ <b>Гнучкий формат</b> – навчайся в зручному ритмі, коли тобі комфортно.\n"
                                  "✅ <b>Конкретний план дій</b> – отримаєш зрозумілий алгоритм створення та розвитку громади.\n"
                                  "✅ <b>Досвід практиків</b> – навчання від лідерів, які вже заснували церкви.\n"
                                  "✅ <b>Фокус на результат</b> – лише те, що дійсно працює у сучасному служінні.\n"
                                  "\n🎯 <b>Для кого цей курс?</b>\n"
                                  "\n <b>-</b> Для тих, хто хоче зрозуміти, чи кличе їх Бог до заснування церкви.\n"
                                  "<b>-</b> Для молодих лідерів, які шукають своє місце в служінні.\n"
                                  "<b>-</b> Для тих, хто прагне навчитись ефективно вести команду та будувати громаду.\n"
                                  "\n📌<b> Якщо ти шукаєш ясність у покликанні та чіткі кроки для служіння – цей курс для тебе!</b>\n"
                                  "\nНатискай 'Реєстрація' та приєднуйся до навчання🚀",
                                  reply_markup=sm.program_go_back_inline_markup)


@dp.callback_query(F.data == 'program_go_back')
async def program_go_back(callback: CallbackQuery):
    await callback.answer()
    video_id = "BAACAgIAAxkBAAMDZ8BKn5Cuc8QAAb0ce2k7QJdqiP9aAAKlcgACVwwAAUpvyyB6gghfJjYE"
    await callback.message.answer_video(video_id)
    await callback.message.answer("👋 Привіт! <b>Раді, що ти тут!</b> Якщо ти дивишся це відео, значить, прагнеш зрозуміти свій поклик. І це чудово! 🎯\n"
                             "\n<b>М4 Інтенсив</b> – це 90 днів практичного навчання, що допоможе тобі знайти своє місце в служінні. Ми підтримаємо тебе на цьому шляху та дамо інструменти для впевненого старту.\n"
                             "\n<b>Як почати?</b>\n"
                             "\n🔹 <b>Щоб впевнитися, що це для тебе – переглянь інформацію під відео: про нас, програму курсу, відгуки учасників. Досліджуй та приймай рішення!\n"
                             "🔹 <b>Готовий зробити крок? Натискай 'Зареєструватися', заповнюй форму та ставай частиною нашої спільноти! 🚀",
                                  reply_markup=sm.main_regicter_inline_markup)


@dp.callback_query(F.data == 'why_need')
async def why_need(callback: CallbackQuery):
    await callback.answer()
    video_id = 'BAACAgIAAxkBAAOnZ8BnIbfCSg2R5HU4izjpcI-7dzgAAqdhAAJApwABSsDvmC8dOYGgNgQ'
    await callback.message.answer_video(video_id)
    await callback.message.answer_photo(photo='AgACAgIAAxkBAAOjZ8BmyzugXiu1u03VDUA7QorTKtgAApjpMRtXDAhKvNirwneIGxUBAAMCAAN5AAM2BA')
    await callback.message.answer("🚀 <b>Чи кличе тебе Бог до заснування церкви?</b>\n"
                                  "\nТи відчуваєш, що Бог може кликати тебе до більшого, але не знаєш, з чого почати? Чи активно ділишся Євангелієм, дбаєш про людей, прагнеш змін у своїй громаді, але не впевнений, чи варто тобі засновувати церкву? <b>M4 Інтенсив</b> – це 90-денний інтерактивний онлайн-курс у Telegram, створений саме для тих, хто шукає відповіді на ці питання та прагне зробити впевнені перші кроки у своєму покликанні.\n"
                                  "\n🔹 <b>Що ти отримаєш?</b> \n"
                                  "\n ✅ 6 ключових модулів, що проведуть тебе від розпізнавання покликання до практичного служіння.\n"
                                  "✅ Лаконічні відеоуроки та інтерактивні завдання для застосування знань у реальному житті.\n"
                                  "✅ Структурований підхід, що допоможе рухатися вперед у зручному темпі без хаосу та перевантаження.\n"
                                  "✅ Онлайн-спільнота, де ти знайдеш підтримку, натхнення та відповіді на свої питання.\n"
                                  "✅ Регіональні зустрічі для знайомства, обміну досвідом та зміцнення у покликанні.\n"
                                  "\n🎯 <b>Для кого цей курс?</b>\n"
                                  "\n<b>-</b> Для тих, хто хоче зрозуміти, чи дійсно Бог кличе їх засновувати церкву.\n"
                                  "<b>-</b> Для молодих лідерів, які шукають своє місце в служінні.\n"
                                  "<b>-</b> Для тих, хто хоче навчитись вести команду та розвивати здорову церкву.\n"
                                  "\n 📌 <b>Якщо ти прагнеш знайти чітке бачення свого покликання – ця програма для тебе!</b> Натискай 'Реєстрація' та ставай частиною цього шляху.",
                                  reply_markup=sm.program_go_back_inline_markup)


@dp.callback_query(F.data == 'register')
async def register(callback: CallbackQuery):
    await callback.answer()
    video_id = 'BAACAgIAAxkBAAMKZ8BNTYitzbPryFUzEPINTV2IYkIAAtVyAAJXDAABShI4YflxeikaNgQ'
    await callback.message.answer_video(video_id,
                                  caption='🎉 Ти на крок ближче до змін! Зараз важливо визначитися: чи готовий ти інвестувати час у своє покликання?\n'
                                          '\n<b>Що потрібно знати?</b>\n'
                                          '✅ <b>Цінність навчання – 145$</b>, але для українців діє спецпропозиція – <b>500 грн</b>. Ми встановили мінімальну оплату, щоб долучалися лише ті, хто серйозно налаштований навчатися й застосовувати знання на практиці.'
                                          '✅ \n<b>Перед стартом прийми умови</b> – це гарантія якісного навчання.\n'
                                          '\n<b>Як приєднатися?</b>\n'
                                          '\n1️⃣ <b>Прочитай умови</b> – натисни "Прочитати умови".\n'
                                          '2️⃣ <b>Підтвердь згоду</b> – натисни "Прийняти умови".\n'
                                          '3️⃣ <b>Заповни форму</b> та залиш e-mail. Маєш питання? Пиши на M4Ukraine@gmail.com.\n'
                                          '4️⃣ <b>Оплати курс</b> – швидко та безпечно через WayForPay.\n'
                                          '\n🚀 Якщо ти готовий діяти – почнемо просто зараз!',
                                  reply_markup=sm.register_inline_markup)


@dp.callback_query(F.data == 'go_back_register')
async def go_back_register(callback: CallbackQuery):
    await callback.answer()
    video_id = 'BAACAgIAAxkBAAMKZ8BNTYitzbPryFUzEPINTV2IYkIAAtVyAAJXDAABShI4YflxeikaNgQ'
    await callback.message.answer_video(video_id,
                                        caption='🎉 Ти на крок ближче до змін! Зараз важливо визначитися: чи готовий ти інвестувати час у своє покликання?\n'
                                          '\n<b>Що потрібно знати?</b>\n'
                                          '✅ <b>Цінність навчання – 145$</b>, але для українців діє спецпропозиція – <b>500 грн</b>. Ми встановили мінімальну оплату, щоб долучалися лише ті, хто серйозно налаштований навчатися й застосовувати знання на практиці.'
                                          '✅ \n<b>Перед стартом прийми умови</b> – це гарантія якісного навчання.\n'
                                          '\n<b>Як приєднатися?</b>\n'
                                          '\n1️⃣ <b>Прочитай умови</b> – натисни "Прочитати умови".\n'
                                          '2️⃣ <b>Підтвердь згоду</b> – натисни "Прийняти умови".\n'
                                          '3️⃣ <b>Заповни форму</b> та залиш e-mail. Маєш питання? Пиши на M4Ukraine@gmail.com.\n'
                                          '4️⃣ <b>Оплати курс</b> – швидко та безпечно через WayForPay.\n'
                                          '\n🚀 Якщо ти готовий діяти – почнемо просто зараз!',
                                        reply_markup=sm.main_regicter_inline_markup)


class RegisterState(StatesGroup):
    waiting_for_email = State()


EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


@dp.callback_query(F.data == 'accept')
async def accept(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegisterState.waiting_for_email)
    await callback.answer()
    existing_user = await AsyncDB.get_user_by_telegram_id(callback.from_user.id)
    if existing_user:
        await callback.message.answer('✅ Ви вже зареєстровані! Продовжуємо...',
                                      reply_markup=sm.accept_inline_markup)
    else:
        await callback.message.answer('🎉 Ти майже готовий розпочати навчання! Щоб отримати доступ, нам потрібен твій e-mail – Telegram дозволяє надсилати матеріали лише зареєстрованим у системі користувачам.\n'
                                      '\n<b>Що потрібно зробити?</b>\n'
                                      '\n✉️ <b>Введи свій e-mail</b> у поле нижче.\n'
                                      '🔐 <b>Переконайся, що він правильний</b>, щоб не втратити доступ.\n'
                                      '✅<b>Далі – заповнення форми</b>, після чого зможеш перейти до оплати.\n'
                                      '\n🚀Все готово? Тоді вперед!')


@dp.message(RegisterState.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    if not re.match(EMAIL_REGEX, email):
        await message.answer('❌ Некоректний email. Введіть правильну адресу, наприклад: example@gmail.com')
        return

    await state.update_data(email=email)
    user_data = await state.get_data()
    await AsyncDB.create_user(
        telegram_id=message.chat.id,
        name=message.from_user.full_name,
        email=user_data["email"],
        username=message.from_user.username
    )
    await AsyncDB.create_user_progress(telegram_id=message.chat.id)
    await bot.send_message(
        message.chat.id,
        "🎯 Ти майже на старті! Залишився важливий крок – заповнити анкету. Це обов’язкова умова для реєстрації та доступу до курсу.\n"
        "\nАнкета допоможе нам краще зрозуміти твої потреби та зробити навчання більш цінним для тебе. А для тебе – це можливість усвідомити свої цілі та отримати максимальну користь\n"
        "\n<b>Чому це важливо?</b>\n"
        "\n📝 Чіткіше визначиш свої очікування від курсу.\n"
        "📊 Ми адаптуємо матеріали під потреби учасників.\n"
        "🤝 Станеш частиною спільноти однодумців.\n"
        "\n<b>Що робити?</b>\n"
        "\n1️⃣ <b>Заповни анкету</b> – натисни кнопку нижче.\n"
        "2️⃣ <b>Повернися та натисни 'Я заповнив/ла анкету'</b>, щоб перейти до оплати.\n"
        "\n🚀 Ти готовий? Тоді вперед!\n",
        reply_markup=sm.form_inline_markup)
    await state.clear()


@dp.callback_query(F.data == 'go_back_accept')
async def register(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('✅ Ви вже зареєстровані! Продовжуємо...',
                                  reply_markup=sm.register_inline_markup)


@dp.callback_query(F.data == 'form')
async def form(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("🎯 Ти майже на старті! Залишився важливий крок – заповнити анкету. Це обов’язкова умова для реєстрації та доступу до курсу.\n"
                                  "\nАнкета допоможе нам краще зрозуміти твої потреби та зробити навчання більш цінним для тебе. А для тебе – це можливість усвідомити свої цілі та отримати максимальну користь\n"
                                  "\n<b>Чому це важливо?</b>\n"
                                  "\n📝 Чіткіше визначиш свої очікування від курсу.\n"
                                  "📊 Ми адаптуємо матеріали під потреби учасників.\n"
                                  "🤝 Станеш частиною спільноти однодумців.\n"
                                  "\n<b>Що робити?</b>\n"
                                  "\n1️⃣ <b>Заповни анкету</b> – натисни кнопку нижче.\n"
                                  "2️⃣ <b>Повернися та натисни 'Я заповнив/ла анкету'</b>, щоб перейти до оплати.\n"
                                  "\n🚀 Ти готовий? Тоді вперед!\n",
                                  reply_markup=sm.form_inline_markup)


@dp.callback_query(F.data == 'go_back_form')
async def go_back_form(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("🎯 Ти майже на старті! Залишився важливий крок – заповнити анкету. Це обов’язкова умова для реєстрації та доступу до курсу.\n"
                                  "\nАнкета допоможе нам краще зрозуміти твої потреби та зробити навчання більш цінним для тебе. А для тебе – це можливість усвідомити свої цілі та отримати максимальну користь\n"
                                  "\n<b>Чому це важливо?</b>\n"
                                  "\n📝 Чіткіше визначиш свої очікування від курсу.\n"
                                  "📊 Ми адаптуємо матеріали під потреби учасників.\n"
                                  "🤝 Станеш частиною спільноти однодумців.\n"
                                  "\n<b>Що робити?</b>\n"
                                  "\n1️⃣ <b>Заповни анкету</b> – натисни кнопку нижче.\n"
                                  "2️⃣ <b>Повернися та натисни 'Я заповнив/ла анкету'</b>, щоб перейти до оплати.\n"
                                  "\n🚀 Ти готовий? Тоді вперед!\n",
                                  reply_markup=sm.accept_inline_markup)


@dp.callback_query(F.data == 'to_pay')
async def front_of_menu(callback: CallbackQuery):

    # при успешной оплате
    video_id = 'BAACAgIAAxkBAAPFZ8Bu8ajHtoaignWxQ97udddTYCwAAq5hAAJXDAhKFdXY_cFCbyE2BA'
    await callback.answer()
    await callback.message.answer_video(video_id,
                                        reply_markup=sm.menu_buttons_keyboard)



@dp.callback_query(F.data == 'check_registration_form')
async def check_registration_form(callback: CallbackQuery):
    tel_id = callback.message.chat.id
    user = await AsyncDB.get_user(tel_id)
    await bot.delete_message(tel_id, callback.message.message_id)
    if user:
        if user.phone and user.region and user.denomination and user.role:
            if len(user.phone) != 0 and len(user.region) != 0 and len(user.denomination) != 0 and len(user.role) != 0:
                payment_number = await AsyncDB.get_user_payments(tel_id)
                wfp = WayForPay(key=W4P_KEY, domain_name=DOMAIN_NAME)
                res = wfp.create_invoice(
                    merchantAccount=MERCHANT_ACCOUNT,
                    merchantAuthType='SimpleSignature',
                    amount='500',
                    currency='UAH',
                    productNames=["Оплата за курс M4"],
                    productPrices=[500],
                    productCounts=[1],
                    orderID=f"M4-{tel_id}-{0 if payment_number is None else payment_number + 1}"
                )
                link = res.invoiceUrl
                if link is not None:
                    await bot.send_message(tel_id, pay_text, reply_markup=sm.pay_keyb(link))
                    return

    await bot.send_message(tel_id, not_registered_yet, reply_markup=sm.form_inline_markup)


@dp.message(F.text == "Навчання 📚")
async def study(message: Message):
    user = await AsyncDB.get_user(message.chat.id)

    if not user:
        await message.answer("Вы не зарегистрированы.")
        return
    keyboard = sm.get_module_keyboard(getattr(user, "current_module", 1) or 1)
    await message.answer("Оберіть модуль:", reply_markup=keyboard)


@dp.message(F.text == 'Як навчатися?')
async def study_how(message: Message):

    await message.answer('text', reply_markup=sm.module_back_buttons_keyboard)


@dp.message(lambda message: message.text.startswith('Модуль'))
async def handle_module(message: Message):
    module_number = int(message.text.split(" ")[1])  # Получаем номер модуля
    tel_id = message.chat.id

    current_module = await AsyncDB.get_user_progress_current_module(tel_id)
    current_lesson = await AsyncDB.get_user_progress_current_lesson(tel_id)
    if current_module == 1:
        lesson_data = await get_lesson_data_json(current_module, current_lesson)
        video_data = lesson_data["video_module"]
        # Получаем видео по текущему индексу
        video_to_send = video_data[0]
        await message.answer(f"{video_to_send['title1']}")

    await AsyncDB.update_user_progress_module(tel_id, module_number)

    # Получаем пользователя из БД по telegram_id
    user = await AsyncDB.get_user_by_telegram_id(message.chat.id)

    if user:
        user = await AsyncDB.get_user(message.chat.id)

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        keyboard = get_lesson_keyboard(getattr(user, "current_lesson", 1))
        await AsyncDB.check_module_score(tel_id, module_number)
        await message.answer("Оберіть урок:", reply_markup=keyboard)
    else:
        await message.answer("Пользователь не найден в базе данных.")


# Обработчик для кнопки "Урок"
@dp.message(lambda message: message.text.startswith('Урок'))
async def handle_lesson(message: Message):
    lesson_number = int(message.text.split(" ")[1])  # Получаем номер урока
    tel_id = message.chat.id
    module_number = await AsyncDB.get_user_progress_current_module(tel_id)
    current_module = await AsyncDB.get_user_current_module(tel_id)
    current_lesson = await AsyncDB.get_current_lesson(tel_id)  # Получаем текущий урок пользователя
    await update_current_video_index_0(module_number, lesson_number)
    await update_current_test_index_0(module_number, lesson_number)
    current_video_index = await get_current_video_index(module_number, lesson_number)  # Получаем текущий индекс видео
    curent_test_index = await get_current_test_index(module_number, lesson_number)

    # Если пользователь пытается перейти к уроку, который соответствует текущему уроку
    if module_number == current_module and lesson_number == current_lesson:
        await AsyncDB.update_user_progress_lesson(tel_id, lesson_number)

        lesson_data = await get_lesson_data_json(module_number, lesson_number)

        if lesson_data:
            if "video" in lesson_data and len(lesson_data["video"]) > 0:
                video_data = lesson_data["video"]
                # Получаем видео по текущему индексу
                video_to_send = video_data[current_video_index]
                first_video_id = video_to_send.get("video_id")
                if first_video_id:
                    # Создаём инлайн-кнопку с ссылкой на тест
                    test_data = lesson_data.get("tests", [])
                    if test_data:
                        # Берем первую ссылку из списка тестов
                        test_url = test_data[current_video_index]["url"]
                        test_title = test_data[curent_test_index]["test_id"]
                        inline_button = InlineKeyboardButton(text=f"{test_title}",
                                                             url=test_url)
                        inline_button2 = InlineKeyboardButton(text=f"Далі ➡️",
                                                              callback_data="next_lesson_part")
                        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_button], [inline_button2]])

                        # Создаем реплай-кнопку для продолжения
                        # next_button = KeyboardButton(text="Далі")
                        # lesson_keyboard_reply = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[next_button]])

                        # Обновляем индекс видео для следующего раза
                        next_video_index = current_video_index + 1
                        await update_current_video_index(module_number, lesson_number, next_video_index)
                        await update_current_test_index(module_number, lesson_number, next_video_index)

                        # Отправляем видео с кнопкой
                        await message.answer_video(
                            video=first_video_id,
                            caption=f'{lesson_data.get("title")}\n \n {video_to_send["title"]}',
                            reply_markup=inline_keyboard
                        )
                        # await message.answer(f"{video_to_send['title']}",
                        #                      reply_markup=lesson_keyboard_reply)

                else:
                    await message.answer("ID видео отсутствует в данных.")
            else:
                await message.answer("В уроке нет видео.")
        else:
            await message.answer("Не удалось найти данные об уроке.")
    else:

        number = 0
        lesson_data = await get_lesson_data_json(module_number, lesson_number)
        await message.answer(f'{lesson_data.get("title")}')

        while number < len(lesson_data['video']):
            video_data = lesson_data["video"]
            # Получаем видео по текущему индексу
            video_to_send = video_data[number]
            video_id = video_to_send.get("video_id")

            await message.answer_video(video_id,
                                       caption=f"{video_to_send['title']}")
            number += 1
        else:
            await message.answer("Ось усі відео з цього уроку.",
                                 reply_markup=sm.lesson_back_buttons_keyboard)


@dp.callback_query(F.data == 'next_lesson_part')
async def front_of_menu(callback: CallbackQuery):
    tel_id = callback.message.chat.id
    _up_ = await AsyncDB.get_user_progress(tel_id)
    up = dict(json.loads(_up_.progress))
    module_number = _up_.select_module
    lesson_number = _up_.select_lesson
    current_video_index = await get_current_video_index(module_number, lesson_number)
    curent_test_index = await get_current_test_index(module_number, lesson_number)
    test_result = up[f"module{module_number}"][f"lesson{lesson_number}"][str(current_video_index)]
    if test_result is not None:
        if int(test_result) < 80:
            lesson_data = await get_lesson_data_json(module_number, lesson_number)
            test_data = lesson_data.get("tests", [])
            test_url = test_data[current_video_index]["url"]
            test_title = test_data[curent_test_index]["test_id"]
            inline_button = InlineKeyboardButton(text=f"{test_title}",
                                                 url=test_url)
            inline_button2 = InlineKeyboardButton(text=f"Далі ➡️",
                                                  callback_data="next_lesson_part")
            inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_button], [inline_button2]])
            await bot.send_message(tel_id, failed_test, reply_markup=inline_keyboard)
        else:
            await handle_next_button(callback.message)  # переход дальше
    else:
        await bot.send_message(tel_id, test_not_passed)
        return


# Обработчик для кнопки "Далі"
async def handle_next_button(message: Message):
    tel_id = message.chat.id
    module_number = await AsyncDB.get_user_progress_current_module(tel_id)
    lesson_number = await AsyncDB.get_user_progress_current_lesson(tel_id)
    # Получаем данные урока из JSON
    lesson_data = await get_lesson_data_json(module_number, lesson_number)
    print(lesson_data)
    # Получаем текущий индекс видео
    current_video_index = await get_current_video_index(module_number, lesson_number)
    curent_test_index = await get_current_test_index(module_number, lesson_number)

    if lesson_data:
        print(current_video_index, len(lesson_data['video']))
        if current_video_index < len(lesson_data['video']):
            video_data = lesson_data["video"]
            # Получаем видео по текущему индексу
            video_to_send = video_data[current_video_index]
            first_video_id = video_to_send.get("video_id")
            if first_video_id:
                # Создаём инлайн-кнопку с ссылкой на тест
                test_data = lesson_data.get("tests", [])
                if test_data:
                    # Берем первую ссылку из списка тестов
                    test_url = test_data[current_video_index]["url"]
                    test_title = test_data[curent_test_index]["test_id"]
                    inline_button = InlineKeyboardButton(text=f"{test_title}",
                                                         url=test_url)
                    inline_button2 = InlineKeyboardButton(text=f"Далі ➡️",
                                                          callback_data="next_lesson_part")
                    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_button], [inline_button2]])

                    # Создаем реплай-кнопку для продолжения
                    # next_button = KeyboardButton(text="Далі")
                    # lesson_keyboard_reply = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[next_button]])

                    # Обновляем индекс видео для следующего раза
                    next_video_index = current_video_index + 1
                    await update_current_video_index(module_number, lesson_number, next_video_index)
                    await update_current_test_index(module_number, lesson_number, next_video_index)

                    # Отправляем видео с кнопкой
                    await message.answer_video(
                        video=first_video_id,
                        caption=f"{video_to_send['title']}",
                        reply_markup=inline_keyboard
                    )
                    # await message.answer(f"{video_to_send['title']}",
                    #                      reply_markup=lesson_keyboard_reply)
            else:
                await message.answer("Ви молодці приступайте до наступного уроку",
                                     reply_markup=sm.get_next_lesson_keyboard())
        else:
            current_module = await AsyncDB.get_user_current_module(tel_id)
            current_lesson = await AsyncDB.get_current_lesson(tel_id)
            if current_lesson == 6:
                lesson_data = await get_lesson_data_json(current_module, current_lesson)
                video_data = lesson_data["video_module"]
                # Получаем видео по текущему индексу
                video_to_send = video_data[0]
                video_id = video_to_send.get("video_id")
                await message.answer_video(video_id,
                                           caption=f"{video_to_send['title2']}",
                                           reply_markup=sm.next_module_markup)
            else:
                await message.answer("Ви молодці приступайте до наступного уроку",
                                 reply_markup=sm.get_next_lesson_keyboard())
    else:
        current_module = await AsyncDB.get_user_current_module(tel_id)
        current_lesson = await AsyncDB.get_current_lesson(tel_id)
        if current_lesson == 6:
            lesson_data = await get_lesson_data_json(current_module, current_lesson)
            video_data = lesson_data["video_module"]
            # Получаем видео по текущему индексу
            video_to_send = video_data[0]
            video_id = video_to_send.get("video_id")
            await message.answer_video(video_id,
                                       caption=f"{video_to_send['title2']}",
                                       reply_markup=sm.next_module_markup)


@dp.message(lambda message: message.text == "Наступний урок")
async def handle_next_lesson(message: Message):
    tel_id = message.chat.id
    current_lesson = await AsyncDB.get_current_lesson(tel_id)
    next_lesson = current_lesson + 1

    # Проверяем, что пользователь не пытается перейти на урок, который он уже прошел
    if current_lesson is not None and current_lesson <= 6:  # Например, у нас 6 уроков
        await AsyncDB.update_current_lesson(tel_id, next_lesson)
        await message.answer(f"Ви перейшли на {next_lesson}-й урок. Успіхів у навчанні!")

        # Получаем информацию о пользователе для отправки следующих уроков
        user = await AsyncDB.get_user_by_telegram_id(tel_id)
        if user:
            # Отправляем клавиатуру с новым уроком
            keyboard = get_lesson_keyboard(next_lesson)
            await message.answer("Оберіть урок:", reply_markup=keyboard)
        else:
            await message.answer("Пользователь не найден в базе данных.")
    else:
        await message.answer("Поздравляем, вы завершили все уроки этого модуля!")


@dp.message(F.text == "Повернутися до уроків")
async def back_to_lessons(message: Message):
    # Получаем пользователя из БД по telegram_id
    user = await AsyncDB.get_user_by_telegram_id(message.chat.id)

    if user:
        user = await AsyncDB.get_user(message.chat.id)

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        keyboard = get_lesson_keyboard(getattr(user, "current_lesson", 1))
        await message.answer("Оберіть урок:", reply_markup=keyboard)
    else:
        await message.answer("Пользователь не найден в базе данных.")


@dp.message(F.text == "Головне меню")
async def back_to_lessons(message: Message):
    await message.answer("Ви повернулись у головне меню.",
                         reply_markup=sm.menu_buttons_keyboard)


@dp.message(F.text == "🔙Модулі")
async def back_to_lessons(message: Message):
    user = await AsyncDB.get_user(message.chat.id)
    keyboard = sm.get_module_keyboard(getattr(user, "current_module", 1))
    await message.answer("Ви повернулись до модулів:", reply_markup=keyboard)


@dp.message(F.text == "Наступний модуль")
async def next_module(message: Message):
    # Получаем пользователя из БД по telegram_id
    user = await AsyncDB.get_user_by_telegram_id(message.chat.id)

    if user:
        user = await AsyncDB.get_user(message.chat.id)

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        keyboard = get_lesson_keyboard(getattr(user, "current_lesson", 1))
        await message.answer("Наступний модуль ще не відкрит:", reply_markup=keyboard)
    else:
        await message.answer("Пользователь не найден в базе данных.")

# async def check_modules():
#     """Проверяет пользователей и открывает новый модуль, если прошло 15 дней."""
#     users = await AsyncDB.get_all_users()  # Получаем всех пользователей
#
#     for user in users:
#         if user.module_start_date and user.current_module < 6:
#             days_passed = (datetime.now().date() - user.module_start_date).days
#             if days_passed >= 15:
#                 await AsyncDB.update_current_module(user.tel_id, user.current_module + 1)
#                 await AsyncDB.set_module_start_date(user.tel_id)
#
#
async def scheduler():
    while True:
        await block_inactive_users()
#         await check_modules()
#         await asyncio.sleep(86400)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
try:
    asyncio.run(main())
    asyncio.run(scheduler())
except KeyboardInterrupt:
    print('Exit')
