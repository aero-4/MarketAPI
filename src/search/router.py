from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from src.middlewares.ratelimit import rate_limit, get_ip_client
from src.search.constants import LIMIT_SEARCH_REQ, WINDOW_SEARCH_REQ
from src.search.schemas import SearchSchema, SearchResultSchema
from src.search.search_service import search_last_items

search_router = APIRouter(prefix="/search", tags=["Search"])


@search_router.post("/", response_model=SearchResultSchema)
@rate_limit(limit=LIMIT_SEARCH_REQ, window=WINDOW_SEARCH_REQ, key_func=lambda request, *a, **kw: get_ip_client(request))
async def search_handler(request: Request, schema: SearchSchema):
    try:
        search = await search_last_items(schema)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Try again later")
    return search
