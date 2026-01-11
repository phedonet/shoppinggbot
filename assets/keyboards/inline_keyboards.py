from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from assets import base_op as base

def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="15,0% Сельскохозяйственное предприятие Искра", callback_data="categories:1:1"),
        ]
    ])

async def shopping_main(page: int, limit: int) -> InlineKeyboardMarkup:
    pages = await base.count_pages_categories(limit)
    page %= pages + 1
    if page == 0:
        page = 1
    categories = await base.show_categories(page, limit)
    inl_kb = [[InlineKeyboardButton(text="Поиск", callback_data="search:0")]]
    id_subcategory = 1 + limit * (page - 1)

    for category in categories:
        inl_kb.append([InlineKeyboardButton(text=category[0], callback_data=f'subcategories:{id_subcategory}:1')])
        id_subcategory += 1
    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"categories:2:{page-1}"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"categories:2:{page+1}")                                                                                                                                               ])

    inl_kb.append([InlineKeyboardButton(text="Назад", callback_data="main_menu:0")])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)

async def subcategory_kb(id_subcategory: int, page: int, limit: int) -> InlineKeyboardMarkup:
    pages = await base.count_pages_subcategories(id_subcategory, limit)
    subcategories = await base.show_subcategories(id_subcategory, page, limit)
    page %= pages + 1
    if page == 0:
        page = 1
    inl_kb = []
    id_products = 1 + limit * (page - 1)

    for subcategory in subcategories:
        inl_kb.append([InlineKeyboardButton(text=subcategory[0], callback_data=f'products:{id_products}:1:{id_subcategory}')])
        id_products += 1

    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"subcategories:{id_subcategory}:{page - 1}"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"subcategories:{id_subcategory}:{page + 1}")])
    inl_kb.append([InlineKeyboardButton(text="Назад", callback_data="categories:2:1")])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)

async def products_kb(id_products: int, page: int, limit: int, id_subcategory: int) -> InlineKeyboardMarkup:
    pages = await base.count_pages_products(id_products, limit)
    products = await base.show_products(id_products, page, limit)
    page %= pages + 1
    if page == 0:
        page = 1
    inl_kb = []
    id_product = 1 + limit * (page - 1)
    for product in products:
        inl_kb.append([InlineKeyboardButton(text=product[0], callback_data=f'product:{id_product}:{id_subcategory}:{id_products}')])
        id_product += 1
    inl_kb.append([InlineKeyboardButton(text="<", callback_data=f"products:{id_subcategory}:{page - 1}:{id_products}"),
                   InlineKeyboardButton(text=f"{page}/{pages}", callback_data=" "),
                   InlineKeyboardButton(text=">", callback_data=f"products:{id_subcategory}:{page + 1}:{id_products}")])
    inl_kb.append([InlineKeyboardButton(text="Назад", callback_data=f"subcategories:{id_subcategory}:1")])

    return InlineKeyboardMarkup(inline_keyboard=inl_kb)

def product_kb(id_products: int, id_subcategory: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data=f"products:{id_products}:1:{id_subcategory}")]])