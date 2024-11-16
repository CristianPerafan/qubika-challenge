import streamlit as st

from modules.nav import Navbar

from src.model.schemas import New
from src.tools.news_scrapper import load_articles_from_json
from src.agents.news_agent import NewsAgent
from src import config


@st.cache_resource
def instantiate_news_agent():
    news_agent_instance = NewsAgent(local_agent=False)
    return news_agent_instance


def main():
    st.set_page_config(page_title="Chat", page_icon='🤖')
    st.title("Chat 🤖")

    articles:list[New] = load_articles_from_json('data/articles.json')
    if not articles:
        st.warning("No hay noticias en la base de datos")
        return

    news_agent_instance = instantiate_news_agent()


    if config.DB_NEEDS_TO_BE_UPDATED:
        news_agent_instance.setup_vector_db()
        config.DB_NEEDS_TO_BE_UPDATED = False


    with st.chat_message("assistant"):
        st.markdown(
            """
            ¡Bienvenido al chatbot de noticias! Puedo responder a tus preguntas sobre las noticias almacenadas en la base de datos.
            """
        )

    if user_input := st.chat_input("¿En qué puedo ayudarte?"):
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response = news_agent_instance.query_agent(user_input)
            st.markdown(response)











    Navbar()
if __name__ == '__main__':
    main()