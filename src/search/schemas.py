from pydantic import BaseModel

from src.search.constants import MAX_LIMIT


class SearchSchema(BaseModel):
    query: str = None
    cat: str = None
    sub_cat: str = None
    params: dict = None
    article_id: int = None
    offset: int = 0
    limit: int = MAX_LIMIT


class SearchResultSchema(BaseModel):
    offset: int
    limit: int
    data: list
    has_more: bool
