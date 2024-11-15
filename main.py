import os

from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from src.tools.news_scrapper import download_articles_from_sites

sites = ['https://www.eltiempo.com/', 'https://www.lasillavacia.com/']

download_articles_from_sites(sites, limit=1)