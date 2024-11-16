import streamlit as st

from modules.nav import Navbar
from src.tools.news_scrapper import load_articles_from_json


def main():
    st.set_page_config(page_title="Noticias", page_icon='📰')
    st.title("Noticias 📰")
    news = load_articles_from_json('data/articles.json')
    for new in news:
        with st.expander(f"{new.title} - {new.source}"):
            st.write(f"**Autor:** {new.author}")
            st.write(f"**Fecha de publicación:** {new.publication_date}")
            st.write(f"**Contenido:** {new.content}")
            st.write(f"**URL:** {new.url}")
    Navbar()
if __name__ == '__main__':
    main()