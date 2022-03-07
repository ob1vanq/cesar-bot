from loader import dp
from aiogram.dispatcher.filters import Command

from aiogram import types


@dp.message_handler(Command("help"))
async def help(message: types.Message):
    link = "https://ru.wikipedia.org/wiki/%D0%A8%D0%B8%D1%84%D1%80_%D0%A6%D0%B5%D0%B7%D0%B0%D1%80%D1%8F"
    string = "<b>Как пользоваться ботом?</b>\n\n" \
             "🔏 - <i>Зашифровать сообщение</i>\n" \
             "🔓 - <i>Розшифровать сообщение</i>\n\n" \
             "Бот меняет ключ шифрования каждый час!\n\n" \
             f"Алгоритм <a href ='{link}'> Шифр Цезаря</a>, является один из самых простых " \
             f"и наиболее широко известных методов шифрования.\n\n" \
             f"По всем вопросам:  @engineer_spock" \

    await message.answer(string)
