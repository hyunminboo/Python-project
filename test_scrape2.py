import urllib.request
import re
from urllib.parse import quote

query = quote("손흥민".encode('euc-kr'))
url = f"https://cafe.naver.com/ArticleSearchList.nhn?search.clubid=29267144&search.menuid=58&search.searchBy=1&search.query={query}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('euc-kr', errors='ignore')
    # Extract article titles and links
    articles = re.findall(r'<a[^>]+href="(/ArticleRead\.nhn\?clubid=29267144&page=1&menuid=58&boardtype=L&articleid=\d+[^"]*)"[^>]*>([^<]+)</a>', html)
    print(len(articles))
    for href, title in articles[:5]:
        print(title.strip(), href)
except Exception as e:
    print(e)
