import requests
from bs4 import BeautifulSoup

def find_news_by_site_url(site_url: str, limit: int = 5):
    """
    Find news by site URL
    Available sites: https://www.eltiempo.com/, https://www.semana.com/
    """
    response = requests.get(site_url)
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        news_titles = soup.find_all('h2', class_='card-title')


        if not news_titles:
            news_titles = soup.find_all('h3', class_='c-article__title')

        news_info = []

        for index, news_title in enumerate(news_titles):
            if index == limit:
                break

            article_url = news_title.a['href'] if news_title.a['href'].startswith('http') else site_url + news_title.a['href']
            news_info.append({
                'title': news_title.text,
                'url': article_url
            })

        return news_info
    else:
        print('An error has occurred while getting the news')
        return []

url = "https://www.eltiempo.com/colombia/"

news = find_news_by_site_url(url)

for new in news:
    print(new['title'])
    print(new['url'])
    print()

