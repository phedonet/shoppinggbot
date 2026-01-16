import aiosqlite as sql

async def show_categories(page: int, limit: int) -> list:
    async with sql.connect('assets/database.db') as con:
        start_l = (page - 1) * limit
        res = await con.execute_fetchall(
            'SELECT id, name FROM categories '
            'ORDER BY id '
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
            'ORDER BY id '
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
    end_l = page * limit
    async with sql.connect('assets/database.db') as con:
        res = await con.execute_fetchall(
            'SELECT id, name, brand FROM products '
            'WHERE id_subcategory = ? '
            'ORDER BY id LIMIT ?, ?',
            (id_subcategory, start_l, end_l)
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