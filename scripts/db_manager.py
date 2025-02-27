import json
import aiomysql
from aiogram import Bot
from aiogram.client.session import aiohttp

from scripts.config import DB_CONFIG, TOKEN_API
from scripts.models import User
from scripts.models import Lessons

bot = Bot(TOKEN_API)


class AsyncDB:
    @staticmethod
    async def get_connection():
        return await aiomysql.connect(**DB_CONFIG)

    @staticmethod
    async def get_user(telegram_id: int):
        conn = await AsyncDB.get_connection()  # Добавляем await
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM users WHERE tel_id = %s", (telegram_id,))
            result = await cursor.fetchone()

            if result:
                result.pop("id", None)  # Убираем id, если есть
                return User(**result)

        await conn.ensure_closed()  # Закрываем соединение
        return None

    @staticmethod
    async def get_all_users():
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM users")
                return await cursor.fetchall()

    @staticmethod
    async def user_exists(telegram_id: int):
        return bool(await AsyncDB.get_user(telegram_id))

    @staticmethod
    async def create_user(telegram_id: int, name: str, email: str, context: str = "", username=None):
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO users 
                    (tel_id, name, email, context, is_blocked, is_admin, last_date, module_start_date, username) 
                    VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)
                    """,
                    (telegram_id, name, email, context, False, False, username)
                )
                await conn.commit()

    @staticmethod
    async def update_user(telegram_id: int, **kwargs):
        query = ", ".join([f"{key}=%s" for key in kwargs])
        values = list(kwargs.values()) + [telegram_id]
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET {query} WHERE tel_id=%s", values)
                await conn.commit()

    @staticmethod
    async def block_user(telegram_id: int):
        await AsyncDB.update_user(telegram_id, is_blocked=True)

    @staticmethod
    async def get_user_by_telegram_id(tel_id: int):
        query = "SELECT * FROM users WHERE tel_id = %s"
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (tel_id,))
                return await cursor.fetchone()

    @staticmethod
    async def set_module_start_date(telegram_id: int):
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT module_start_date FROM users WHERE tel_id = %s",
                    (telegram_id,)
                )
                result = await cursor.fetchone()

                # Если дата уже есть, не обновляем
                if result and result[0]:
                    return

                # Если даты нет, записываем текущую дату
                await cursor.execute(
                    "UPDATE users SET module_start_date = NOW() WHERE tel_id = %s",
                    (telegram_id,)
                )
                await conn.commit()

    @staticmethod
    async def update_current_module(telegram_id: int, new_module: int):
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE users SET current_module = %s, module_start_date = NOW() WHERE tel_id = %s",
                    (new_module, telegram_id)
                )
                await conn.commit()

    @staticmethod
    async def update_current_lesson(telegram_id: int, new_lesson: int):
        """
        Обновляет поле current_lesson для пользователя с данным telegram_id.
        """
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE users SET current_lesson = %s WHERE tel_id = %s",
                    (new_lesson, telegram_id)
                )
                await conn.commit()

    @staticmethod
    async def get_current_lesson(telegram_id: int):
        """
        Получает текущее значение current_lesson для пользователя с данным telegram_id.
        """
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT current_lesson FROM users WHERE tel_id = %s", (telegram_id,))
                result = await cursor.fetchone()
                return result['current_lesson'] if result else None

    @staticmethod
    # Функция для получения текущего модуля пользователя по telegram_id
    async def get_user_current_module(telegram_id: int):
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    SELECT current_module
                    FROM users
                    WHERE tel_id = %s
                """, (telegram_id,))

                result = await cursor.fetchone()

                if result:
                    return result[0]  # возвращаем current_module
                else:
                    return None

    # //////////////////////////////////////////////////////////////////////
    #     ///////////////////////////////////////////////////////////////////////

    @staticmethod
    async def create_user_progress(telegram_id: int):
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO user_progress (tel_id, name, email, select_module, select_lesson, test_score, completed_at)
                    SELECT tel_id, name, email, 1, 1, 0, NOW()
                    FROM users
                    WHERE tel_id = %s
                    """,
                    (telegram_id,)
                )
                await conn.commit()

    @staticmethod
    async def update_user_progress_module(tel_id: int, select_module: int):
        """Обновляет текущий модуль пользователя в UserProgress"""
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    UPDATE user_progress 
                    SET select_module = %s 
                    WHERE tel_id = %s
                """, (select_module, tel_id))

                await conn.commit()

    @staticmethod
    async def update_user_progress_lesson(tel_id: int, select_lesson: int):
        """Обновляет lesson_id для пользователя в таблице user_progress"""
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Обновляем только lesson_id для конкретного пользователя
                await cursor.execute("""
                    UPDATE user_progress
                    SET select_lesson = %s
                    WHERE tel_id = %s
                """, (select_lesson, tel_id))

                await conn.commit()

    @staticmethod
    async def get_user_progress_current_module(tel_id: int) -> int:
        """Получает текущий модуль пользователя из таблицы users"""
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                # Извлекаем current_module пользователя по его телеграм айди
                await cursor.execute(
                    "SELECT select_module FROM user_progress WHERE tel_id = %s", (tel_id,)
                )
                result = await cursor.fetchone()
                if result:
                    return result[0]  # Получаем первый элемент из кортежа
                return 0  # Если нет записи, возвращаем 0 (например, если пользователь еще не начал)

    @staticmethod
    async def get_user_progress_current_lesson(tel_id: int) -> int:
        """Получает текущий урок пользователя из таблицы users"""
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                # Извлекаем select_lesson пользователя по его телеграм айди
                await cursor.execute(
                    "SELECT select_lesson FROM user_progress WHERE tel_id = %s", (tel_id,)
                )
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0  # Если нет записи, возвращаем 0 (например, если пользователь еще не начал)

    # ////////////////////////////////////////////////////////// работа с уроками
    @staticmethod
    async def is_lesson_completed(tel_id: int, module_id: int, lesson_id: int) -> bool:
        """Проверяет, прошёл ли пользователь указанный урок"""
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT current_module, current_lesson 
                    FROM users 
                    WHERE tel_id = %s
                    """,
                    (tel_id,)
                )
                user = await cursor.fetchone()

                if not user:
                    return False  # Если пользователя нет, считаем урок не пройденным

                current_module, current_lesson = user

                # Если current_module > module_id или (current_module == module_id и current_lesson > lesson_id)
                return (current_module > module_id) or (current_module == module_id and current_lesson > lesson_id)

    @staticmethod
    async def get_user_payments(telegram_id: int):
        conn = await AsyncDB.get_connection()  # Добавляем await
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(f"SELECT * FROM myapp1_payment WHERE order_reference LIKE 'M4-{telegram_id}-%';")
            result = await cursor.fetchall()
            # await conn.ensure_closed()
            return len(result)
        await conn.ensure_closed()  # Закрываем соединение
        return None


# Функция для получения данных урока
async def get_lesson_data(lesson_id: int, module_id: int):
    async with (await AsyncDB.get_connection()) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                SELECT title, video, test_link
                FROM lessons
                WHERE lesson_id = %s AND module_id = %s
            """, (lesson_id, module_id))

            result = await cursor.fetchone()

            if result:
                title, video, test_link = result
                return title, video, test_link
            else:
                return None


async def block_inactive_users():
    async with aiomysql.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                UPDATE users 
                SET is_blocked = TRUE 
                WHERE DATEDIFF(NOW(), last_date) > 14
            """)
            await conn.commit()


# /////////////////////////////////////////
# /////////////////////////////////////////
import aiofiles


# Примерная загрузка данных из файла (если FILE_PATH - путь к файлу)
# def load_data_from_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)
#
#
# # Теперь переменная FILE_PATH содержит данные в формате словаря, а не строки
# FILE_PATH = load_data_from_file('D:\PythonProjects\Bot_M4\lessons.json')

FILE_PATH = 'lessons.json'


# async def get_lesson_data_json(module_id: int, lesson_id: int):
#     """Получает данные об уроке по его ID и модулю из JSON."""
#     try:
#         async with aiofiles.open(FILE_PATH, "r", encoding="utf-8") as file:
#             content = await file.read()
#             data = json.loads(content)
#
#         # Проверяем, есть ли список уроков в данных
#         lessons = data.get("lessons")
#         if not lessons:
#             return None
#
#         # Ищем нужный урок по module_id и lesson_id
#         lesson = next(
#             (
#                 lesson
#                 for lesson in lessons
#                 if lesson.get("module_id") == module_id and lesson.get("lesson_id") == lesson_id
#             ),
#             None,
#         )
#
#         return lesson
#
#     except FileNotFoundError:
#         print(f"Файл {FILE_PATH} не найден.")
#     except json.JSONDecodeError:
#         print(f"Ошибка парсинга JSON в файле {FILE_PATH}.")
#     return None


# Метод для получения текущего индекса видео по module_id и lesson_id
async def get_current_video_index(module_id, lesson_id):
    """Получает текущий индекс видео для урока по module_id и lesson_id."""
    try:
        async with aiofiles.open(FILE_PATH, "r", encoding="utf-8") as file:
            content = await file.read()
            data = json.loads(content)

        # Проверяем, есть ли список уроков в данных
        lessons = data.get("lessons")
        if not lessons:
            return None

        # Ищем урок по module_id и lesson_id
        for lesson in lessons:
            if lesson['module_id'] == module_id and lesson['lesson_id'] == lesson_id:
                return lesson.get('current_video_index')
        return None  # если урок с таким ID и module_id не найден

    except FileNotFoundError:
        print(f"Файл {FILE_PATH} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка парсинга JSON в файле {FILE_PATH}.")
    return None


async def update_current_video_index(module_id, lesson_id, new_index):
    """Обновляет текущий индекс видео для урока по module_id и lesson_id."""
    try:
        async with aiofiles.open(FILE_PATH, "r", encoding="utf-8") as file:
            content = await file.read()
            data = json.loads(content)

        # Проверяем, есть ли список уроков в данных
        lessons = data.get("lessons")
        if not lessons:
            return False  # Если список уроков пуст, возвращаем False

        # Ищем урок по module_id и lesson_id
        for lesson in lessons:
            if lesson['module_id'] == module_id and lesson['lesson_id'] == lesson_id:
                lesson['current_video_index'] = new_index
                # Сохраняем изменения в файл
                async with aiofiles.open(FILE_PATH, "w", encoding="utf-8") as file:
                    await file.write(json.dumps(data, indent=4, ensure_ascii=False))
                return True  # Возвращаем True, если обновление прошло успешно
        return False  # Если урок не найден, возвращаем False

    except FileNotFoundError:
        print(f"Файл {FILE_PATH} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка парсинга JSON в файле {FILE_PATH}.")
    return False


async def update_current_test_index(module_id, lesson_id, new_index):
    """Обновляет текущий индекс теста для урока по module_id и lesson_id."""
    try:
        async with aiofiles.open(FILE_PATH, "r", encoding="utf-8") as file:
            content = await file.read()
            data = json.loads(content)

        # Проверяем, есть ли список уроков в данных
        lessons = data.get("lessons")
        if not lessons:
            return False  # Если список уроков пуст, возвращаем False

        # Ищем урок по module_id и lesson_id
        for lesson in lessons:
            if lesson['module_id'] == module_id and lesson['lesson_id'] == lesson_id:
                lesson['current_test_index'] = new_index
                # Сохраняем изменения в файл
                async with aiofiles.open(FILE_PATH, "w", encoding="utf-8") as file:
                    await file.write(json.dumps(data, indent=4, ensure_ascii=False))
                return True  # Возвращаем True, если обновление прошло успешно
        return False  # Если урок не найден, возвращаем False

    except FileNotFoundError:
        print(f"Файл {FILE_PATH} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка парсинга JSON в файле {FILE_PATH}.")
    return False


async def update_current_video_index_0(module_id, lesson_id):
    """Обновляет текущий индекс видео для урока по module_id и lesson_id."""
    try:
        async with aiofiles.open(FILE_PATH, "r", encoding="utf-8") as file:
            content = await file.read()
            data = json.loads(content)

        # Проверяем, есть ли список уроков в данных
        lessons = data.get("lessons")
        if not lessons:
            return False  # Если список уроков пуст, возвращаем False

        # Ищем урок по module_id и lesson_id
        for lesson in lessons:
            if lesson['module_id'] == module_id and lesson['lesson_id'] == lesson_id:
                lesson['current_video_index'] = 0
                # Сохраняем изменения в файл
                async with aiofiles.open(FILE_PATH, "w", encoding="utf-8") as file:
                    await file.write(json.dumps(data, indent=4, ensure_ascii=False))
                return True  # Возвращаем True, если обновление прошло успешно
        return False  # Если урок не найден, возвращаем False

    except FileNotFoundError:
        print(f"Файл {FILE_PATH} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка парсинга JSON в файле {FILE_PATH}.")
    return False


async def update_current_test_index_0(module_id, lesson_id):
    """Обновляет текущий индекс видео для урока по module_id и lesson_id."""
    try:
        async with aiofiles.open(FILE_PATH, "r", encoding="utf-8") as file:
            content = await file.read()
            data = json.loads(content)

        # Проверяем, есть ли список уроков в данных
        lessons = data.get("lessons")
        if not lessons:
            return False  # Если список уроков пуст, возвращаем False

        # Ищем урок по module_id и lesson_id
        for lesson in lessons:
            if lesson['module_id'] == module_id and lesson['lesson_id'] == lesson_id:
                lesson['current_test_index'] = 0
                # Сохраняем изменения в файл
                async with aiofiles.open(FILE_PATH, "w", encoding="utf-8") as file:
                    await file.write(json.dumps(data, indent=4, ensure_ascii=False))
                return True  # Возвращаем True, если обновление прошло успешно
        return False  # Если урок не найден, возвращаем False

    except FileNotFoundError:
        print(f"Файл {FILE_PATH} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка парсинга JSON в файле {FILE_PATH}.")
    return False


async def get_videos_by_module_lesson(module_id: int, lesson_id: int):
    """Получает все видео по заданному module_id и lesson_id."""
    try:
        async with aiofiles.open(FILE_PATH, "r", encoding="utf-8") as file:
            content = await file.read()
            data = json.loads(content)

        lessons = data.get("lessons", [])
        videos_list = []

        for lesson in lessons:
            if lesson.get("module_id") == module_id and lesson.get("lesson_id") == lesson_id:
                videos = lesson.get("video", [])

                for video in videos:
                    for key, url in video.items():
                        videos_list.append(f"Урок {lesson_id}, Модуль {module_id}: {url}")

        return videos_list

    except FileNotFoundError:
        print(f"Файл {FILE_PATH} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка парсинга JSON в файле {FILE_PATH}.")

    return []
# /////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////
# Качаем видосыыыыыыыыыыыыыыыыыыыы


# # Обработчик для кнопки "Урок"
# @dp.message(lambda message: message.text.startswith('Урок'))
# async def handle_lesson(message: Message):
#     lesson_number = int(message.text.split(" ")[1])  # Получаем номер урока
#     tel_id = message.from_user.id
#     module_number = await AsyncDB.get_user_progress_current_module(tel_id)
#     current_module = await AsyncDB.get_user_current_module(tel_id)
#     current_lesson = await AsyncDB.get_current_lesson(tel_id)
#
#     if module_number == current_module and lesson_number == current_lesson:
#         await update_current_video_index_0(lesson_number, module_number)
#
#         await AsyncDB.update_user_progress_lesson(tel_id, lesson_number)
#
#         lesson_data = await get_lesson_data_json(module_number, lesson_number)
#
#         if lesson_data:
#             first_video = lesson_data["video"][0].get("video_1")  # Первая ссылка на видео
#             first_test_link = lesson_data["test_links"][0].get("test_1")  # Первая ссылка на тест
#
#             # Создаем инлайн кнопку для теста
#             test_button = InlineKeyboardButton(text="Пройти тест", url=first_test_link)
#
#             # Создаем инлайн клавиатуру
#             lesson_keyboard = InlineKeyboardMarkup(inline_keyboard=[[test_button]])
#
#             # Создаем реплай-кнопку для продолжения
#             next_button = KeyboardButton(text="Далі")
#             lesson_keyboard_reply = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[next_button]])
#
#             # Отправляем сообщение с видео и кнопкой
#             await message.answer(
#                 f"Ваше видео для {lesson_data['title']}:\n{first_video}",
#                 reply_markup=lesson_keyboard
#             )
#
#             if not lesson_data:
#                 await message.answer("Урок не найден в базе данных.")
#                 return
#
#             # Получаем индекс текущего видео
#             video_index = lesson_data['current_video_index']
#             await update_current_video_index(module_number, lesson_number, video_index + 1)
#             await update_current_test_index(module_number, lesson_number, video_index + 1)
#             await message.answer("Для перехода к следующему шагу, нажмите 'Далі'.",
#                                  reply_markup=lesson_keyboard_reply)  # Здесь реплай-кнопка)
#         else:
#             await message.answer("Не удалось найти данные об уроке.")
#     else:
#         lesson_data = await get_videos_by_module_lesson(module_number, lesson_number)
#         await message.answer(f'Вот усі відео {lesson_data}',
#                              reply_markup=sm.lesson_back_buttons_keyboard)

async def get_lesson_data_json(module_id: int, lesson_id: int):
    """Получает данные об уроке по его ID и модулю из JSON."""
    try:
        async with aiofiles.open(FILE_PATH, "r", encoding="utf-8") as file:
            content = await file.read()
            data = json.loads(content)

        # Проверяем, есть ли список уроков в данных
        lessons = data.get("lessons")
        if not lessons:
            print("Не найдены уроки в данных JSON.")
            return None

        # Ищем нужный урок по module_id и lesson_id
        lesson = next(
            (
                lesson
                for lesson in lessons
                if lesson.get("module_id") == module_id and lesson.get("lesson_id") == lesson_id
            ),
            None,
        )

        if not lesson:
            print(f"Урок с module_id={module_id} и lesson_id={lesson_id} не найден.")
            return None

        return lesson

    except FileNotFoundError:
        print(f"Файл {FILE_PATH} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка парсинга JSON в файле {FILE_PATH}.")
    return None



# # Обработчик для кнопки "Далі"
# @dp.message(lambda message: message.text == 'Далі')
# async def handle_next_button(message: Message):
#     tel_id = message.from_user.id
#     current_module = await AsyncDB.get_user_progress_current_module(tel_id)
#
#     # Получаем текущий урок пользователя
#     current_lesson_data = await AsyncDB.get_user_progress_current_lesson(tel_id)
#     # Получаем данные урока из JSON
#     lesson_data = await get_lesson_data_json(current_module, current_lesson_data)
#
#     if not current_lesson_data:
#         await message.answer("Урок не найден.")
#         return
#
#     if not lesson_data:
#         await message.answer("Урок не найден в базе данных.")
#         return
#
#     # Получаем индекс текущего видео
#     video_index = lesson_data['current_video_index']
#
#     # Проверяем, есть ли следующее видео
#     if video_index < len(lesson_data['video']):
#         # Получаем ссылку на следующее видео
#         video_url = list(lesson_data['video'][video_index].values())[0]  # получаем ссылку на видео
#         test_index = lesson_data['current_test_index']
#         if test_index < len(lesson_data['test_links']):
#             # Получаем ссылку на следующий тест
#             test_url = list(lesson_data['test_links'][test_index].values())[0]  # получаем ссылку на тест
#             # Создаем инлайн кнопку для теста
#             test_button = InlineKeyboardButton(text="Пройти тест", url=test_url)
#
#             # Создаем инлайн клавиатуру
#             lesson_keyboard = InlineKeyboardMarkup(inline_keyboard=[[test_button]])
#             # Обновляем индекс видео для пользователя
#             await update_current_video_index(current_module, current_lesson_data, video_index + 1)
#             await message.answer_video(f"Смотрите видео: {video_url}",
#                                        reply_markup=lesson_keyboard)
#         else:
#             await message.answer('Ви молодці!')
#     else:
#         await message.answer("Ви молодці приступайте до наступного уроку",
#                              reply_markup=sm.get_next_lesson_keyboard())