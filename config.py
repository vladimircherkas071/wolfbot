import json
import os
from datetime import date

ACCESS_FILE = "wheel_access.json"

TEAMMATES = {
  -1003341137383: [
    "Volleibollist",
    "Dukee",
    "Gareek",
    "Tushkann",
    "SizhkaAlaverda",
    "Miilka"
    ]
}

REG_GIFS = [
  "reg1.mp4",
  "reg2.mp4",
  "reg3.mp4"
  ]


def load_wheel_access():
    if not os.path.exists(ACCESS_FILE):
        return {}

    try:
        with open(ACCESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("[wheel_access load error]:", e)
        return {}


def save_wheel_access(data):
    try:
        with open(ACCESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("[wheel_access save error]:", e)