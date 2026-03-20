import requests
import json
from datetime import datetime, timedelta, timezone

NEWS_API_KEY = "ключ"

def main():
    from_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    response = requests.get("https://newsapi.org/v2/everything", params={
        "q": "technology",
        "language": "en",
        "from": from_date,
        "sortBy": "relevancy",
        "pageSize": 100,
        "apiKey": NEWS_API_KEY,
    }, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("status") != "ok":
        raise ValueError(f"Ошибка NewsAPI: {data.get('message')}")
    result = []
    for article in data.get("articles", []):
        if len(result) == 50:
            break
        if article.get("title") and article.get("url") and len(article.get("description") or "") >= 50:
            result.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "published": article.get("publishedAt", ""),
                "Author": article.get("author") or "Не указан",
            })
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
