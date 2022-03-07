from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .script import cesar, alpha
from database import db

from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
import time
import random
import threading


@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await message.answer(f"Отправь мне любой текст, {message.from_user.get_mention(as_html=True)}\n\n"
                         f"<b>Как пользоваться ботом - /help</b>")
    db.add_user(message.from_user.id)
    db.backup_copy()


def key():
    while True:
        
        with open("key.txt", "w") as file:
            k = random.randint(0, alpha.count-1)
            file.write(str(k))
            cesar.key = int(k)
        time.sleep(60*60)


threading.Thread(target=key).start()

keyboard_error = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="На случай ошибки", callback_data="error"),
            ]
        ]
    )

keyboard = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔏", callback_data="to"),
                InlineKeyboardButton("❌", callback_data="delete"),
                InlineKeyboardButton(text="🔓", callback_data="from"),

            ]
        ]
    )


@dp.callback_query_handler(text="error")
async def error_text(call: types.CallbackQuery):
    await call.answer("Сделаем вид будто этого не было", show_alert=True)
    await call.message.delete()


@dp.message_handler()
async def simple_text(message: types.Message):
    text = str(message.text).lower()
    await message.delete()
    for liter in text:
        if liter not in alpha.alphabet:
            await message.answer(f"Такой символ нельзя: {liter}", reply_markup=keyboard_error)
            return None

    try:
        await message.answer(f"<pre>{text}</pre>", reply_markup=keyboard, parse_mode=None)
    except Exception as err:
        await message.answer(f"Вылезла ошибочка:\n<b>{err}</b>", reply_markup=keyboard_error)


@dp.callback_query_handler(text="delete")
async def to_cesar(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()


@dp.callback_query_handler(text="to")
async def to_cesar(call: types.CallbackQuery):
    await call.answer()
    text = call.message.text
    to_ces = cesar.to_cesar(text)
    await call.message.edit_text(f"<pre>{to_ces}</pre>", reply_markup=keyboard)


@dp.callback_query_handler(text="from")
async def to_cesar(call: types.CallbackQuery):
    await call.answer()
    text = call.message.text
    from_ces = cesar.from_cesar(text)
    await call.message.edit_text(f"<pre>{from_ces}</pre>", reply_markup=keyboard)
