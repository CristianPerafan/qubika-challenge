from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from src import config
from src.agents.constants import NEWS_AGENT_PROMPT_TEMPLATE_SYSTEM, NEWS_AGENT_PROMPT_TEMPLATE_HUMAN, \
    TUNE_VECTOR_DB_QUERY_PROMPT_TEMPLATE_SYSTEM, TUNE_VECTOR_DB_QUERY_PROMPT_TEMPLATE_HUMAN
from src.db.chroma_db import save_to_chroma_v2, load_from_chroma
from src.model.schemas import VectorDBQuery
from src.tools.news_scrapper import load_articles_from_json_as_documents, load_articles_from_json
from src.tools.text_processor import chunk_text
from src.tools.json_tools import convert_llm_response_to_json


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

tune_vector_db_query_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            TUNE_VECTOR_DB_QUERY_PROMPT_TEMPLATE_SYSTEM,
        ),
        ("human",
            TUNE_VECTOR_DB_QUERY_PROMPT_TEMPLATE_HUMAN
        ),
    ]
)

class NewsAgent:
    def __init__(self, local_agent: bool):
        self.local_agent = local_agent
        self.llm = None
        self.question_chain = None
        self.tune_vector_db_query_chain = None
        self.embedding_model = None
        self.vector_db = None
        self.setup_agent()

    def setup_embedding_model(self):
        self.embedding_model = OpenAIEmbeddings(
            model="text-embedding-3-large"
        )

    def set_up_second_llm(self):
        self.tune_vector_db_query_chain = tune_vector_db_query_prompt | self.llm


    def set_up_llm(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
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

    def load_vector_db(self):
        self.vector_db = load_from_chroma(self.embedding_model)


    def setup_agent(self):
        self.setup_embedding_model()
        self.set_up_llm()
        self.set_up_second_llm()

    def query_document(self, query: str):
        return self.vector_db.similarity_search_with_score(query,3)

    def advance_query(self, user_query: str):

        news = load_articles_from_json('data/articles.json')

        tuned_response = self.tune_vector_db_query_chain.invoke(
            {
                "query": user_query
            }
        )

        json_response = convert_llm_response_to_json(tuned_response.content)

        structured_query = VectorDBQuery(**json_response)

        print(f"Structured query: {structured_query.query}")


        combined_filter = self.combine_filters(structured_query)

        if combined_filter:

            base_retriever = self.vector_db.as_retriever(search_kwargs={'k': 4, 'filter': combined_filter})
            context = base_retriever.invoke(structured_query.query)

            structured_context = "\n\n---\n\n".join([
                f"**Título**: {doc.metadata.get('title', 'Sin título')}\n"
                f"**Autor**: {', '.join(doc.metadata.get('author', ['Desconocido']))}\n"
                f"**Fecha de publicación**: {doc.metadata.get('publication_date', 'Fecha desconocida')}\n"
                f"**Fuente**: [{doc.metadata.get('url', 'Sin fuente')}]\n\n"
                f"{doc.page_content}"
                for doc in context
            ])

            response = self.question_chain.invoke(
                {
                    "question": structured_query.query,
                    "context": structured_context,
                    "news": "\n".join([f"- {new.title} - {new.source} - {new.author}" for new in news])
                }
            )

            return response.content
        else:
            return self.query_agent(user_query)

    @staticmethod
    def combine_filters(structured_query: VectorDBQuery):
        filters = []

        # Solo agregar filtros que tengan valores
        if structured_query.titles:
            filters.append({"title": {"$in": structured_query.titles}})
        if structured_query.sources:
            filters.append({"source": {"$in": structured_query.sources}})
        if structured_query.authors:
            filters.append({"author": {"$in": structured_query.authors}})
        if structured_query.dates:
            filters.append({"publication_date": structured_query.dates})

        if len(filters) > 1:
            combined_filter = {"$or": filters}
        elif filters:
            combined_filter = filters[0]
        else:
            combined_filter = None

        return combined_filter


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


