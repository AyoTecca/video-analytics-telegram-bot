import os
import logging
import psycopg2

from aiogram import Bot, Dispatcher, executor, types
from llm.query_builder import build_query

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def run_sql(query: str):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(query)

            if not cur.description:
                return None

            rows = cur.fetchall()

            if len(rows) == 1 and len(rows[0]) == 1:
                return rows[0][0]

            return rows


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply(
        "Я отвечаю на аналитические вопросы по видео.\n"
        "Примеры:\n"
        "Сколько всего видео есть в системе?\n"
        "Сколько просмотров было 28 ноября 2025?"
    )


@dp.message_handler()
async def handle_query(msg: types.Message):
    try:
        sql = build_query(msg.text)
        logging.info(f"SQL: {sql}")

        result = run_sql(sql)

        if result is None:
            await msg.reply("0")
        else:
            await msg.reply(str(result))

    except Exception as e:
        logging.exception("Query failed")
        await msg.reply("0")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
