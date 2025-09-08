import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "dbname": os.getenv("dbname"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "host": os.getenv("host"),
    "port": os.getenv("port"),
}

companies = [
    {"id": 1122462, "name": "Skyeng"},
    {"id": 856498, "name": "Леста Игры"},
    {"id": 5920492, "name": "DNS Головной офис"},
    {"id": 3529, "name": "СБЕР"},
    {"id": 1740, "name": "Яндекс"},
    {"id": 78638, "name": "Т-банк"},
    {"id": 1942330, "name": "Пятёрочка"},
    {"id": 15478, "name": "VK"},
    {"id": 1440683, "name": "RUTUBE"},
    {"id": 4233, "name": "X5 Group"},
]

hh_api = "https://api.hh.ru/"
