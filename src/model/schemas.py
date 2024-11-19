from typing import Optional

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


class VectorDBQuery(BaseModel):
    query: str
    titles: Optional[list[str]] = None
    sources: Optional[list[str]] = None
    authors: Optional[list[str]] = None
    dates: Optional[str] = None
