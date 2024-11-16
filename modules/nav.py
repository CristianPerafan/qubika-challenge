import streamlit as st


def Navbar():
    with st.sidebar:
        st.page_link('app.py', label='Inicio', icon='🏠')
        st.page_link('pages/chat.py', label='Chat', icon='🤖')
        st.page_link('pages/news.py', label='Noticias', icon='📰')