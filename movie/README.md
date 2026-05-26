# Гид по фильмам с AI

Простое веб-приложение на Python. Пользователь логинится через Google, вводит название фильма, получает информацию о нём (из Kinopoisk.dev: год, рейтинг, жанры, постер, описание) и разбор от AI (Mistral): чем фильм интересен, кому понравится, какие похожие фильмы посмотреть. Понравившиеся фильмы можно сохранять в список «Хочу посмотреть».

---

## Архитектура

```
                  +------------------+
                  |  Google Auth     |  <--+
                  +------------------+     |
                                           |
+---------+        +-------------+        +------+
|   UI    | <----> | API Client  | <----> |  DB  |
+---------+        +-------------+        +------+
                       |    |
                       |    +-------> External API (Kinopoisk.dev)
                       |
                       +-----> AI Client -----> Mistral API
```

Каждый компонент — отдельный файл/папка:

| Компонент схемы | Файл / папка |
|---|---|
| **UI** | `app.py` (Streamlit) |
| **API Client** | `api/client.py` |
| **DB** | `db/models.py` + `db/database.py` (SQLite) |
| **AI Client** | `ai_client/advisor.py` |
| **External API** | `external/kinopoisk.py` (Kinopoisk.dev) |
| **Mistral** | вызывается из `ai_client/advisor.py` |
| **Google Auth** | `auth.py` |

---

## Что лежит в каждом файле

### `app.py` — UI на Streamlit
Главный файл приложения, с него начинается выполнение. Содержит весь интерфейс: проверку входа через Google и две вкладки — «Поиск фильма» (поиск + информация + разбор AI + кнопка «Хочу посмотреть») и «Хочу посмотреть» (список сохранённых фильмов с возможностью снова запросить разбор AI и удалить фильм). Сам ничего не вычисляет — только вызывает функции из `api/client.py`.

### `auth.py` — Google OAuth
Реализация входа через Google. Две функции:
- `get_login_url()` — возвращает URL, на который надо отправить пользователя для логина.
- `get_user_info(code)` — обменивает код от Google на профиль (имя, email, google_id).

### `config.py` — настройки
Загружает ключи API из файла `.env` в переменные Python.

### `db/models.py` — модели данных
Описание таблиц БД через SQLAlchemy ORM:
- `User` — пользователи (привязка к Google).
- `FavoriteMovie` — сохранённые фильмы (название, год, рейтинг, описание).

### `db/database.py` — подключение к SQLite
Создаёт движок SQLAlchemy и фабрику сессий. Функция `init_db()` создаёт таблицы при первом запуске. БД хранится в файле `movies.db` в корне проекта.

### `external/kinopoisk.py` — Kinopoisk.dev API
Обёртка над неофициальным API Кинопоиска. Главная функция:
- `find_movie(name)` — ищет фильм по названию, возвращает данные (год, рейтинг, жанры, страны, описание, постер).

Внутри есть таймауты и обработка сетевых ошибок — если API недоступен, бросается понятное исключение `MovieError`, а не «голая» ошибка requests.

### `ai_client/advisor.py` — обёртка над Mistral
Единственное место, где код знает про Mistral. Функция `get_review(movie)` отправляет данные о фильме в Mistral и получает разбор на русском языке. Обрабатывает ошибку перегрузки (429) — показывает понятное сообщение вместо краша.

### `api/client.py` — API Client (центральный слой)
Бизнес-логика приложения. Содержит функции:
- `get_or_create_user(...)` — найти или создать пользователя в БД.
- `get_movie_info(name)` — ищет фильм → получает разбор AI → возвращает всё вместе.
- `get_movie_review_only(movie)` — только разбор AI (для сохранённых фильмов, без повторного поиска).
- `get_favorites(user_id)` — список сохранённых фильмов пользователя.
- `add_favorite(user_id, movie)` — добавляет фильм в список.
- `remove_favorite(favorite_id)` — удаляет фильм из списка.

UI и БД через этот слой полностью развязаны — UI не знает ничего ни про базу, ни про внешние сервисы.

### `requirements.txt`
Список зависимостей с фиксированными версиями.

### `.env.example`
Шаблон для файла `.env` с переменными окружения. Реальный `.env` надо создать самому и заполнить своими ключами.

---

## Установка и запуск (подробно, по шагам)

### Шаг 1. Проверка Python

Нужен **Python 3.10 или выше**. В терминале выполни:

```bash
python --version
```

Если меньше 3.10 — обнови с [python.org](https://www.python.org/downloads/).

### Шаг 2. Виртуальное окружение

Распакуй архив, открой терминал в папке проекта и создай виртуальное окружение:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

После активации в строке терминала появится `(venv)`.

### Шаг 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

Займёт 1-2 минуты.

### Шаг 4. Получение Google OAuth ключей

1. Перейди на [Google Cloud Console → Credentials](https://console.cloud.google.com/apis/credentials).
2. Если у тебя ещё нет проекта — создай новый.
3. Нажми **«+ Create Credentials»** → **«OAuth client ID»**.
4. Если попросит настроить OAuth consent screen — настрой:
   - User Type: **External**
   - App name: любое (например, `Movie Guide`)
   - User support email: твой email
   - Developer contact: твой email
   - В Scopes ничего добавлять не нужно.
   - В Test users добавь свой Google-аккаунт.
5. Вернись к созданию OAuth client ID:
   - **Application type:** `Web application`
   - **Name:** любое
   - **Authorized redirect URIs:** добавь `http://localhost:8501` (точно, без слеша в конце)
6. Нажми Create. Скопируй **Client ID** и **Client Secret**.

### Шаг 5. Получение Mistral API ключа

1. Зарегистрируйся на [console.mistral.ai](https://console.mistral.ai/).
2. Перейди в раздел **API Keys** и создай новый ключ.
3. Скопируй ключ — он показывается **только один раз**.

У Mistral есть бесплатный тариф.

### Шаг 6. Получение Kinopoisk.dev API ключа

1. Открой Telegram и найди бота **@kinopoiskdev_bot** (либо перейди на [kinopoisk.dev](https://kinopoisk.dev/)).
2. Нажми Start и следуй инструкции бота — он бесплатно выдаст API-ключ.
3. Скопируй полученный ключ.

Бесплатный тариф Kinopoisk.dev даёт 200 запросов в сутки — этого с запасом хватает для учебного проекта.

### Шаг 7. Настройка `.env`

В корне проекта скопируй `.env.example` в `.env`:

**Windows:**
```bash
copy .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

Открой `.env` в любом редакторе и заполни пять строк:

```
GOOGLE_CLIENT_ID=твой_client_id_от_google
GOOGLE_CLIENT_SECRET=твой_client_secret_от_google
GOOGLE_REDIRECT_URI=http://localhost:8501
MISTRAL_API_KEY=твой_ключ_от_mistral
KINOPOISK_API_KEY=твой_ключ_от_kinopoisk
```

### Шаг 8. Запуск приложения

```bash
streamlit run app.py
```

В терминале появится:
```
Local URL: http://localhost:8501
```

Браузер откроется автоматически. Если нет — открой ссылку вручную.

### Шаг 9. Первый вход

1. Нажми **«Войти через Google»**.
2. Выбери свой Google-аккаунт.
3. Google вернёт тебя обратно — приложение залогинит.
4. Введи название фильма (например, `Матрица`) и нажми **«Найти фильм»**.

---

## Как остановить приложение

В терминале, где запущен Streamlit:
- **Ctrl + C** (Windows / Linux)
- **Cmd + C** (macOS)

Если порт 8501 остался занят:

**Windows (PowerShell):**
```powershell
netstat -ano | findstr :8501
taskkill /PID <номер_PID> /F
```

**macOS / Linux:**
```bash
lsof -ti:8501 | xargs kill -9
```

---

## Структура проекта

```
movie_guide/
├── app.py                # UI (Streamlit) — главный файл
├── auth.py               # вход через Google
├── config.py             # настройки из .env
├── requirements.txt      # зависимости
├── .env.example          # шаблон .env
├── README.md             # этот файл
├── db/
│   ├── __init__.py
│   ├── database.py       # подключение к SQLite
│   └── models.py         # таблицы User, FavoriteMovie
├── api/
│   ├── __init__.py
│   └── client.py         # API Client — бизнес-логика
├── ai_client/
│   ├── __init__.py
│   └── advisor.py        # обёртка над Mistral
└── external/
    ├── __init__.py
    └── kinopoisk.py      # обёртка над Kinopoisk.dev
```

---

## Возможные ошибки

**`redirect_uri_mismatch`** — URI в `.env` не совпадает с тем, что в Google Console. Должны быть идентичны до символа, включая отсутствие слеша в конце.

**`Access blocked: ... has not completed the Google verification process`** — добавь свой email в Test users в OAuth consent screen в Google Cloud Console.

**`401` или `403` от Kinopoisk.dev** — неверный или не активированный API-ключ. Проверь, что вставил ключ из Telegram-бота правильно.

**`AI сейчас перегружен`** — это не ошибка приложения, а перегрузка бесплатного тарифа Mistral. Подожди минуту и попробуй ещё раз.

**`Фильм не найден`** — попробуй ввести по-другому (например, полное название или год).

**`Kinopoisk.dev не отвечает / не удалось подключиться`** — проблема с сетью. Проверь интернет. Если используешь VPN — попробуй включить/выключить его.

**`Missing dependencies for SOCKS support`** — у тебя активен SOCKS-прокси/VPN, а `requests` не умеет с ним работать без доп. библиотеки. В активированном `venv` выполни `pip install PySocks`. Если pip сам идёт через тот же прокси и падает с той же ошибкой — временно убери прокси (`set ALL_PROXY=` в cmd) и поставь пакет.
