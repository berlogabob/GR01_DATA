# excel_to_md_and_csv.py
from markitdown import MarkItDown
import pandas as pd
import os

# ВШИТОЕ ИМЯ ФАЙЛА — ИЗМЕНИ НА СВОЁ!
FILENAME = "HospitaldaLuz.xlsx"  # ← Укажи имя твоего Excel-файла

# Получаем базовое имя без расширения
base_name = os.path.splitext(FILENAME)[0]
MD_FILE = f"{base_name}.md"
CSV_FILE = f"{base_name}.csv"

# Шаг 1: Конвертируем Excel в Markdown
print(f"Конвертируем {FILENAME} в Markdown...")
md_converter = MarkItDown()
result = md_converter.convert(FILENAME)
markdown_text = result.text_content

# Шаг 2: Очищаем Markdown (оставляем разделитель, убираем мусор)
lines = markdown_text.split('\n')
clean_lines = []

for line in lines:
    stripped = line.strip()
    if stripped.startswith('|') and '|' in stripped:
        # Строка таблицы — добавляем ВСЕ (включая |---|)
        clean_lines.append(line)
    else:
        # Не таблица: добавляем только если не пустая (убираем лишний текст/пустоты)
        if stripped:  # Только непустые
            clean_lines.append(line)

# Убираем лишние пустые строки (мусор)
clean_lines = [line for line in clean_lines if line.strip() or line == '']  # Оставляем одну пустую между блоками, если нужно
clean_markdown = '\n'.join(clean_lines).strip()

# Шаг 3: Сохраняем очищенный Markdown (с разделителем)
with open(MD_FILE, "w", encoding="utf-8") as f:
    f.write(clean_markdown)

print(f"Очищенный Markdown сохранён: {MD_FILE}")

# Шаг 4: Извлекаем таблицу в CSV (удаляем разделитель)
print("Извлекаем таблицу и сохраняем в CSV...")

table_rows = []
for line in clean_lines:
    if line.strip().startswith('|') and line.strip().endswith('|'):
        row = [cell.strip() for cell in line.split('|')[1:-1]]
        if row:
            # УДАЛЯЕМ строки-разделители (с '---')
            if any('---' in cell for cell in row):
                continue
            table_rows.append(row)

if len(table_rows) < 2:
    print("Ошибка: В Markdown нет таблицы с данными!")
else:
    headers = table_rows[0]
    data = table_rows[1:]
    
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(CSV_FILE, index=False, encoding="utf-8")
    
    print(f"CSV сохранён: {CSV_FILE}")
    print(f"Размер таблицы: {len(data)} строк, {len(headers)} колонок")
    print("\nПервые 3 строки CSV:")
    print(df.head(3).to_string(index=False))