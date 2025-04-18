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
from scripts.config import TOKEN_API, W4P_KEY, DOMAIN_NAME, MERCHANT_ACCOUNT, AMOUNT
from scripts.db_manager import AsyncDB, block_inactive_users, \
    get_lesson_data_json, update_current_video_index, update_current_test_index, update_current_video_index_1, \
    get_current_video_index, update_current_test_index_1, get_current_test_index, get_dostup_module_index, \
    update_dostup_module_index
from datetime import datetime, date
from scripts.markup import get_lesson_keyboard

import scripts.markup as sm
from scripts.texts import *
from scripts.way4pay import WayForPay

import schedule

bot = Bot(TOKEN_API, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


async def check_user(tel_id):
    user = await AsyncDB.get_user(tel_id)
    if user is not None:
        if user.is_blocked == 1:
            await bot.send_message(tel_id, text=block_text)
            return False
        else:
            return True
    return False


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await AsyncDB.update_user(message.chat.id, last_date=datetime.now().date())
    existing_user = await AsyncDB.get_user_by_telegram_id(message.chat.id)
    user = await AsyncDB.get_user(message.chat.id)
    if existing_user:
        video_id = "BAACAgIAAxkBAAMPZ_4Ps87vEG8mEXzRwtQ2bbJ08HUAAhFjAALA6vBL0sd6YDDWayA2BA"
        await message.answer_video(video_id,
                                   caption="🎉 <b>Вітаємо на навчанні!</b>\n"
                                           "\nТи зробив важливий крок, і ми раді вітати тебе у цій подорожі! "
                                           "Відкритість до нового – це ключ до зростання. Цей курс допоможе тобі "
                                           "розкрити своє покликання та використати знання для служіння."
                                           "\n\n<b>🔹 Як отримати максимум?</b> "
                                           "\n\n✅ Постав собі за мету взяти все, що може дати це навчання."
                                           "\n✅ Пройди всі 6 модулів у встановлені терміни – кожен модуль триває "
                                           "2 тижні."
                                           "\n✅ Будь активним у навчанні, став запитання та взаємодій зі спільнотою."
                                           "\n\n💡 <b>Досліди меню, щоб легко орієнтуватися та рухатися вперед!</b>"
                                           "\n\n🎯 <b>Ти готовий? Починай навчання вже зараз!</b>",
                                   reply_markup=sm.main_menu(user.is_admin))
    else:

        video_id = "BAACAgIAAxkBAAMHZ_4NV3G2jd1j467XUGOBjH32jP4AAgNjAALA6vBL7VJJ5eTLNM42BA"
        await message.answer_video(video_id,
                                   caption="👋 Привіт! <b>Раді, що ти тут!</b> Якщо ти дивишся це відео, значить, "
                                           "прагнеш зрозуміти свій поклик. І це чудово! 🎯\n"
                                           "\n<b>М4 Інтенсив</b> – це 90 днів практичного навчання, що допоможе тобі "
                                           "знайти своє місце в служінні. Ми підтримаємо тебе на цьому шляху та дамо "
                                           "інструменти для впевненого старту.\n"
                                           "\n<b>Як почати?</b>\n"
                                           "\n🔹 <b>Щоб впевнитися, що це для тебе</b> – переглянь інформацію під "
                                           "відео: про нас, програму курсу, відгуки учасників. Досліджуй та "
                                           "приймай рішення!\n"
                                           "🔹 <b>Готовий зробити крок?</b> Натискай 'Зареєструватися', заповнюй "
                                           "форму та ставай частиною нашої спільноти! 🚀",
                                   reply_markup=sm.main_regicter_inline_markup)


@dp.callback_query(F.data == 'program')
async def program(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAMZZ_4ffRb-4wwwN5PZxv8pPmvQ6w8AAvHnMRvA6vBLsvQsDJcXcN8BAAMCAAN5AAM2BA")

    video_id = "BAACAgIAAxkBAAMLZ_4O6rwwWwIQb7nR5hgedfXVyswAAgxjAALA6vBLY45jfA26hWM2BA"
    await callback.message.answer_video(video_id)

    await callback.message.answer(program_text,
                                  reply_markup=sm.program_go_back_inline_markup)


@dp.callback_query(F.data == 'program_go_back')
async def program_go_back(callback: CallbackQuery):
    await callback.answer()
    video_id = "BAACAgIAAxkBAAMHZ_4NV3G2jd1j467XUGOBjH32jP4AAgNjAALA6vBL7VJJ5eTLNM42BA"
    await callback.message.answer_video(video_id,
                                        caption="👋 Привіт! <b>Раді, що ти тут!</b> Якщо ти дивишся це відео, "
                                                "значить, прагнеш"
                                                " зрозуміти свій поклик. І це чудово! 🎯\n"
                                                "\n<b>М4 Інтенсив</b> – це 90 днів практичного навчання, що допоможе"
                                                " тобі знайти своє місце в служінні. Ми підтримаємо тебе на цьому шляху"
                                                " та дамо інструменти для впевненого старту.\n"
                                                "\n<b>Як почати?</b>\n"
                                                "\n🔹 <b>Щоб впевнитися, що це для тебе</b> – переглянь інформацію"
                                                " під відео: про нас, програму курсу, відгуки учасників. Досліджуй"
                                                " та приймай рішення!\n"
                                                "🔹 <b>Готовий зробити крок?</b> Натискай 'Зареєструватися', заповнюй"
                                                " форму та ставай частиною нашої спільноти! 🚀",
                                        reply_markup=sm.main_regicter_inline_markup)


@dp.callback_query(F.data == 'why_need')
async def why_need(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer_photo(
        photo='AgACAgIAAxkBAAMbZ_4gX8-3E7yQuEhMw_oe5TgoFQIAAvTnMRvA6vBLweglqVmEeB8BAAMCAAN5AAM2BA')

    video_id = 'BAACAgIAAxkBAAMNZ_4PMicufFlEHjlzJBwr5mq0qLIAAg1jAALA6vBL8V68THZ-K6M2BA'
    await callback.message.answer_video(video_id)

    await callback.message.answer(why_need_text,
                                  reply_markup=sm.program_go_back_inline_markup)


@dp.callback_query(F.data == 'register')
async def register(callback: CallbackQuery):
    await callback.answer()
    video_id = 'BAACAgIAAxkBAAMJZ_4OATNtScGjDGNekhizgk3Q630AAghjAALA6vBLmmkJXgv6M402BA'
    await callback.message.answer_video(video_id,
                                        caption='🎉 Ти на крок ближче до змін! Зараз важливо визначитися: чи готовий'
                                                ' ти інвестувати час у своє покликання?\n'
                                                '\n<b>Що потрібно знати?</b>\n'
                                                '✅ <b>Цінність навчання – 145$</b>, але для українців діє'
                                                ' спецпропозиція – <b>500 грн</b>. Ми встановили мінімальну оплату, '
                                                'щоб долучалися лише ті, хто серйозно налаштований навчатися й'
                                                ' застосовувати знання на практиці.'
                                                '\n✅ <b>Перед стартом прийми умови</b> – це гарантія якісного'
                                                ' навчання.\n'
                                                '\n<b>Як приєднатися?</b>\n'
                                                '\n1️⃣ <b>Прочитай умови</b> – натисни "Прочитати умови".\n'
                                                '2️⃣ <b>Підтвердь згоду</b> – натисни "Прийняти умови".\n'
                                                '3️⃣ <b>Заповни форму</b> та залиш e-mail.\n'
                                                '4️⃣ <b>Оплати курс</b> – швидко та безпечно через WayForPay.\n'
                                                '\n🚀 Якщо ти готовий діяти – почнемо просто зараз!',
                                        reply_markup=sm.register_inline_markup)


@dp.callback_query(F.data == 'go_back_register')
async def go_back_register(callback: CallbackQuery):
    await callback.answer()
    video_id = 'BAACAgIAAxkBAAMJZ_4OATNtScGjDGNekhizgk3Q630AAghjAALA6vBLmmkJXgv6M402BA'
    await callback.message.answer_video(video_id,
                                        caption='🎉 Ти на крок ближче до змін! Зараз важливо визначитися: чи готовий'
                                                ' ти інвестувати час у своє покликання?\n'
                                          '\n<b>Що потрібно знати?</b>\n'
                                          '✅ <b>Цінність навчання – 145$</b>, але для українців діє спецпропозиція – '
                                          '<b>500 грн</b>. Ми встановили мінімальну оплату, щоб долучалися лише '
                                          'ті, хто серйозно налаштований навчатися й застосовувати знання на практиці.'
                                          '✅ \n<b>Перед стартом прийми умови</b> – це гарантія якісного навчання.\n'
                                          '\n<b>Як приєднатися?</b>\n'
                                          '\n1️⃣ <b>Прочитай умови</b> – натисни "Прочитати умови".\n'
                                          '2️⃣ <b>Підтвердь згоду</b> – натисни "Прийняти умови".\n'
                                          '3️⃣ <b>Заповни форму</b> та залиш e-mail.\n'
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
        await callback.message.answer('🎉 Ти майже готовий розпочати навчання! Щоб отримати доступ, нам потрібен'
                                      ' твій e-mail – Telegram дозволяє надсилати матеріали лише зареєстрованим'
                                      ' у системі користувачам.\n'
                                      '\n<b>Що потрібно зробити?</b>\n'
                                      '\n✉️ <b>Введи свій e-mail</b> у поле нижче. Запиши його, щоб не забути!\n'
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
        "🎯 Ти майже на старті! Залишився важливий крок – заповнити анкету. Це обов’язкова умова для"
        " реєстрації та доступу до курсу.\n"
        "\nАнкета допоможе нам краще зрозуміти твої потреби та зробити навчання більш цінним для тебе. А для тебе – це"
        " можливість усвідомити свої цілі та отримати максимальну користь\n"
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
    await callback.message.answer("🎯 Ти майже на старті! Залишився важливий крок – заповнити анкету."
                                  " Це обов’язкова умова для реєстрації та доступу до курсу.\n"
                                  "\nАнкета допоможе нам краще зрозуміти твої потреби та зробити навчання більш цінним"
                                  " для тебе. А для тебе – це можливість усвідомити свої цілі та отримати"
                                  " максимальну користь\n"
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
    await callback.message.answer("🎯 Ти майже на старті! Залишився важливий крок – заповнити анкету."
                                  " Це обов’язкова умова для реєстрації та доступу до курсу.\n"
                                  "\nАнкета допоможе нам краще зрозуміти твої потреби та зробити навчання більш цінним"
                                  " для тебе. А для тебе – це можливість усвідомити свої цілі та отримати"
                                  " максимальну користь\n"
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
    video_id = 'BAACAgIAAxkBAAMPZ_4Ps87vEG8mEXzRwtQ2bbJ08HUAAhFjAALA6vBL0sd6YDDWayA2BA'
    await callback.answer()
    user = await AsyncDB.get_user(callback.message.chat.id)
    await callback.message.answer_video(video_id,
                                        caption="🎉 <b>Вітаємо на навчанні!</b>\n"
                                                "\nТи зробив важливий крок, і ми раді вітати тебе у цій подорожі!"
                                                " Відкритість до нового – це ключ до зростання. Цей курс допоможе тобі"
                                                " розкрити своє покликання та використати знання для служіння."
                                                "\n\n<b>🔹 Як отримати максимум?</b> "
                                                "\n\n✅ Постав собі за мету взяти все, що може дати це навчання."
                                                "\n✅ Пройди всі 6 модулів у встановлені терміни – кожен модуль триває"
                                                " 2 тижні."
                                                "\n✅ Будь активним у навчанні, став запитання та взаємодій зі"
                                                " спільнотою."
                                                "\n\n💡 <b>Досліди меню, щоб легко орієнтуватися та рухатися вперед!</b>"
                                                "\n\n🎯 <b>Ти готовий? Починай навчання вже зараз!</b>",
                                        reply_markup=sm.main_menu(user.is_admin))


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
                    amount=f'{AMOUNT}',
                    currency='UAH',
                    productNames=["Оплата за курс M4"],
                    productPrices=[AMOUNT],
                    productCounts=[1],
                    orderID=f"M4-{tel_id}-{0 if payment_number is None else payment_number + 1}"
                )
                if res.reason == 'Duplicate Order ID':
                    res = wfp.create_invoice(
                        merchantAccount=MERCHANT_ACCOUNT,
                        merchantAuthType='SimpleSignature',
                        amount=f'{AMOUNT}',
                        currency='UAH',
                        productNames=["Оплата за курс M4"],
                        productPrices=[AMOUNT],
                        productCounts=[1],
                        orderID=f"M4-{tel_id}-{0 if payment_number is None else payment_number + 2}"
                    )
                link = res.invoiceUrl
                if link is not None:
                    await bot.send_message(tel_id, pay_text, reply_markup=sm.pay_keyb(link))
                    return

    await bot.send_message(tel_id, not_registered_yet, reply_markup=sm.form_inline_markup)


@dp.message(F.text == "Корисне")
async def people(message: Message):
    inline_button = [
        [
            InlineKeyboardButton(text=f"M4Ukraine", url="https://choko.link/M4Ukraine")
        ]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_button)
    # Отправляем сообщение с кнопкой
    await message.answer("📌 <b>Корисне – розвивайся разом із нами!</b> 🚀"
                         "\n\nХочеш більше <b>натхнення, знань і підтримки</b>? Ми зібрали все,"
                         " що допоможе тобі <b>зростати та впевнено рухатися у покликанні.</b>\n"
                         "\n🌱 <b>Що тут є?</b>"
                         "\n 🔹 <b>YouTube</b> – практичні відео про заснування церков."
                         "\n 🔹 <b>Pastory</b> – інтерв’ю з пасторами про їхній шлях і виклики."
                         "\n 🔹 <b>Instagram</b> – мотивація, новини та реальні історії."
                         "\n\n📢 <b>Приєднуйся та зростай!</b> 🔥"
                         "\n\n🔗 <b>Усі ресурси тут:</b>",
                         reply_markup=inline_keyboard)


@dp.message(F.text == "Підтримка")
async def people(message: Message):
    inline_button = [
        [
            InlineKeyboardButton(text=f"Підтримка", url="https://t.me/m4_intensive")
        ]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_button)
    # Отправляем сообщение с кнопкой
    await message.answer("💬 <b>Потрібна допомога?</b>\n"
                         "\n🔍 <b>Спочатку переглянь 'Питання-відповіді'</b> – там уже є відповіді"
                         " на найпоширеніші запити. Це зекономить твій час!"
                         "\n\n👉 <b>Перейти до питань-відповідей:</b>"
                         " https://telegra.ph/Pitannya-v%D1%96dpov%D1%96d%D1%96-03-12"
                         "\n\nЯкщо не знайшов відповіді – <b>напиши нам.</b> 📩 Але будь ласка, <b>май терпіння</b>,"
                         " відповідь може зайняти трохи часу."
                         "💬 <b>Звернутися в підтримку:</b>",
                         reply_markup=inline_keyboard)


@dp.message(F.text == "Публічний договір")
async def people(message: Message):
    inline_button = [
        [
            InlineKeyboardButton(text=f"Телеграф",
                                 url="https://telegra.ph/Publ%D1%96chna-oferta-na-koristuvannya-poslugami-chat-bota-z-navchalnimi-kursami-02-27")
        ]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_button)
    # Отправляем сообщение с кнопкой
    await message.answer("📄 <b>Публічний договір – знай свої права!</b>\n"
                         "\nТи вже проходиш навчання, а отже, погодився з його умовами. 📜 У договорі вказано"
                         " <b>твої права, обов’язки, правила користування матеріалами та політику"
                         " повернення коштів.</b>"
                         "\n\n⚖ <b>Основне:</b>"
                         "\n ✅ Як використовувати навчальні матеріали."
                         "\n ✅ Твої права та обов’язки."
                         "\n ✅ Умови повернення коштів."
                         "\n\n📌 <b>Ознайомся з документом, щоб усе було зрозуміло!</b>"
                         "\n\n👉 <b>Перейти до публічного договору:</b>",
                         reply_markup=inline_keyboard)


@dp.message(F.text == "Спільнота")
async def people(message: Message):
    inline_button = [
        [
            InlineKeyboardButton(text=f"Спільнота", url="https://t.me/+jHR9xirMMaMzMDBi")
        ]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_button)
    # Отправляем сообщение с кнопкой
    await message.answer("🤝 <b>Спільнота – твоя підтримка та зростання!</b> 🚀"
                         "\n\nТи не один у своєму покликанні! У закритій <b>онлайн-спільноті</b> ти "
                         "знайдеш <b>підтримку, натхнення та ексклюзивні матеріали,</b> які допоможуть тобі рости."
                         "\n\n🔥 <b>Що тут є?</b>"
                         "\n ✅ Однодумці, які розуміють твій шлях."
                         "\n ✅ Матеріали, яких немає в курсі."
                         "\n ✅ Поради та відповіді на важливі питання."
                         "\n ✅ Місце, де можна ділитися досвідом, викликами та перемогами."
                         "\n\n📢 <b>Приєднуйся та зростай разом із нами!</b> 💪✨"
                         "\n 🔗 <b>Долучайся до спільноти:</b>",
                         reply_markup=inline_keyboard)


@dp.message(F.text == "Питання-відповіді")
async def people(message: Message):
    inline_button = [
        [
            InlineKeyboardButton(text=f"Питання-відповіді 📌",
                                 url="https://telegra.ph/Pitannya-v%D1%96dpov%D1%96d%D1%96-03-12")
        ]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_button)
    # Отправляем сообщение с кнопкой
    await message.answer("❓ <b>Питання та відповіді – знайди рішення швидко!</b>"
                         "\n\nПеред тим як писати в підтримку, <b>переглянь цей розділ</b> – відповідь уже може"
                         " бути тут! \n🔍 Ми зібрали найпоширеніші запити, щоб ти міг <b>отримати рішення без"
                         " очікування.</b>"
                         "\n\n⚡ <b>Чому це зручно?</b>"
                         "\n ✅ Відповідь одразу, без листування."
                         "\n ✅ Вчишся самостійно розбиратися з питаннями."
                         "\n ✅ Розділ оновлюється – можливо, твоє питання скоро з’явиться тут."
                         "\n\n📌 <b>Перейти до питань-відповідей:</b> "
                         "\n\nЯкщо рішення ще немає – повертайся пізніше, ми над цим працюємо! 🚀",
                         reply_markup=inline_keyboard)


@dp.message(F.text == "Навчання 📚")
async def study(message: Message):
    user = await AsyncDB.get_user(message.chat.id)

    # ДЛЯ АДМИНА
    if user and user.is_admin:
        keyboard = sm.get_module_keyboard(6)  # Все уроки открыты
        await message.answer("Оберіть модуль (адміністратор):", reply_markup=keyboard)
        return


    if not user:
        await message.answer("Вы не зарегистрированы.")
        return
    if await check_user(message.chat.id):
        keyboard = sm.get_module_keyboard(getattr(user, "current_module", 1) or 1)
        await message.answer("Оберіть модуль:", reply_markup=keyboard)


@dp.message(F.text == 'Як навчатися?')
async def study_how(message: Message):

    await message.answer(how_learn,
                         reply_markup=sm.module_back_buttons_keyboard)


@dp.message(lambda message: message.text.startswith('Модуль'))
async def handle_module(message: Message):
    tel_id = message.chat.id
    if await check_user(message.chat.id):
        module_number = int(message.text.split(" ")[1])  #Получаем номер модуля

        # ДЛЯ АДМИНА
        user = await AsyncDB.get_user(tel_id)
        if user and user.is_admin:
            keyboard = get_lesson_keyboard(6)  # Все уроки открыты
            await message.answer("Оберіть урок (адміністратор):", reply_markup=keyboard)
            return

        dostup_module = await get_dostup_module_index(tel_id)

        if module_number > dostup_module:
            module_start_date = await AsyncDB.get_module_start_date(message.chat.id)

            if not user:
                await message.answer("Вы не зарегистрированы.")
                return

            if module_start_date:
                module_start_date = module_start_date.date() if isinstance(module_start_date,
                                                                           datetime) else module_start_date
                days_passed = (datetime.now().date() - module_start_date).days
                days_left = 15 - days_passed

                if days_passed < 15:

                    back_to_main_menu = ReplyKeyboardMarkup(
                        keyboard=[
                            [KeyboardButton(text="Головне меню")]
                        ],
                        resize_keyboard=True
                    )
                    await message.answer(f"Наступний модуль буде відкрито через {days_left} днів.",
                                         reply_markup=back_to_main_menu)
                    return
        else:
            await AsyncDB.update_user_progress_module(tel_id, module_number)

            current_module = await AsyncDB.get_user_current_module(tel_id)
            await AsyncDB.check_module_data(tel_id, module_number)

            select_module = await AsyncDB.get_user_progress_current_module(tel_id)
            select_lesson = await AsyncDB.get_user_progress_current_lesson(tel_id)

            if select_module == current_module:
                # await AsyncDB.update_current_lesson(tel_id, 1)
                current_lesson = await AsyncDB.get_current_lesson(tel_id)
                lesson_data = await get_lesson_data_json(current_module,  current_lesson)
                # print("lesson_data:", lesson_data)
                video_data = lesson_data["video_module"]
                # Получаем видео по текущему индексу
                video_to_send = video_data[0]
                await message.answer(f"{video_to_send['title1']}")
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
            else:
                user = await AsyncDB.get_user_by_telegram_id(message.chat.id)

                if user:
                    # await AsyncDB.update_current_lesson(tel_id, 6)

                    user = await AsyncDB.get_user(message.chat.id)

                    if not user:
                        await message.answer("Вы не зарегистрированы.")
                        return

                    keyboard = get_lesson_keyboard(6)
                    await message.answer("Оберіть урок:", reply_markup=keyboard)


# Обработчик для кнопки "Урок"
@dp.message(lambda message: message.text.startswith('Урок'))
async def handle_lesson(message: Message):
    tel_id = message.chat.id
    if await check_user(message.chat.id):
        lesson_number = int(message.text.split(" ")[1])
        module_number = await AsyncDB.get_user_progress_current_module(tel_id)
        current_module = await AsyncDB.get_user_current_module(tel_id)
        current_lesson = await AsyncDB.get_current_lesson(tel_id)

        user = await AsyncDB.get_user(tel_id)

        # ДЛЯ АДМИНА
        if user and user.is_admin:
            lesson_data = await get_lesson_data_json(module_number, lesson_number)
            if lesson_data:
                await message.answer(f'{lesson_data.get("title")}')
                for i, video_to_send in enumerate(lesson_data['video']):
                    video_id = video_to_send.get("video_id")
                    await message.answer_video(
                        video_id,
                        caption=f"{video_to_send['title']}\nВідео {i+1}/{len(lesson_data['video'])}"
                    )
                await message.answer("Ось усі відео з цього уроку.", reply_markup=sm.lesson_6_back_buttons_keyboard)
                return

        await AsyncDB.update_user_progress_lesson(tel_id, lesson_number)
        lesson_data = await get_lesson_data_json(module_number, lesson_number)

        if not lesson_data:
            await message.answer("Не удалось найти данные об уроке.")
            return

        test_scores = await AsyncDB.get_all_test_scores(tel_id, module_number, lesson_number)
        passed_tests = [score for score in test_scores if score is not None and score >= 80]

        for index, video_to_send in enumerate(lesson_data["video"]):
            video_id = video_to_send.get("video_id")
            caption = f"{lesson_data.get('title')}\n\nВідео {index + 1}/{len(lesson_data['video'])}\n\n{video_to_send['title']}"

            print(index)
            await AsyncDB.update_current_index_user_progress(tel_id, index + 1)
            current_index = await AsyncDB.get_current_index_user_progress(tel_id)
            print(current_index)
            print(index)
            if index < len(passed_tests):
                # Видео уже просмотрено и тест сдан — просто показать видео и текст
                await message.answer_video(video=video_id, caption=caption)
            elif index == len(passed_tests):
                # Текущее видео для прохождения с тестом
                test_data = lesson_data.get("tests", [])
                if index < len(test_data):
                    test_url = test_data[index]["url"]
                    test_title = test_data[index]["test_id"]

                    inline_button = InlineKeyboardButton(text=f"{test_title}", url=test_url)
                    inline_button2 = InlineKeyboardButton(text=f"Далі ➡️", callback_data="next_lesson_part")
                    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_button], [inline_button2]])

                    await message.answer_video(video=video_id, caption=caption, reply_markup=inline_keyboard)
                    return
                else:
                    back_markup = sm.lesson_back_buttons_keyboard if lesson_number != 6 else sm.lesson_6_back_buttons_keyboard
                    await message.answer("Ось усі відео з цього уроку.", reply_markup=back_markup)


@dp.callback_query(F.data == 'next_lesson_part')
async def front_of_menu(callback: CallbackQuery):
    tel_id = callback.message.chat.id
    if await check_user(tel_id):
        _up_ = await AsyncDB.get_user_progress(tel_id)
        up = dict(json.loads(_up_.progress))
        module_number = _up_.select_module
        lesson_number = _up_.select_lesson
        current_index = await AsyncDB.get_current_index_user_progress(tel_id)

        print(current_index)

        test_result = up[f"module{module_number}"][f"lesson{lesson_number}"].get(str(current_index))
        print(test_result)
        if test_result is not None:
            if int(test_result) < 80:
                lesson_data = await get_lesson_data_json(module_number, lesson_number)
                test_data = lesson_data.get("tests", [])
                test_url = test_data[current_index - 1]["url"]
                test_title = test_data[current_index - 1]["test_id"]
                inline_button = InlineKeyboardButton(text=f"{test_title}", url=test_url)
                inline_button2 = InlineKeyboardButton(text=f"Далі ➡️", callback_data="next_lesson_part")
                inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_button], [inline_button2]])
                await bot.send_message(tel_id, failed_test, reply_markup=inline_keyboard)
            else:
                await AsyncDB.update_current_index_user_progress(tel_id, current_index + 1)
                await handle_next_button(callback.message)
        else:
            user = await AsyncDB.get_user(tel_id)
            lesson_data = await get_lesson_data_json(module_number, lesson_number)
            test_data = lesson_data.get("tests", [])
            test_url = test_data[current_index - 1]["url"]
            test_title = test_data[current_index - 1]["test_id"]
            inline_button = InlineKeyboardButton(text=f"{test_title}", url=test_url)
            inline_button2 = InlineKeyboardButton(text=f"Далі ➡️", callback_data="next_lesson_part")
            inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_button], [inline_button2]])
            text = test_not_passed.replace('%s', user.email)
            await bot.send_message(tel_id, text=text, reply_markup=inline_keyboard)


async def handle_next_button(message: Message):
    tel_id = message.chat.id
    if await check_user(tel_id):
        module_number = await AsyncDB.get_user_progress_current_module(tel_id)
        lesson_number = await AsyncDB.get_user_progress_current_lesson(tel_id)
        lesson_data = await get_lesson_data_json(module_number, lesson_number)
        current_video_index = await AsyncDB.get_current_video_index(tel_id, module_number, lesson_number)
        curent_test_index = await AsyncDB.get_current_video_index(tel_id, module_number, lesson_number)

        if lesson_data:
            if current_video_index < len(lesson_data['video']):
                video_data = lesson_data["video"]
                video_to_send = video_data[current_video_index]
                first_video_id = video_to_send.get("video_id")
                if first_video_id:
                    test_data = lesson_data.get("tests", [])
                    if test_data:
                        test_url = test_data[current_video_index]["url"]
                        test_title = test_data[curent_test_index]["test_id"]
                        inline_button = InlineKeyboardButton(text=f"{test_title}", url=test_url)
                        inline_button2 = InlineKeyboardButton(text=f"Далі ➡️", callback_data="next_lesson_part")
                        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_button], [inline_button2]])

                        await message.answer_video(
                            video=first_video_id,
                            caption=f"{lesson_data.get('title')}\n\nВідео {current_video_index + 1}/{len(video_data)}\n\n{video_to_send['title']}",
                            reply_markup=inline_keyboard
                        )
                else:
                    await message.answer("Гарна робота! Урок завершено ✅ Продовжуй далі)", reply_markup=sm.get_next_lesson_keyboard())
            else:
                current_module = await AsyncDB.get_user_current_module(tel_id)
                current_lesson = await AsyncDB.get_current_lesson(tel_id)
                if current_lesson == 6:
                    lesson_data = await get_lesson_data_json(current_module, current_lesson)
                    video_data = lesson_data["video_module"]
                    video_to_send = video_data[0]
                    video_id = video_to_send.get("video_id")
                    await message.answer_video(video_id, caption=f"{video_to_send['title2']}", reply_markup=sm.next_module_markup)
                else:
                    await message.answer("Гарна робота! Урок завершено ✅ Продовжуй далі)", reply_markup=sm.get_next_lesson_keyboard())
        else:
            current_module = await AsyncDB.get_user_current_module(tel_id)
            current_lesson = await AsyncDB.get_current_lesson(tel_id)
            if current_lesson == 6:
                lesson_data = await get_lesson_data_json(current_module, current_lesson)
                video_data = lesson_data["video_module"]
                video_to_send = video_data[0]
                video_id = video_to_send.get("video_id")
                await message.answer_video(video_id, caption=f"{video_to_send['title2']}", reply_markup=sm.next_module_markup)


@dp.message(F.text == "Повернутися до уроків🔙")
async def back_to_lessons(message: Message):
    # Получаем пользователя из БД по telegram_id
    user = await AsyncDB.get_user(message.chat.id)

    # ДЛЯ АДМИНА
    if user and user.is_admin:
        keyboard = get_lesson_keyboard(6)  # Все уроки открыты
        await message.answer("Оберіть урок (адміністратор):", reply_markup=keyboard)
        return

    if user:
        user = await AsyncDB.get_user(message.chat.id)

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        keyboard = get_lesson_keyboard(6)
        await message.answer("Оберіть урок:", reply_markup=keyboard)
    else:
        await message.answer("Пользователь не найден в базе данных.")


@dp.message(lambda message: message.text == "Наступний урок")
async def handle_next_lesson(message: Message):
    tel_id = message.chat.id
    if await check_user(tel_id):
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
    video_id = 'BAACAgIAAxkBAAMPZ_4Ps87vEG8mEXzRwtQ2bbJ08HUAAhFjAALA6vBL0sd6YDDWayA2BA'
    user = await AsyncDB.get_user(message.chat.id)
    await message.answer_video(video_id,
                               caption="🎉 <b>Вітаємо на навчанні!</b>\n"
                                 "\nТи зробив важливий крок, і ми раді вітати тебе у цій подорожі! Відкритість до нового – це ключ до зростання. Цей курс допоможе тобі розкрити своє покликання та використати знання для служіння."
                                 "\n\n<b>🔹 Як отримати максимум?</b> "
                                 "\n\n✅ Постав собі за мету взяти все, що може дати це навчання."
                                 "\n✅ Пройди всі 6 модулів у встановлені терміни – кожен модуль триває 2 тижні."
                                 "\n✅ Будь активним у навчанні, став запитання та взаємодій зі спільнотою."
                                 "\n\n💡 <b>Досліди меню, щоб легко орієнтуватися та рухатися вперед!</b>"
                                 "\n\n🎯 <b>Ти готовий? Починай навчання вже зараз!</b>",
                               reply_markup=sm.main_menu(user.is_admin))


@dp.message(F.text == "🔙Модулі")
async def back_to_lessons(message: Message):
    user = await AsyncDB.get_user(message.chat.id)
    # ДЛЯ АДМИНА
    if user and user.is_admin:
        keyboard = sm.get_module_keyboard(6)  # Все уроки открыты
        await message.answer("Оберіть модуль (адміністратор):", reply_markup=keyboard)
        return

    keyboard = sm.get_module_keyboard(getattr(user, "current_module", 1))
    await message.answer("Ви повернулись до модулів:", reply_markup=keyboard)


@dp.message(F.text == "Наступний модуль")
async def next_module(message: Message):
    user = await AsyncDB.get_user(message.chat.id)
    tel_id = message.chat.id
    if await check_user(tel_id):
        if user.current_module == 6:
            current_module = await AsyncDB.get_user_current_module(tel_id)
            new_module = current_module + 1
            await AsyncDB.update_current_module(tel_id, new_module)
            video_id = "BAACAgIAAxkBAAPQZ_47oZIPI2-ZcSdzZsiKRfGCkmEAApxlAALA6vBL3qsoDDIa3k02BA"
            await message.answer_video(video_id,
                                       caption="<b>Вітаємо!</b> 🎉 "
                                               "\n\nТи пройшов важливий шлях, отримав нові знання та навички, розкрив своє"
                                               " покликання у Божій історії. Незалежно від того, ким ти себе бачиш – <b>"
                                               "засновником церкви, частиною команди або лідером у своїй громаді,</b> "
                                               "– тепер ти <b>готовий діяти.</b>"
                                               "\n\n💡 <b>Що далі?</b>"
                                               "\n ✅ Використовуй усе, що дізнався – у своїй церкві, служінні, команді,"
                                               " сім’ї."
                                               "\n ✅ Відчуваєш поклик до заснування церкви? <b>Не зволікай!</b>"
                                               " Зроби перший крок!"
                                               "\n ✅ Залишайся на зв’язку з нашою командою, приєднуйся до спільноти та"
                                               " конференцій."
                                               "\n\n🎁<b>Маємо подарунок для тебе!</b>"
                                               "\nЩоб отримати <b>сертифікат</b> про завершення курсу та <b>особливий"
                                               " подарунок</b> від нас, напиши в чат підтримки!"
                                               "\n\n🙏 <b>Ми молимося за тебе і благословляємо твій шлях!</b> Нехай Бог"
                                               " веде тебе у твоєму покликанні, а ти <b>рухайся вперед із вірою та"
                                               " впевненістю!</b>"
                                               "\n\n<b>Ти круто попрацював – тепер час діяти!</b> 🚀🔥",
                                       reply_markup=sm.main_menu(user.is_admin))
            return
        module_start_date = await AsyncDB.get_module_start_date(message.chat.id)

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        if module_start_date:
            module_start_date = module_start_date.date() if isinstance(module_start_date, datetime) else module_start_date
            days_passed = (datetime.now().date() - module_start_date).days
            days_left = 15 - days_passed

            if days_passed < 15:
                current_module = await AsyncDB.get_user_current_module(tel_id)
                new_module = current_module + 1
                await AsyncDB.update_current_module(tel_id, new_module)
                keyboard = get_lesson_keyboard(getattr(user, "current_lesson", 1))
                await message.answer(f"Наступний модуль буде відкрито через {days_left} днів.",
                                     reply_markup=keyboard)
                return
            else:
                await message.answer("Наступний модуль не відкрито",
                                     reply_markup=sm.main_menu(user.is_admin))


# @dp.message(F.text == "ADMIN")
# async def next_module(message: Message):
#     tel_id = message.chat.id
#     user = await AsyncDB.get_user(tel_id)
#     if user.is_admin == 1:



async def check_modules():
    """Проверяет пользователей и открывает новый модуль, если прошло 15 дней."""
    users = await AsyncDB.get_all_users()  # Получаем всех пользователей

    updated_users = []  # Список пользователей, которым обновим модуль

    for user in users:
        module_start_date = user.get("module_start_date")
        current_module = user.get("current_module")
        dostup_module = await get_dostup_module_index(user["tel_id"])
        new_module = dostup_module + 1
        if not module_start_date:
            continue  # Пропускаем, если у пользователя нет даты старта

        module_start_date = module_start_date.date() if isinstance(module_start_date, datetime) else module_start_date
        days_passed = (datetime.now().date() - module_start_date).days

        if days_passed >= 15 and current_module > dostup_module:
            await AsyncDB.update_current_lesson(user["tel_id"], 1)
            await update_dostup_module_index(user["tel_id"], new_module)
            await AsyncDB.update_module_start_date(user["tel_id"])


async def daily_texts():
    """Рассылка ежедневных каких-то сообщений """
    users = await AsyncDB.get_all_users_in_model()
    for user in users:
        if user.is_blocked != 1:
            if user.current_module >= 1:
                module_date = datetime.strptime(str(user.module_start_date),
                                                "%Y-%m-%d %H:%M:%S").date()  # Получаем только дату
                today = date.today()  # Текущая дата
                days_difference = (today - module_date).days  # разница дат
                if days_difference in {2, 4, 6, 8, 10, 12, 14}:
                    text = MODULES_TEXTS[f"module{user.current_module}"][str(int(days_difference/2))]
                    await bot.send_message(user.tel_id, text=text, disable_notification=True)


def block_inactive_users_sync():
    loop = asyncio.get_running_loop()
    loop.create_task(block_inactive_users())


def check_modules_sync():
    loop = asyncio.get_running_loop()
    loop.create_task(check_modules())


def daily_texts_sync():
    loop = asyncio.get_running_loop()
    loop.create_task(daily_texts())


async def scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)


async def main():
    schedule.every().day.at("03:59").do(block_inactive_users_sync)
    schedule.every().day.at("04:09").do(check_modules_sync)
    schedule.every().day.at("04:19").do(daily_texts_sync)

    asyncio.create_task(scheduler())

    # Удаляем webhook, чтобы избежать конфликта
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
