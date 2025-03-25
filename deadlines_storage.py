import json
import os
from datetime import datetime

DEADLINES_FILE = "deadlines.json"

# Инициализация файла, если он не существует
if not os.path.exists(DEADLINES_FILE):
    with open(DEADLINES_FILE, "w") as f:
        json.dump({}, f)

def load_deadlines():
    """Загружает дедлайны из файла."""
    with open(DEADLINES_FILE, "r") as f:
        return json.load(f)

def save_deadlines(deadlines):
    """Сохраняет дедлайны в файл."""
    with open(DEADLINES_FILE, "w") as f:
        json.dump(deadlines, f, indent=4)

def add_deadline(user_id, deadline_name, deadline_datetime):
    """Добавляет дедлайн для пользователя."""
    deadlines = load_deadlines()
    if str(user_id) not in deadlines:
        deadlines[str(user_id)] = []
    deadlines[str(user_id)].append({
        "name": deadline_name,
        "datetime": deadline_datetime.strftime("%Y-%m-%d %H:%M")
    })
    save_deadlines(deadlines)

def get_user_deadlines(user_id):
    """Возвращает дедлайны пользователя."""
    deadlines = load_deadlines()
    return deadlines.get(str(user_id), [])

def remove_deadline(user_id, deadline_index):
    """Удаляет дедлайн по индексу."""
    deadlines = load_deadlines()
    if str(user_id) in deadlines and 0 <= deadline_index < len(deadlines[str(user_id)]):
        deadlines[str(user_id)].pop(deadline_index)
        save_deadlines(deadlines)