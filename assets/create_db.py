import sqlite3

con = sqlite3.connect("database.db")
con.execute("PRAGMA foreign_keys = ON;") # Для REFERENCES

with con:
    con.execute('CREATE TABLE IF NOT EXISTS categories (id INT PRIMARY KEY, name VARCHAR NOT NULL UNIQUE)')
    con.execute('CREATE TABLE IF NOT EXISTS subcategories (id INT PRIMARY KEY, id_category INT REFERENCES categories(id), name VARCHAR NOT NULL UNIQUE)')
  #  con.execute('CREATE TABLE IF NOT EXISTS products (id INT PRIMARY KEY,id_subcategory INT REFERENCES subcategories(id), brand VARCHAR(40), name VARCHAR NOT NULL UNIQUE, result INT, data TEXT, link VARCHAR)')

# con.execute('UPDATE subcategories set name = ? WHERE id = ?', ("Чулочно-носочные изделия", 25))

#con.execute('INSERT INTO subcategories(id, id_category, name) VALUES(?,?,?)', (33, 11, 'Сухие корма для кошек/собак'))

print(*con.execute('SELECT * FROM categories').fetchall())
print()
print(*con.execute('SELECT * FROM subcategories').fetchall())

con.commit()
con.close()