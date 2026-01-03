from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 К продуктам", callback_data="start:1"),
        ]
    ])


def shopping_main(): # Список категорий
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Поиск", callback_data="search:0")],
        [InlineKeyboardButton(text="Хлебобулочные изделия", callback_data="category:1"),
         InlineKeyboardButton(text="Кондитерские изделия", callback_data="category:2")],
        [InlineKeyboardButton(text="Назад", callback_data="main_menu:0"), ],
    ])


def category_1(): # Хлебобулочные изделия
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Хлеб", callback_data="meal:1.1")],
        [InlineKeyboardButton(text="Назад", callback_data="start:1")]
    ])