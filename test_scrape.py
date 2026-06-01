import urllib.request
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://cafe.naver.com/ArticleList.nhn?search.clubid=29267144&search.menuid=58&search.boardtype=L"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('euc-kr', errors='ignore')
    
    # We want <a href="/ArticleRead.nhn?..." class="article">title</a>
    # Naver Cafe often renders the list inside a form or table, let's just grab article titles
    articles = re.findall(r'<a[^>]+href="(/ArticleRead\.nhn\?clubid=29267144[^"]*)"[^>]*class="article"[^>]*>\s*(.*?)\s*</a>', html, re.DOTALL)
    print("Found:", len(articles))
    for href, title in articles[:5]:
        # Clean up tags in title if any
        title = re.sub(r'<[^>]+>', '', title)
        print(title.strip(), href)
except Exception as e:
    print(e)
