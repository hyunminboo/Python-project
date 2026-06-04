from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient

from app.models import mongodb
from app.models.article import ArticleModel
from app.scraper import NaverNewsScraper


app = FastAPI()


BASE_DIR=Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR /"static"),name="static")
templates = Jinja2Templates(directory=BASE_DIR/ "templates")


@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"title":"축구 소식"}
    ) 


@app.get("/search",response_class=HTMLResponse)
async def read_item(request:Request,q:str="축구 이적시장"):
    keyword=q

    naver_news_scraper=NaverNewsScraper()

    articles = await naver_news_scraper.search(keyword,10)


    favorite_articles = await mongodb.engine.find(
        ArticleModel,
        ArticleModel.is_favorite==True
        )

    favorite_links =[article.link for article in favorite_articles]

    article_models=[]

    for article in articles:
        article_model=ArticleModel(
            keyword=keyword,
            title=article["title"],
            pubDate=article["pubDate"],
            link=article["link"],
            description=article.get("description", ""),
            image=article.get("image", None)
        )

        if article_model.link in favorite_links:
            article_model.is_favorite=True

        article_models.append(article_model)

  

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context= {"keyword":q,"articles":article_models,"next_url":f"/search?q={q}"}
    )

@app.post("/favorites")
async def toggle_favorite(
    request:Request,
    keyword:str =Form(...),
    title:str=Form(...),
    pubDate:str=Form(...),
    link:str=Form(...),
    description:str=Form(""),
    image:str=Form(""),
    next_url:str=Form("/")
):
    favorite_article =await mongodb.engine.find_one(
        ArticleModel,
        (ArticleModel.keyword==keyword)
        & (ArticleModel.link==link)
        &(ArticleModel.is_favorite==True)
    )    
    if favorite_article:
        await mongodb.engine.delete(favorite_article)

    else:
        article=ArticleModel(
            keyword=keyword,
            title=title,
            pubDate=pubDate,
            link=link,
            description=description,
            image=image if image else None,
            is_favorite=True
        )
        await mongodb.engine.save(article)

    return RedirectResponse(url=next_url,status_code=303)


@app.get("/favorites",response_class=HTMLResponse)
async def favorites(request:Request):
    articles = await mongodb.engine.find(ArticleModel,ArticleModel.is_favorite==True)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title":"즐겨찾기 목록",
            "articles":articles,
            "next_url":"/favorites"
        }
    )


@app.on_event("startup")
async def on_app_start():
    print("hello server")
    mongodb.connect()

@app.on_event("shutdown")
async def on_app_shutdown():
    print("goodbye server")
    mongodb.close()
