import time

import streamlit as st

from modules.nav import Navbar
from src.model.schemas import New

from src.agents.news_parser_agent import NewsParserAgent

from src import config




def main():
    news_parser_agent = NewsParserAgent(local_agent=False)
    st.set_page_config(page_title="Inicio", page_icon='🏠')
    st.title("Inicio 🏠")
    st.markdown(
        """
            Este es un chatbot basado en RAG que permite realizar consultas sobre noticias de dos principales fuentes de
            noticias en Colombia: El Tiempo y La Silla Vacía. Esta aplicación permite hacer scraping de las noticias de
            los sitios web de los medios de comunicación mencionados y almacenarlas en una base de datos.
        """
    )
    from src.tools.news_scrapper import load_articles_from_json
    articles: list[New] = load_articles_from_json('data/articles.json')
    st.markdown(f"Actualmente, la aplicación tiene :blue-background[{len(articles)}] noticias.")

    st.subheader("Carga de noticias")
    st.markdown(
        f"""
            El siguiente botón tiene la funcionalidad de cargar 5 noticias de los sitios web de :blue-background[El Tiempo]
            y :blue-background[La Silla Vacía] y almacenarlas en la base de datos de la aplicación para su posterior consulta.
            **Recuerda que al cargar las noticias, las noticias anteriores serán eliminadas de la base de datos**.
        """
    )

    number = st.number_input("Número de noticias a cargar por Fuente", min_value=1, max_value=10, value=5)
    agree = st.checkbox("Estoy de acuerdo")


    if st.button("Descargar noticias"):
        if not agree:
            st.error("Debes estar de acuerdo con la eliminación de las noticias anteriores.")
        else:
            with st.spinner("Descargando noticias..."):
                sites = ["https://www.eltiempo.com/", "https://www.lasillavacia.com/"]
                from src.tools.news_scrapper import download_articles_from_sites
                download_articles_from_sites(sites, number)
                st.success("Noticias descargadas con éxito.")
                config.DB_NEEDS_TO_BE_UPDATED = True



    st.markdown(
        f"""
            O en el caso de que desee, puede ingresar una url de un artículo de uno de los sitios web mencionados para
            almacenarla en la base de datos de la aplicación.
        """
    )

    url = st.text_input("URL del artículo")

    if st.button("Almacenar artículo"):
        if not url:
            st.error("Debe ingresar una URL")

    Navbar()

if __name__ == '__main__':
    main()