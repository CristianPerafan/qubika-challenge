import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.agents.constants import GET_NEWS_STRUCTURED_INFO_PROMPT_TEMPLATE_SYSTEM, \
    GET_NEWS_STRUCTURED_INFO_PROMPT_TEMPLATE_HUMAN
from src.tools.json_tools import convert_llm_response_to_json


new_content_prompt = ChatPromptTemplate.from_messages(
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

class NewsAgent:
    def __init__(self, local_agent: bool):
        self.local_agent = local_agent
        self.chain = None

    def setup_agent(self):
        if not self.local_agent:
            llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )

            self.chain = new_content_prompt | llm

    def get_structured_information_from_article(self, title, source,author, content, url):
        response = self.chain.invoke(
            {
                "title": title,
                "source": source,
                "author": author,
                "content": content,
                "url": url
            }
        )

        return convert_llm_response_to_json(response.content)

