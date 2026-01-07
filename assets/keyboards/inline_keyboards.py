from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from assets import base_op as base

def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 К продуктам", callback_data="categories:1:1"),
        ]
    ])

async def shopping_main(page: int, limit: int) -> InlineKeyboardMarkup:
    pages = await base.count_pages_categories(limit)
    page %= pages + 1
    if page == 0:
        page = 1
    categories = await base.show_categories(page, limit)
    inl_kb = [[InlineKeyboardButton(text="Поиск", callback_data="search:0")]]
    i = 1 + limit * (page - 1)

    for category in categories:
        inl_kb.append([InlineKeyboardButton(text=category[0], callback_data=f'subcategories:{i}:1')])
        i += 1
    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"categories:2:{page-1}"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"categories:2:{page+1}")                                                                                                                                               ])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)

async def subcategory_kb(value: int, page: int, limit: int) -> InlineKeyboardMarkup:
    pages = await base.count_pages_subcategories(value, limit)
    subcategories = await base.show_subcategories(value, page, limit)
    page %= pages + 1
    if page == 0:
        page = 1
    inl_kb = []
    i = 1 + limit * (page - 1)

    for subcategory in subcategories:
        inl_kb.append([InlineKeyboardButton(text=subcategory[0], callback_data=f'products:{i}:1:{value}')])
        i += 1

    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"subcategories:{value}:{page - 1}"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"subcategories:{value}:{page + 1}")])
    inl_kb.append([InlineKeyboardButton(text="Назад", callback_data="categories:2:1")])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)

async def products_kb(value: int, page: int, limit: int, subcategory_id: int) -> InlineKeyboardMarkup:
    pages = await base.count_pages_products(value, limit)
    products = await base.show_products(value, page, limit)
    page %= pages + 1
    if page == 0:
        page = 1
    inl_kb = []
    i = 1 + limit * (page - 1)
    for product in products:
        inl_kb.append([InlineKeyboardButton(text=product[0], callback_data=f'product:{i}')])
        i += 1
    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"products:{value}:{page - 1}"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"products:{value}:{page + 1}")])
    inl_kb.append([InlineKeyboardButton(text="Назад", callback_data=f"subcategories:{subcategory_id}:1")])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)