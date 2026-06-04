import asyncio
import aiohttp
from app.config import get_secret


class NaverNewsScraper:
    NAVER_API_NEWS = "https://openapi.naver.com/v1/search/news.json"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

    @staticmethod
    async def fetch_image(session, url):
        try:
            # 타임아웃을 주어 응답이 너무 오래 걸리는 것을 방지
            async with session.get(url, timeout=3) as response:
                if response.status == 200:
                    # 응답의 인코딩을 무시하고 텍스트로 읽음
                    html = await response.read()
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html, 'html.parser')
                    meta_tag = soup.find('meta', property='og:image')
                    if meta_tag and meta_tag.get('content'):
                        return meta_tag['content']
        except Exception:
            pass
        return ""

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                items = result.get("items", [])
                
                # 각 기사별로 이미지를 병렬로 가져오기
                tasks = [NaverNewsScraper.fetch_image(session, item['link']) for item in items]
                images = await asyncio.gather(*tasks)
                
                for item, img_url in zip(items, images):
                    item['image'] = img_url
                    
                return items
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
