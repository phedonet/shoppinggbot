import asyncio
import os
import logging

from assets import texts
from assets.keyboards import inline_keyboards as inl_kb
from aiogram import Dispatcher, Bot, F, Router
from aiogram.filters import Command
from aiogram.types import (Message, CallbackQuery, FSInputFile)
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_TOKEN")
router = Router()

elements_on_page = 5

@router.message(Command('start'))
async def start(message: Message):
    await message.answer_photo(
        FSInputFile('assets/media/bot/menu.png'),
        caption=texts.start,
        reply_markup=inl_kb.start_kb())

@router.message(F.text == "Высотин петр")
async def petr(message: Message):
    await message.answer("Пердун")

@router.callback_query(F.data == 'main_menu:0')
async def start_btn(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer_photo(
        FSInputFile('assets/media/bot/menu.png'),
        caption=texts.start,
        reply_markup=inl_kb.start_kb())

@router.callback_query(F.data.startswith('categories:'))
async def categories(call: CallbackQuery):
    name, value, page = call.data.split(sep=':')
    await call.answer()
    if value == '1':
        await call.message.delete()
        await call.message.answer(
            text=texts.shopping_main,
            reply_markup=await inl_kb.shopping_main(page=int(page), limit=elements_on_page)
        )

    elif value == '2':
        await call.message.edit_text(
            text=texts.shopping_main,
            reply_markup=await inl_kb.shopping_main(page=int(page), limit=elements_on_page)
        )

@router.callback_query(F.data.startswith('subcategories:'))
async def subcategories(call: CallbackQuery):
    name, id_subcategory, page = call.data.split(sep=":")
    await call.answer()
    await call.message.edit_text(
        text=texts.shopping_main,
        reply_markup=await inl_kb.subcategory_kb(int(id_subcategory), int(page), elements_on_page)
    )

@router.callback_query(F.data.startswith('products:'))
async def products(call: CallbackQuery):
    name, id_products, page, value = call.data.split(sep=":")
    await call.answer()
    if int(value):
        await call.message.delete()
        await call.message.answer(
            text=texts.choose_meal,
            reply_markup=await inl_kb.products_kb(int(id_products), int(page), elements_on_page)
        )
    else:
        await call.message.edit_text(
            text=texts.choose_meal,
            reply_markup=await inl_kb.products_kb(int(id_products), int(page), elements_on_page)
        )

@router.callback_query(F.data.startswith('product:'))
async def product(call: CallbackQuery):
    name, id_product = call.data.split(sep=":")
    await call.answer()
    await call.message.delete()
    text = await texts.product(int(id_product))
    await call.message.answer_photo(
        caption=text,
        reply_markup=await inl_kb.product_kb(int(id_product)),
        photo=FSInputFile(f'assets/media/products/{id_product}.png')
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())