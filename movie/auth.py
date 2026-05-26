"""Google OAuth — вход через Google."""
import requests                                            # для HTTP-запросов
from urllib.parse import urlencode                         # для формирования URL с параметрами

from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI  # настройки


def get_login_url():                                       # формирует ссылку для входа через Google
    """Возвращает URL, на который надо отправить пользователя для логина."""
    params = {                                             # параметры OAuth-запроса
        "client_id": GOOGLE_CLIENT_ID,                     # ID нашего приложения в Google
        "redirect_uri": GOOGLE_REDIRECT_URI,               # куда Google вернёт пользователя
        "response_type": "code",                           # просим код авторизации
        "scope": "openid email profile",                   # запрашиваем email и имя
    }
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)  # склеиваем URL


def get_user_info(code):                                   # получает данные пользователя по коду от Google
    """Обменивает код от Google на информацию о пользователе."""
    # Шаг 1: меняем код на access_token
    token_response = requests.post(                        # POST-запрос к Google
        "https://oauth2.googleapis.com/token",             # endpoint обмена кода на токен
        data={                                             # данные запроса
            "code": code,                                  # код от Google
            "client_id": GOOGLE_CLIENT_ID,                 # ID приложения
            "client_secret": GOOGLE_CLIENT_SECRET,         # секрет приложения
            "redirect_uri": GOOGLE_REDIRECT_URI,           # должен совпадать с настройками
            "grant_type": "authorization_code",            # тип запроса по спецификации OAuth
        },
    )
    access_token = token_response.json()["access_token"]   # достаём токен из ответа

    # Шаг 2: запрашиваем профиль пользователя с этим токеном
    user_response = requests.get(                          # GET-запрос за профилем
        "https://www.googleapis.com/oauth2/v3/userinfo",   # endpoint профиля
        headers={"Authorization": f"Bearer {access_token}"},  # передаём токен в заголовке
    )
    data = user_response.json()                            # парсим JSON

    return {                                               # возвращаем только нужные поля
        "google_id": data["sub"],                          # уникальный ID пользователя в Google
        "name": data.get("name", ""),                      # имя
        "email": data["email"],                            # email
    }
