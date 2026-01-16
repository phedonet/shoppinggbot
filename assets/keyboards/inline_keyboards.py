from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from assets import base_op as base

def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="К продуктам 🛒",
                callback_data="categories:1:1"),
        ]
    ])

async def shopping_main(page: int, limit: int) -> InlineKeyboardMarkup:
    pages = await base.count_pages_categories(limit)
    page %= pages + 1
    if page == 0:
        page = 1

    categories = await base.show_categories(page, limit)
    inl_kb = [[InlineKeyboardButton(text="Поиск", callback_data="search:0")]]

    for category in categories:
        inl_kb.append([InlineKeyboardButton(
            text=category[1],
            callback_data=f'subcategories:{category[0]}:1')]
        )

    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"categories:2:{page-1}"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"categories:2:{page+1}")                                                                                                                                               ])

    inl_kb.append([InlineKeyboardButton(text="Назад", callback_data="main_menu:0")])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)

async def subcategory_kb(id_category: int, page: int, limit: int) -> InlineKeyboardMarkup:
    pages = await base.count_pages_subcategories(id_category, limit)
    page %= pages + 1
    if page == 0:
        page = 1

    inl_kb = []
    subcategories = await base.show_subcategories(id_category, page, limit)
    for subcategory in subcategories:
        inl_kb.append([InlineKeyboardButton(
            text=subcategory[1],
            callback_data=f'products:{subcategory[0]}:1:0')]
        )

    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"subcategories:{id_category}:{page - 1}:0"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"subcategories:{id_category}:{page + 1}:0")])
    inl_kb.append([InlineKeyboardButton(text="Назад", callback_data="categories:2:1")])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)

async def products_kb(id_subcategory: int, page: int, limit: int) -> InlineKeyboardMarkup:
    pages = await base.count_pages_products(id_subcategory, limit)
    page %= pages + 1
    if page == 0:
        page = 1

    products = await base.show_products(id_subcategory, page, limit)
    id_category = await base.get_id_category(id_subcategory)
    inl_kb = []
    for product in products:
        inl_kb.append([InlineKeyboardButton(
            text=f'{product[1]} "{product[2]}"',
            callback_data=f'product:{product[0]}')]
        )

    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"products:{id_subcategory}:{page - 1}"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"products:{id_subcategory}:{page + 1}")])
    inl_kb.append([InlineKeyboardButton(text="Назад", callback_data=f"subcategories:{id_category}:1")])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)

async def product_kb(id_product: int) -> InlineKeyboardMarkup:
    id_subcategory = await base.get_id_subcategory(id_product)
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data=f"products:{id_subcategory}:1:1")]])