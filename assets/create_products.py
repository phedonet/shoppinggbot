import sqlite3
from pathlib import Path

import pandas as pd

EXCEL_PATH = Path("monitoring_clean_updated_filled.xlsx")  # ваш Excel
SQLITE_PATH = Path("database.db")                     # куда сохранить SQLite
SHEET_NAME = "Sheet1"
TABLE_NAME = "products"

# 1) Читаем Excel
df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)

# 2) Приводим имена колонок и типы
df = df.rename(columns={"№": "id"})  # вместо "№" будет "num"

# дата в исходнике: "16.08.2024" -> "2024-08-16"
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce").dt.strftime("%Y-%m-%d")

# (опционально) подчистим пробелы у текстов
for col in ["category", "brand", "product_name", "description", "link"]:
    df[col] = df[col].astype(str).str.strip()

# 3) Пишем в SQLite
with sqlite3.connect(SQLITE_PATH) as conn:
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

    # (опционально) индексы для быстрых фильтров по дате/категории
    conn.execute(f'CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_date ON {TABLE_NAME}(date);')
    conn.execute(f'CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_category ON {TABLE_NAME}(category);')

print(f"✅ Загружено строк: {len(df)} → {SQLITE_PATH} / таблица {TABLE_NAME}")
print("Пример проверки: SELECT * FROM monitoring LIMIT 5;")
