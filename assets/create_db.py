import sqlite3

con = sqlite3.connect("database.db")
con.execute("PRAGMA foreign_keys = ON;") # Для REFERENCES

with con:
    con.execute('CREATE TABLE IF NOT EXISTS categories (id INT PRIMARY KEY, name VARCHAR NOT NULL UNIQUE)')
    con.execute('CREATE TABLE IF NOT EXISTS subcategories (id INT PRIMARY KEY, name VARCHAR NOT NULL UNIQUE, id_category INT REFERENCES categories(id))')
    con.execute('CREATE TABLE IF NOT EXISTS products (id INT PRIMARY KEY, name VARCHAR NOT NULL UNIQUE, id_subcategory INT REFERENCES subcategories(id), data TEXT)')

# con.execute('UPDATE categories set name = ? WHERE id = ?', ("Бакалея", 3))
try:
   con.execute('INSERT INTO products (id, name, id_subcategory, data) VALUES (?, ?, ?, ?)', (2, "Хлеб «Социальный» из пшеничной муки 1 с. т/м «Фабрика хлеба»", 1, "Результат: Нарушений не обнаружено ✅\nХлеб «Социальный» из пшеничной муки 1 с., т.м. «Фабрика хлеба», предприятие-изготовитель ИП Осколков В.Б., г. Красноярск - по физико-химическим и микробиологическим показателям соответствует требованиям нормативной документации. Замечаний по маркировке нет. Хлебопекарные улучшители не выявлены."))
except:
    pass

con.commit()
con.close()