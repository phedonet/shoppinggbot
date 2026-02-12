import asyncio
import os
import logging

from aiogram.exceptions import TelegramBadRequest
from assets import texts
from assets.keyboards import inline_keyboards as inl_kb
from aiogram import Dispatcher, Bot, F, Router
from aiogram.filters import Command
from aiogram.types import (Message, CallbackQuery, FSInputFile)
from dotenv import load_dotenv
from assets import base_op as base
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

class Search(StatesGroup):
    search = State()

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_MEDIA_PATH = os.getenv("DEFAULT_MEDIA_PATH")
router = Router()
ADMIN_ID = os.getenv("ADMIN_ID")
SERVICE_CHAT_ID = os.getenv("SERVICE_CHAT_ID")

elements_on_page = 5

@router.message(Command('warmup'))
async def warmup(message: Message):
    if message.from_user.id != int(ADMIN_ID):
        await message.answer(text="Недостаточно прав для исполнения этой команды!")
        return

    for product_id in range(1, await base.count_photos() + 1):
        msg = await message.bot.send_photo(
            photo=FSInputFile(f'{DEFAULT_MEDIA_PATH}/products/{product_id}.png'),
            chat_id=int(SERVICE_CHAT_ID)
        )
        await base.add_id_photo(product_id, msg.photo[-1].file_id)

    for service_id in range(1, await base.count_photos(service_table=True) + 1):
        msg = await message.bot.send_photo(
            photo=FSInputFile(f'{DEFAULT_MEDIA_PATH}/bot/{await base.get_name_service_photo(service_id)}'),
            chat_id=int(SERVICE_CHAT_ID)
        )
        await base.add_id_photo(service_id, msg.photo[-1].file_id, add_to_service=True)

@router.message(Command('start'))
async def start(message: Message):
    id_photo = await base.get_id_photos(id_product="menu.jpg", from_service=True)
    try:
        await message.answer_photo(
            photo=str(id_photo[0][1]),
            caption=texts.start,
            reply_markup=inl_kb.start_kb()
        )

    except TelegramBadRequest:
        msg = await message.answer_photo(
            photo=FSInputFile(f"{DEFAULT_MEDIA_PATH}/bot/menu.jpg"),
            caption=texts.start,
            reply_markup=inl_kb.start_kb()
        )
        await base.add_id_photo(id_photo=1, id_telegram_photo=msg.photo[-1].file_id, add_to_service=True)

@router.message(F.text == "Высотин петр")
async def petr(message: Message):
    await message.answer("Пердун")

@router.callback_query(F.data == 'main_menu:0')
async def start_btn(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    id_photo = await base.get_id_photos(id_product="menu.jpg", from_service=True)
    try:
        await call.message.answer_photo(
            photo=str(id_photo[0][1]),
            caption=texts.start,
            reply_markup=inl_kb.start_kb()
        )

    except TelegramBadRequest:
        msg = await call.message.answer_photo(
            photo=FSInputFile(f"{DEFAULT_MEDIA_PATH}/bot/menu.jpg"),
            caption=texts.start,
            reply_markup=inl_kb.start_kb()
        )
        await base.add_id_photo(id_photo=1, id_telegram_photo=msg.photo[-1].file_id, add_to_service=True)

@router.callback_query(F.data.startswith('categories:'))
async def categories(call: CallbackQuery, state: FSMContext):
    await state.clear()
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
    id_photo_tg = await base.get_id_photos(int(id_product))
    if len(id_photo_tg) == 1:
        try:
            await call.message.answer_photo(
                caption=text,
                reply_markup=await inl_kb.product_kb(int(id_product)),
                photo=str(id_photo_tg[0][1]))

        except TelegramBadRequest:
            msg = await call.message.answer_photo(
                caption=text,
                reply_markup=await inl_kb.product_kb(int(id_product)),
                photo=FSInputFile(f'{DEFAULT_MEDIA_PATH}/products/{id_product}.png')
            )
            await base.add_id_photo(int(id_photo_tg[0][0]), msg.photo[-1].file_id)

@router.callback_query(F.data == 'search:0')
async def search_screen(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(Search.search)
    await call.message.edit_text(text=texts.search_text, reply_markup=inl_kb.search_kb())

@router.message(Search.search)
async def search(message: Message, state: FSMContext):
    brand = message.text.strip()
    await state.clear()
    await message.answer(text=texts.result_search, reply_markup=await inl_kb.searched_kb(brand))


async def main():
    session = AiohttpSession(timeout=180)
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())