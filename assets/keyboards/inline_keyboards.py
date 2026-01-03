from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from assets import base_op

def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 К продуктам", callback_data="start:1"),
        ]
    ])

def shopping_main(): # Список категорий
    categories = base_op.show_categories()
    inl_kb = [[InlineKeyboardButton(text="Поиск", callback_data="search:0")]]
    i = 1

    for category in categories:
        inl_kb.append([InlineKeyboardButton(text=category[0], callback_data=f'category:{i}')])
        i += 1

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)

def subcategory_kb(value):
    subcategories = base_op.show_subcategories(value)
    inl_kb = []
    i = 1

    for subcategory in subcategories:
        inl_kb.append([InlineKeyboardButton(text=subcategory[0], callback_data=f'subcategory:{i}')])
    inl_kb.append([InlineKeyboardButton(text="Назад", callback_data="start:2")])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)
