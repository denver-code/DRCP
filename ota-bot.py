import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = "TOKEN"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await msg.reply(msg)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)