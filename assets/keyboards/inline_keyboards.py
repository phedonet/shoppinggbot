from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from assets import base_op

def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 К продуктам", callback_data="categories:1:1"),
        ]
    ])

def shopping_main(page: int, limit: int) -> InlineKeyboardMarkup:
    pages = base_op.count_pages_categories(limit)
    page %= pages + 1
    if page == 0:
        page = 1
    categories = base_op.show_categories(page, limit)
    inl_kb = [[InlineKeyboardButton(text="Поиск", callback_data="search:0")]]
    i = 1 + limit * (page - 1)

    for category in categories:
        inl_kb.append([InlineKeyboardButton(text=category[0], callback_data=f'subcategories:{i}:1')])
        i += 1
    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"categories:2:{page-1}"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"categories:2:{page+1}")                                                                                                                                               ])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)

def subcategory_kb(value: int, page: int, limit: int) -> InlineKeyboardMarkup:
    pages = base_op.count_pages_subcategories(value, limit)
    subcategories = base_op.show_subcategories(value, page, limit)
    page %= pages + 1
    if page == 0:
        page = 1
    inl_kb = []
    i = 1 + limit * (page - 1)

    for subcategory in subcategories:
        inl_kb.append([InlineKeyboardButton(text=subcategory[0], callback_data=f'subcategory:{i}')])
        i += 1

    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"subcategories:{value}:{page - 1}"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"subcategories:{value}:{page + 1}")])
    inl_kb.append([InlineKeyboardButton(text="Назад", callback_data="categories:2:1")])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)
