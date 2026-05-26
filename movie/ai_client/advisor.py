"""AI Client: получение разбора фильма от Mistral."""
from mistralai import Mistral                              # клиент Mistral

from config import MISTRAL_API_KEY                         # ключ от Mistral


def get_review(movie):                                     # получает разбор фильма от AI
    """Возвращает разбор фильма от AI: о чём фильм, кому понравится, похожие фильмы."""
    # Берём поля через .get() с запасным значением — на случай, если какого-то поля нет.
    # Это важно: у фильма из поиска есть все поля, а у сохранённого в БД — только основные.
    name = movie.get("name", "Неизвестный фильм")          # название (или заглушка)
    year = movie.get("year", "")                           # год (может отсутствовать)
    genres = movie.get("genres", "")                       # жанры (в БД не хранятся — будет пусто)
    rating = movie.get("rating", "")                       # рейтинг
    description = movie.get("description", "")             # описание

    # Готовим текст вопроса для AI с данными о фильме
    question = (                                           # собираем текст промпта
        f"Фильм: {name} ({year}). "                        # название и год
        f"Жанры: {genres}. "                               # жанры (могут быть пустыми)
        f"Рейтинг Кинопоиска: {rating}. "                  # рейтинг
        f"Описание: {description} "                        # описание из Кинопоиска
        f"Расскажи об этом фильме: чем он интересен, кому понравится, "
        f"и посоветуй 2-3 похожих фильма. "                # что должен сделать AI
        f"Ответь на русском, 4-5 предложений."             # требования к ответу
    )

    client = Mistral(api_key=MISTRAL_API_KEY)              # создаём клиент Mistral

    try:                                                   # пробуем отправить запрос
        response = client.chat.complete(                   # отправляем запрос к модели
            model="mistral-small-latest",                  # название модели
            messages=[{"role": "user", "content": question}],  # одно сообщение от пользователя
        )
        return response.choices[0].message.content         # возвращаем текст ответа
    except Exception as e:                                 # если что-то пошло не так
        error_text = str(e)                                # превращаем ошибку в текст
        if "429" in error_text or "capacity" in error_text.lower():  # частая ошибка перегрузки
            return (                                       # понятное сообщение для пользователя
                "AI сейчас перегружен (бесплатный тариф Mistral). "
                "Попробуй нажать кнопку ещё раз через минуту."
            )
        return f"Не удалось получить разбор от AI. Ошибка: {error_text}"  # любая другая ошибка
