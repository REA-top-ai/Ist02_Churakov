"""Настройки приложения. Берутся из файла .env."""
import os                                                  # модуль для работы с переменными окружения
from dotenv import load_dotenv                             # функция для чтения файла .env

load_dotenv()                                              # читаем .env и помещаем значения в os.environ

# Ключи для Google OAuth (логин через Google)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")           # ID OAuth-клиента
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")   # секрет OAuth-клиента
GOOGLE_REDIRECT_URI = "http://localhost:8501"              # куда Google вернёт пользователя после входа

# Ключи для внешних сервисов
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")             # ключ от Mistral (AI)
KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY")         # ключ от Kinopoisk.dev (фильмы)
