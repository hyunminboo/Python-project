from odmantic import Model
from pydantic import ConfigDict
from typing import Optional

class ArticleModel(Model):
    __annotations__ = {
        "keyword": str,
        "title": str,
        "pubDate": str,
        "link": str,
        "description": str,
        "image": Optional[str],
        "is_favorite": bool,
    }
    keyword: str
    title: str
    pubDate: str
    link: str
    description: str
    image: Optional[str] = None
    is_favorite: bool = False
    model_config = {"collection": "articles"}
