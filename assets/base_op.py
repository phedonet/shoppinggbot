import aiosqlite as sql

async def show_categories(page: int, limit: int) -> list:
    async with sql.connect('assets/database.db') as con:
        start_l = (page - 1) * limit
        res = await con.execute_fetchall(
            'SELECT id, name FROM categories '
            'ORDER BY name '
            'LIMIT ?, ?',
            (start_l, limit)
        )

    return res

async def count_pages_categories(limit: int) -> int:
    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall('SELECT COUNT(*) FROM categories')

    return res[0][0] // limit + 1 if res[0][0] % limit != 0 else res[0][0] // limit

async def show_subcategories(id_category: int, page: int, limit: int) -> list:
    async with sql.connect('assets/database.db') as con:
        start_l = (page - 1) * limit
        res = await con.execute_fetchall(
            'SELECT id, name FROM subcategories '
            'WHERE id_category = ? '
            'ORDER BY name '
            'LIMIT ?, ?',
            (id_category, start_l, limit)
        )

    return res

async def count_pages_subcategories(id_category: int, limit: int) -> int:
    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall(
            'SELECT COUNT(*) FROM subcategories '
            'WHERE id_category = ?',
            (id_category,)
        )

    return res[0][0] // limit + 1 if res[0][0] % limit != 0 else res[0][0] // limit

async def show_products(id_subcategory: int, page: int, limit: int) -> list:
    start_l = (page - 1) * limit
    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall(
            'SELECT id, name FROM products '
            'WHERE id_subcategory = ? '
            'ORDER BY id LIMIT ?, ?',
            (id_subcategory, start_l, limit)
        )

    return res

async def count_pages_products(id_subcategory: int, limit: int) -> int:
    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall(
            'SELECT COUNT(*) FROM products '
            'WHERE id_subcategory = ?',
            (id_subcategory,)
        )

    return res[0][0] // limit + 1 if res[0][0] % limit != 0 else res[0][0] // limit

async def get_product(id_product: int) -> tuple:
    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall(
            'SELECT * FROM products '
            'WHERE id = ?',
            (id_product,)
        )

    return res[0]

async def get_id_category(id_subcategory: int) -> int:
    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall(
            'SELECT id_category FROM subcategories '
            'WHERE id = ?',
            (id_subcategory,)
        )

    return res[0][0]

async def get_id_subcategory(id_product: int) -> int:
    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall(
            'SELECT id_subcategory FROM products '
            'WHERE id = ?',
            (id_product,)
        )

    return res[0][0]

async def get_id_photos(id_product: int | str, from_service=False) -> list:
    async with sql.connect('assets/database.db') as con:
        if from_service:
            res = await con.execute_fetchall(
                'SELECT id, tg_photo_id FROM service '
                'WHERE name_in_bot_folder = ?',
                (id_product,)
            )

        else:
            res = await con.execute_fetchall(
                'SELECT id, tg_photo_id FROM photos '
                'WHERE id_product = ?',
                (id_product,)
            )

    return res

async def add_id_photo(id_photo: int, id_telegram_photo: str, add_to_service=False) -> None:
    async with sql.connect('assets/database.db') as con:
        if add_to_service:
            await con.execute(
                'UPDATE service SET tg_photo_id = ? '
                'WHERE id = ?',
                (id_telegram_photo, id_photo)
            )

        else:
            await con.execute(
                'UPDATE photos SET tg_photo_id = ? '
                'WHERE id = ?',
                (id_telegram_photo, id_photo)
            )

        await con.commit()

async def count_photos(service_table=False) -> int:
    async with sql.connect('assets/database.db') as con:
        if service_table:
            res = await con.execute_fetchall('SELECT COUNT(*) FROM service')
        else:
            res = await con.execute_fetchall('SELECT COUNT(*) FROM photos')

    return res[0][0]

async def get_id_product(id_photo: int) -> int:
    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall(
            'SELECT id_product FROM photos '
            'WHERE id = ?',
            (id_photo,)
        )

    return res[0][0]

async def get_name_service_photo(id_photo: int) -> str:
    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall(
            'SELECT name_in_bot_folder FROM service '
            'WHERE id = ?',
            (id_photo,)
        )

    return res[0][0]

async def search_brand(text: str) -> list:
    req = 'SELECT id, name FROM products WHERE for_search LIKE ?'
    add_and = ' AND for_search LIKE ?'
    add_or = ' OR for_search LIKE ?'
    text = text.lower()
    text = text.replace('%', '')
    text = text.replace('-', ' ')
    text = text.strip()
    prev_space = False
    new_text = ''
    for i in range(len(text)):
        if prev_space and text[i] == ' ':
            continue
        elif text[i] == ' ':
            prev_space = True
            new_text += text[i]
        else:
            prev_space = False
            new_text += text[i]

    new_text = new_text.split()
    for i in range(len(new_text)):
        new_text[i] = f'%{new_text[i]}%'
    req += add_and * (len(new_text) - 1)

    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall(
            req,
            new_text
        )

    return res