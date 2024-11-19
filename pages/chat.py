import streamlit as st

import shortuuid

from modules.nav import Navbar

from src.model.schemas import New
from src.tools.news_scrapper import load_articles_from_json
from src.agents.news_agent import NewsAgent
from src import config
from src.tools.voice import verify_audio_exists, get_audio_path, text_to_speech, autoplay_audio


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
    else:
        pass

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"id": shortuuid.uuid(),"role": "assistant", "content": "¡Bienvenido al chatbot de noticias! Puedo responder a tus preguntas sobre las noticias almacenadas en la base de datos."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if st.button("🔈", key=message["id"]):
                with st.spinner("Cargando audio..."):
                    audio_file = None
                    if verify_audio_exists(message["id"]):
                        audio_file = get_audio_path(message["id"])
                    else:
                        print(message["id"])
                        audio_file = text_to_speech(message["content"], message["id"])
                    autoplay_audio(audio_file)




    if user_input := st.chat_input("¿En qué puedo ayudarte?"):
        st.session_state.messages.append({"id": shortuuid.uuid(), "role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Pensando🤔.."):
                response = news_agent_instance.advance_query(user_input)
                print(response)
                id_ = shortuuid.uuid()
                st.session_state.messages.append({"id": id_,"role": "assistant", "content": response})
                st.markdown(response)
                if st.button("🔈", key=id_):
                    with st.spinner("Cargando audio..."):
                        audio_file = text_to_speech(response, id_)
                        autoplay_audio(audio_file)











    Navbar()
if __name__ == '__main__':
    main()