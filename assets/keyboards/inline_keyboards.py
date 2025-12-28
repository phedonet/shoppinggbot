from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 К продуктам", callback_data="shopping:1"),
        ]
    ])


def shopping_main():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Поиск", callback_data="search:0")],
        [InlineKeyboardButton(text="Заморозка", callback_data="category:1"),
         InlineKeyboardButton(text="Овощи", callback_data="category:2")],
        [InlineKeyboardButton(text="Назад", callback_data="main_menu:0"), ],
    ])


def zamorozka():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пельмени", callback_data="zamorozka:1")],
        [InlineKeyboardButton(text="Назад", callback_data="shopping:1")]
    ])