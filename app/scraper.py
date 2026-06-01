import asyncio
import aiohttp
from app.config import get_secret


class NaverNewsScraper:
    NAVER_API_NEWS = "https://openapi.naver.com/v1/search/news.json"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("items", [])
            return []

    def unit_url(self, keyword, start):
        return {
            "url": f"{self.NAVER_API_NEWS}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-Id": self.NAVER_API_ID,
                "X-Naver-Client-Secret": self.NAVER_API_SECRET
            },
        }

    async def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, 1 + i * 10) for i in range(total_page)]

        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[
                    NaverNewsScraper.fetch(session, api["url"], api["headers"])
                    for api in apis
                ]
            )
            result = []

            for data in all_data:
                if data:
                    for article in data:
                        result.append(article)

            return result

    def run(self, keyword, total_page):
        return asyncio.run(self.search(keyword, total_page))


if __name__ == "__main__":
    scraper = NaverNewsScraper()
    print(scraper.run("이적시장", 1))
