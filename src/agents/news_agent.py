from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from src import config
from src.agents.constants import NEWS_AGENT_PROMPT_TEMPLATE_SYSTEM, NEWS_AGENT_PROMPT_TEMPLATE_HUMAN
from src.db.chroma_db import  save_to_chroma_v2
from src.tools.news_scrapper import load_articles_from_json_as_documents, load_articles_from_json
from src.tools.text_processor import chunk_text

news_agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            NEWS_AGENT_PROMPT_TEMPLATE_SYSTEM,
        ),
        ("human",
            NEWS_AGENT_PROMPT_TEMPLATE_HUMAN
        ),
    ]
)

class NewsAgent:
    def __init__(self, local_agent: bool):
        self.local_agent = local_agent
        self.llm = None
        self.question_chain = None
        self.embedding_model = None
        self.vector_db = None
        self.setup_agent()

    def setup_embedding_model(self):
        self.embedding_model = OpenAIEmbeddings(
            model="text-embedding-3-large"
        )

    def set_up_llm(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo-0125",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        self.question_chain = news_agent_prompt | self.llm

    def setup_vector_db(self):
        documents = load_articles_from_json_as_documents('data/articles.json')
        documents = chunk_text(documents)
        self.vector_db = save_to_chroma_v2(documents, self.embedding_model)
        config.DB_NEEDS_TO_BE_UPDATED = False

    def setup_agent(self):
        self.setup_embedding_model()
        self.set_up_llm()

    def query_document(self, query: str):
        return self.vector_db.similarity_search_with_score(query,3)

    def query_agent(self, question:str):
        documents = self.query_document(question)
        news = load_articles_from_json('data/articles.json')

        context = "\n\n---\n\n".join([
            f"**Título**: {doc.metadata.get('title', 'Sin título')}\n"
            f"**Autor**: {', '.join(doc.metadata.get('author', ['Desconocido']))}\n"
            f"**Fecha de publicación**: {doc.metadata.get('publication_date', 'Fecha desconocida')}\n"
            f"**Fuente**: [{doc.metadata.get('url', 'Sin fuente')}]\n\n"
            f"{doc.page_content}"
            for doc, _score in documents
        ])

        response = self.question_chain.invoke(
            {
                "question": question,
                "context": context,
                "news": "\n".join([f"- {new.title} - {new.source} - {new.author}" for new in news])
            }
        )

        return response.content


