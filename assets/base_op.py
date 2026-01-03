import sqlite3

def show_categories() -> list:
    con = sqlite3.connect("database.db")
    res = con.execute('SELECT name FROM categories ORDER BY id').fetchall()
    con.close()
    return res

def show_subcategories(id_category) -> list:
    con = sqlite3.connect("database.db")
    res = con.execute('SELECT name FROM subcategories WHERE id_category = ? ORDER BY id', (id_category,)).fetchall()
    con.close()
    return res

def show_products(id_subcategory) -> list:
    con = sqlite3.connect("database.db")
    res = con.execute('SELECT name FROM products WHERE id_subcategory = ? ORDER BY id', (id_subcategory,)).fetchall()
    con.close()
    return res