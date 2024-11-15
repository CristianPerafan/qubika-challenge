from pydantic import BaseModel

class NewSnippet(BaseModel):
    title: str
    url: str
    source: str

class New(NewSnippet):
    content: str
    author:list[str]
    publication_date: str
    resources_url: list[str]