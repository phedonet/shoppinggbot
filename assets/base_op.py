import sqlite3

def show_categories(page: int, limit: int) -> list:
    con = sqlite3.connect("database.db")
    start_l = (page - 1) * limit
    res = con.execute('SELECT name FROM categories ORDER BY id LIMIT ?, ?', (start_l, limit)).fetchall()
    con.close()
    return res

def count_pages_categories(limit: int) -> int:
    con = sqlite3.connect("database.db")
    res = con.execute('SELECT COUNT(*) FROM categories').fetchall()
    con.close()
    return res[0][0] // limit + 1 if res[0][0] % limit != 0 else res[0][0] // limit

def show_subcategories(id_category: int, page: int, limit: int) -> list:
    con = sqlite3.connect("database.db")
    start_l = (page - 1) * limit
    res = con.execute('SELECT name FROM subcategories WHERE id_category = ? ORDER BY id LIMIT ?, ?', (id_category, start_l, limit)).fetchall()
    con.close()
    return res

def count_pages_subcategories(id_category: int, limit: int) -> int:
    con = sqlite3.connect("database.db")
    res = con.execute('SELECT COUNT(*) FROM subcategories WHERE id_category = ?', (id_category,)).fetchall()
    con.close()
    return res[0][0] // limit + 1 if res[0][0] % limit != 0 else res[0][0] // limit

def show_products(id_subcategory: int, page: int, limit: int) -> list:
    con = sqlite3.connect("database.db")
    start_l = (page - 1) * limit
    end_l = page * limit
    res = con.execute('SELECT name FROM products WHERE id_subcategory = ? ORDER BY id LIMIT ?, ?', (id_subcategory, start_l, end_l)).fetchall()
    con.close()
    return res

def count_pages_products(id_subcategory: int, limit: int) -> int:
    con = sqlite3.connect("database.db")
    res = con.execute('SELECT COUNT(*) FROM products WHERE id_subcategory = ?', (id_subcategory,)).fetchall()
    con.close()
    return res[0][0] // limit + 1 if res[0][0] % limit != 0 else res[0][0] // limit
