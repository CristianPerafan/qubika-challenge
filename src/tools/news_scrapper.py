from importlib.metadata import metadata

import requests

from bs4 import BeautifulSoup
from langchain_core.documents import Document

from src.agents.news_parser_agent import NewsParserAgent
from src.model.schemas import NewSnippet, New

# Set up the newsagent
news_agent = NewsParserAgent(local_agent=False)

def search_articles_urls_from_site(site_url: str, limit: int = 5) -> list[NewSnippet]:
    """
    Find news by site URL getting the title and URL of the article
    Available sites: https://www.eltiempo.com/, https://www.semana.com/
    """
    response = requests.get(site_url)
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        news_snippet_titles = soup.find_all('h2', class_='entry-title')

        if not news_snippet_titles:
            news_snippet_titles = soup.find_all('h3', class_='c-article__title')

        news_snippet_info: list[NewSnippet] = []

        for index, news_title in enumerate(news_snippet_titles):
            if index == limit:
                break

            article_url = news_title.a['href'] if news_title.a['href'].startswith('http') else site_url + news_title.a['href']

            news_snippet_info.append(NewSnippet(title=news_title.text, url=article_url, source=site_url))

        return news_snippet_info
    else:
        return []

def get_authors_from_article(response_text: str):
    soup = BeautifulSoup(response_text, 'html.parser')
    author = author_.text.strip() if (author_ := soup.find('a', class_='c-detail__author__name')) else None
    if not author:
        author_span = soup.find_all('span', class_='author vcard')
        if not author_span:
            author = 'Unknown'
        else:
            author_names = [author.find('a').text.strip() for author in author_span]
            author = ' y '.join(author_names)

    return author
def get_date_from_article(response_text: str):
    soup = BeautifulSoup(response_text, 'html.parser')
    date = date_.text.strip() if (date_ := soup.find('time', class_='c-detail__date')) else None
    if not date:
        date = date_['datetime'] if (date_ := soup.find('time', class_='entry-date published')) else 'Unknown'

    return date

def get_content_from_article(response_text: str):
    soup = BeautifulSoup(response_text, 'html.parser')
    # Remove scripts and styles
    for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'form']):
        tag.decompose()

    # Extraer solo el texto visible
    text = soup.get_text(separator=' ', strip=True)

    # Eliminar líneas vacías y espacios adicionales
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    clean_text = ' '.join(lines)

    return clean_text


def get_resources_url_from_article(response_text: str):
    soup = BeautifulSoup(response_text, 'html.parser')
    resources = soup.find_all('a', href=True)
    resources_url = [resource['href'] for resource in resources]
    return resources_url

def get_general_information_from_article(article : NewSnippet):
    """
    Get the general information of the article
    """
    author = 'Unknown'
    date = 'Unknown'
    content = 'Unknown'
    response = requests.get(article.url)
    if response.status_code == 200:
        author = get_authors_from_article(response.text)
        date = get_date_from_article(response.text)
        content = get_content_from_article(response.text)


    return author, date, content

def download_articles_from_sites(sites: list[str], limit: int = 1):
    """
    Download news articles from a list of sites
    """
    articles = []

    for site in sites:
        articles_snippets = search_articles_urls_from_site(site, limit)
        for article_snippet in articles_snippets:
            author, date, content = get_general_information_from_article(article_snippet)
            json_object = news_agent.get_structured_information_from_article(article_snippet.title, article_snippet.source, author, content, article_snippet.url)
            article = New(**json_object)
            articles.append(article)

    save_articles_to_json(articles, 'data/articles.json')


def save_articles_to_json(articles: list[New], file_name: str):
    """
    Save the articles in a json file
    """
    import json
    with open(file_name, 'w') as file:
        json.dump([article.model_dump() for article in articles], file, indent=4)


def load_articles_from_json(file_name: str)-> list[New]:
    """
    Load the articles from a json file
    """
    import json

    try:
        with open(file_name, 'r') as file:
            articles = json.load(file)
    except Exception as e:
        return []

    return [New(**article) for article in articles]

def load_articles_from_json_as_documents(file_name: str):
    """
    Load the articles from a json file as documents
    """
    news = load_articles_from_json(file_name)

    documents = []
    for article in news:
        documents.append(Document(
            page_content=article.content,
            metadata={
                "title": article.title,
                "source": article.source,
                "author": ", ".join(article.author),
                "url": article.url,
                "date": article.publication_date
            }
        ))

    return documents


