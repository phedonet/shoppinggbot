import asyncio
import os
import logging

from aiogram import Dispatcher, Bot, F, Router
from aiogram.filters import Command
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardRemove, WebAppInfo, KeyboardButtonPollType, FSInputFile, )
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_TOKEN")
router = Router()

class Texts:
    start = "Привет! 👋\nДобро пожаловать в бот, который помогает находить действительно качественные продукты в магазине. Здесь собрана большая база товаров из разных категорий — от молочной продукции и мяса до сладостей и напитков. Для каждого продукта доступны результаты независимых экспертиз и проверок, чтобы ты мог сделать осознанный выбор и избежать некачественных товаров. Бот подскажет, на что стоит обратить внимание: состав, соответствие стандартам и реальные оценки качества. Просто ищи продукт и получай проверенную информацию быстро и удобно. 🛒✨"
    shopping_main = "Выберите категорию товаров или воспользуйтесь поиском:"

class INLINE_KEYBOARDS:

    def start_kb(self):
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🛒 К продуктам", callback_data="shopping:1"),
            ]
        ])

    def shopping_main(self):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Поиск", callback_data="search:0")],
            [InlineKeyboardButton(text="Заморозка", callback_data="category:1"), InlineKeyboardButton(text="Овощи", callback_data="category:2")],
            [InlineKeyboardButton(text="Назад", callback_data="main_menu:0"),],
        ])

    def zamorozka(self):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пельмени", callback_data="zamorozka:1")],
            [InlineKeyboardButton(text="Назад", callback_data="shopping:1")]
        ])
InLineKeyBoards = INLINE_KEYBOARDS()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer_photo(
        FSInputFile('assets/media/menu.png'),
        caption=Texts.start,
        reply_markup=InLineKeyBoards.start_kb())

@router.message(F.text == "Высотин птср")
async def petr(message: Message):
    await message.answer("Пердун")

@router.callback_query(F.data == 'main_menu:0')
async def start_btn(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer_photo(
        FSInputFile('media/menu.png'),
        caption=Texts.start,
        reply_markup=InLineKeyBoards.start_kb())

@router.callback_query(F.data.startswith('shopping:'))
async def buttons(call: CallbackQuery):
    name, value = call.data.split(sep=':')
    await call.answer()
    if value == '1':
        await call.message.delete()
        await call.message.answer(text=Texts.shopping_main, reply_markup=InLineKeyBoards.shopping_main())

@router.callback_query(F.data.startswith('category:'))
async def categories(call: CallbackQuery):
    name, value = call.data.split(sep=":")
    await call.answer()
    await call.message.delete()
    if value == "1":
        await call.message.answer(text="Выберите нужный продукт", reply_markup=InLineKeyBoards.zamorozka())

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())