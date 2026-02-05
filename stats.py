import json
from datetime import datetime
from pathlib import Path

FILE = Path("stats.json")


def load():
    if FILE.exists():
      try:
        return json.loads(FILE.read_text())
      except:
        return {}
    return {}


def save(data):
    FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def current_month():
    return datetime.now().strftime("%Y-%m")


def add(chat_id, name, reg_type):
    data = load()
    month = current_month()

    chat = str(chat_id)

    data.setdefault(chat, {})
    data[chat].setdefault(month, {})
    data[chat][month].setdefault(name, {"pipe": 0, "dep": 0})

    data[chat][month][name][reg_type] += 1

    save(data)


def reset_month(chat_id):
    data = load()
    chat = str(chat_id)
    month = current_month()

    if chat in data and month in data[chat]:
        del data[chat][month]

    save(data)