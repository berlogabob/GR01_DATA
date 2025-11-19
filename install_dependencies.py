# install_dependencies.py
# Этот скрипт устанавливает/обновляет все зависимости для проекта (markitdown, docling, pandas, matplotlib, plotly).
# Запусти в активированном .venv: python install_dependencies.py

import subprocess
import sys

def run_command(cmd):
    """Запускает команду pip и выводит результат."""
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ {cmd[2:]}: успешно (или обновлено)")
        if result.stdout:
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка в {cmd[2:]}: {e.stderr.strip()}")
        sys.exit(1)

# Список зависимостей
dependencies = [
    'markitdown[all]',
    'docling',
    'pandas',
    'matplotlib',
    'plotly'
]

print("Проверяем/устанавливаем зависимости...")
for dep in dependencies:
    run_command(['pip', 'install', '--upgrade', dep])

print("\nГотово! Все зависимости обновлены.")
print("Для Typst (PDF): brew install typst (если на Mac).")