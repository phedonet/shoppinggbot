import sqlite3

con = sqlite3.connect("database.db")
con.execute("PRAGMA foreign_keys = ON;") # Для REFERENCES
con.row_factory = sqlite3.Row # Для словаря на выходе

# code - № категории

# sub_code - № подкатегории; category_id - № категории, к которой принадлежит подкатегория


con.close()