import asyncio
import os
import logging

from assets import texts
from assets.keyboards import inline_keyboards as inl_kb
from aiogram import Dispatcher, Bot, F, Router
from aiogram.filters import Command
from aiogram.types import (Message, CallbackQuery, ReplyKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardRemove, WebAppInfo, KeyboardButtonPollType, FSInputFile)
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_TOKEN")
router = Router()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer_photo(
        FSInputFile('assets/media/menu.png'),
        caption=texts.start,
        reply_markup=inl_kb.start_kb())

@router.message(F.text == "Высотин птср")
async def petr(message: Message):
    await message.answer("Пердун")

@router.callback_query(F.data == 'main_menu:0')
async def start_btn(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer_photo(
        FSInputFile('assets/media/menu.png'),
        caption=texts.start,
        reply_markup=inl_kb.start_kb())

@router.callback_query(F.data.startswith('start:'))
async def categories(call: CallbackQuery):
    name, value = call.data.split(sep=':')
    await call.answer()
    if value == '1':
        await call.message.delete()
        await call.message.answer(text=texts.shopping_main, reply_markup=inl_kb.shopping_main())

@router.callback_query(F.data.startswith('category:'))
async def check_category(call: CallbackQuery):
    name, value = call.data.split(sep=":")
    await call.answer()
    if value == "1":
        await call.message.edit_text(text=texts.choose_meal, reply_markup=inl_kb.category_1())

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())