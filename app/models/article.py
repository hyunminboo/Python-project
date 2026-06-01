from odmantic import Model
from pydantic import ConfigDict

class ArticleModel(Model):
    __annotations__ = {
        "keyword": str,
        "title": str,
        "pubDate": str,
        "link": str,
        "description": str,
        "is_favorite": bool,
    }
    keyword: str
    title: str
    pubDate: str
    link: str
    description: str
    is_favorite: bool = False
    model_config = {"collection": "articles"}
