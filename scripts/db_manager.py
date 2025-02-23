import aiomysql
from scripts.config import DB_CONFIG
from scripts.models import User


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
    async def create_user(telegram_id: int, name: str, email: str, context: str = ""):
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO users (tel_id, name, email, context, is_blocked, is_admin, last_date)"
                    " VALUES (%s, %s, %s, %s, %s, %s, NOW())",
                    (telegram_id, name, email, context, False, False)
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
    async def update_modules():
        async with (await AsyncDB.get_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    UPDATE users 
                    SET current_module = current_module + 1, 
                        module_start_date = NOW()
                    WHERE DATEDIFF(NOW(), module_start_date) >= 15
                        AND current_module < 6
                """)
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


async def block_inactive_users():
    async with aiomysql.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                UPDATE users 
                SET is_blocked = TRUE 
                WHERE DATEDIFF(NOW(), last_date) > 14
            """)
            await conn.commit()
