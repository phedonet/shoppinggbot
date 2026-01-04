import sqlite3

con = sqlite3.connect("database.db")
con.execute("PRAGMA foreign_keys = ON;") # Для REFERENCES

with con:
    con.execute('CREATE TABLE IF NOT EXISTS categories (id INT PRIMARY KEY, name VARCHAR NOT NULL UNIQUE)')
    con.execute('CREATE TABLE IF NOT EXISTS subcategories (id INT PRIMARY KEY, name VARCHAR NOT NULL UNIQUE, id_category INT REFERENCES categories(id))')
    con.execute('CREATE TABLE IF NOT EXISTS products (id INT PRIMARY KEY,id_subcategory INT REFERENCES subcategories(id), brand VARCHAR(40), name VARCHAR NOT NULL UNIQUE, result INT, data TEXT, link VARCHAR)')

# con.execute('UPDATE categories set name = ? WHERE id = ?', ("Бакалея", 3))
con.execute('INSERT INTO products(id, id_subcategory, brand, name, result, data, link) VALUES (?,?,?,?,?,?,?)', (1, 1, 'Камарчагский', 'Творог Камарчагский 5%', 90, 'Состав:\nИзготовлен из нормализованного молока с использованием закваски\nБезопасность:\nСогласно протоколу испытаний № 1574 от 19.09.2025 ИЦ ФБУ «Красноярский ЦСМ» творог м.д. ж. 5,0 % по всем проверенным физико-химическим и микробиологическим показателям соответствует требованиям нормативно-правовой и нормативной документации. Наличие крахмала, сорбиновой и бензойной кислот, растительных жиров в жировой фазе продукта не установлено\nМаркировка:\nУстановлены нарушения по маркировке потребительских упаковок - не указаны условия хранения продукта после вскрытия упаковки, что является нарушением требований пп. 4.1 ТР ТС 022/2011, р. 12 ТР ТС 033/2013 и п. 5.3 ГОСТ 31453-2013.\nЗаключение:\nУстановлены нарушения по маркировке потребительских упаковок', 'prodnadzor24.ru/catalogue/tovars/tovars_1695.html?tov=111'))
con.commit()
con.close()