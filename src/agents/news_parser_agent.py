import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

from src.agents.constants import GET_NEWS_STRUCTURED_INFO_PROMPT_TEMPLATE_SYSTEM, \
    GET_NEWS_STRUCTURED_INFO_PROMPT_TEMPLATE_HUMAN

from src.tools.json_tools import convert_llm_response_to_json

new_parser_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            GET_NEWS_STRUCTURED_INFO_PROMPT_TEMPLATE_SYSTEM,
        ),
        ("human",
            GET_NEWS_STRUCTURED_INFO_PROMPT_TEMPLATE_HUMAN
         ),
    ]
)

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class NewsParserAgent:
    def __init__(self, local_agent: bool):
        self.local_agent = local_agent
        self.llm = None
        self.news_parser_chain = None
        self.setup_agent()


    def setup_agent(self):
        self.set_up_llm()
        self.set_up_news_parser_chain()
        #self.load_vector_db()

    def set_up_llm(self):
        if not self.local_agent:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo-0125",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )

    def set_up_news_parser_chain(self):
        self.news_parser_chain = new_parser_prompt | self.llm



    def get_structured_information_from_article(self, title, source,author, content, url):
        response = self.news_parser_chain.invoke(
            {
                "title": title,
                "source": source,
                "author": author,
                "content": content,
                "url": url
            }
        )

        return convert_llm_response_to_json(response.content)




