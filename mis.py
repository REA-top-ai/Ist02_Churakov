
import requests
from datetime import datetime, timedelta
import json


NEWS_API_KEY = "8bc30f206dcd4214a41727b5cc7df765"
MISTRAL_API_KEY = "GPSB8WT7zmFMRv4mrDJIGOLikiP52OsB"
TOPIC = "технологии"



def get_articles_from_newsapi(topic: str, api_key: str, days_back: int = 1):
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "from": from_date,
        "to": to_date,
        "sortBy": "publishedAt",
        "language": "ru",
        "apiKey": api_key,
        "pageSize": 50
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "ok":
        raise Exception(f"NewsAPI error: {data.get('message', 'Unknown error')}")

    articles = []
    for item in data.get("articles", []):
        articles.append({
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "content": item.get("content", ""),
            "url": item.get("url", "")
        })
    return articles


def generate_annotation(articles, topic: str, mistral_key: str) -> str:
    news_text = ""
    for i, art in enumerate(articles[:20], 1):
        title = art["title"][:200] if art["title"] else "Без заголовка"
        desc = art["description"][:300] if art["description"] else "Нет описания"
        news_text += f"{i}. {title}\n   {desc}\n\n"

    if not news_text:
        return "Не найдено статей по заданной теме за последний день."

    prompt = f"""Ты — профессиональный аналитик новостей. На основе приведённых ниже статей по теме «{topic}» за последние сутки напиши краткую аналитическую аннотацию на русском языке объёмом 250–300 слов.

В аннотации:
- Выдели главные события и тренды.
- Оцени, что произошло за последний день в этой сфере (динамика, неожиданные факты, ключевые фигуры/компании).
- Дай обобщающий вывод.

Статьи:
{news_text}

Аннотация:"""


    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {mistral_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 800
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    annotation = result["choices"][0]["message"]["content"].strip()
    return annotation


def main():
    print(f"Загружаем статьи по теме '{TOPIC}' за последний день...")
    articles = get_articles_from_newsapi(TOPIC, NEWS_API_KEY)
    print(f"Найдено статей: {len(articles)}")

    if not articles:
        print("Нет статей. Проверьте тему или ключ NewsAPI.")
        return

    print("Отправляем запрос в Mistral AI...")
    annotation = generate_annotation(articles, TOPIC, MISTRAL_API_KEY)

    with open("text", "w", encoding="utf-8") as f:
        f.write(annotation)

    print("Готово! Аннотация сохранена в файл 'text'.")
    print("\n--- АННОТАЦИЯ ---")
    print(annotation)


if __name__ == "__main__":
    main()