from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, bot
from database import db
from data.config import ADMINS


class poster(StatesGroup):
    create = State()
    post = State()


def get_mention(id):
    return f"<a href='tg://user?id={id}'>пользователю</a>"

def keyboard(data: list):
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text=data[0], callback_data=data[-1]),
                InlineKeyboardButton(text="Отмена", callback_data="stop"),
            ]
        ]
    )


keyboard2 = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отправить всем", callback_data="share"),
            InlineKeyboardButton(text="Отмена", callback_data="stop")
        ]
    ]
)


@dp.callback_query_handler(state=(None, poster.post), text="stop")
async def stop_post(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Пост отменен")
    await state.finish()


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = message.from_user.id
        return str(member) in ADMINS


@dp.message_handler(Command("admin"), AdminFilter())
async def statistic(message: types.Message):
    import datetime
    data = datetime.datetime.now().strftime("%H:%M:%S| %d/%m/%y, %A")
    await message.answer(f"<b>{data}</b>\n\nВсего пользователей: {db.count()}",
                         reply_markup=keyboard(["Создать пост", "post"]))


@dp.callback_query_handler(text="post")
async def create_post_message(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Жду текст 👇")
    await poster.create.set()


@dp.message_handler(state=poster.create)
async def create_post(message: types.Message, state: FSMContext):
    text = message.html_text
    await message.answer(text, reply_markup=keyboard2, parse_mode="HTML")
    await poster.post.set()
    await state.set_data(dict(text=text))


@dp.callback_query_handler(state=poster.post, text="share")
async def share(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data["text"]
    await call.message.answer("Начинаю отправку...")
    for user_id in db.get_users():
        try:
            await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")
        except Exception as err:
            await call.message.answer(f"Сообщение не пришло {get_mention(user_id)} по причине:\n{err}"
                                      f"\nОн был удален из базы данных!")
            db.delete_user(user_id=user_id)
    await call.message.answer("Пост отправлен!")
    await state.finish()

