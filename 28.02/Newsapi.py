import urllib.request
import urllib.parse
import json
def make_request(url, params):
    params = {k: v for k, v in params.items() if v is not None}
    if params:
        url += '?' + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except urllib.error.HTTPError as e:
        error_message = e.read().decode('utf-8')
        return {'error': e.code, 'message': error_message}
    except Exception as e:
        return {'error': 'unknown', 'message': str(e)}
def get_top_headlines(api_key, country=None, category=None, q=None, page_size=20, page=1):
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': api_key,
        'country': country,
        'category': category,
        'q': q,
        'pageSize': page_size,
        'page': page
    }
    return make_request(url, params)
def get_everything(api_key, q=None, sources=None, domains=None, from_date=None, to_date=None,
                   language=None, sort_by='publishedAt', page_size=20, page=1):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'apiKey': api_key,
        'q': q,
        'sources': sources,
        'domains': domains,
        'from': from_date,
        'to': to_date,
        'language': language,
        'sortBy': sort_by,
        'pageSize': page_size,
        'page': page
    }
    return make_request(url, params)
def get_sources(api_key, category=None, language=None, country=None):
    url = 'https://newsapi.org/v2/sources'
    params = {
        'apiKey': api_key,
        'category': category,
        'language': language,
        'country': country
    }
    return make_request(url, params)
if __name__ == '__main__':
    API_KEY = 'ваш_ключ_здесь'
    print("=== ТЕСТ get_top_headlines (новости России) ===")
    top = get_top_headlines(API_KEY, country='ru', page_size=3)
    if 'articles' in top:
        for art in top['articles']:
            print('-', art['title'])
    else:
        print('Ошибка:', top)
    print("\n=== ТЕСТ get_everything (новости про Python) ===")
    everything = get_everything(API_KEY, q='Python', language='en', page_size=3)
    if 'articles' in everything:
        for art in everything['articles']:
            print('-', art['title'])
    else:
        print('Ошибка:', everything)
    print("\n=== ТЕСТ get_sources (источники из США) ===")
    sources = get_sources(API_KEY, country='us', language='en')
    if 'sources' in sources:
        for src in sources['sources'][:5]:
            print('-', src['name'])
    else:
        print('Ошибка:', sources)