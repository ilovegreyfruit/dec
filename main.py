import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from dec_2 import logger

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'

@logger('get_headers_log')
def get_headers():
    return Headers(browser="chrome", os="win").generate()

@logger('get_articles.log')
def get_articles(url):
    response = requests.get(url, headers=get_headers())
    
    if response.status_code != 200:
        print(f'Ошибка при загрузке страницы: {response.status_code}')
        return []
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    articles = soup.find_all('article')
    matching_articles = []

    for article in articles:
        tag_time = article.find("time")
        pub_time = tag_time["datetime"]

        h2_tag = article.find("h2")
        a_tag = h2_tag.find("a")

        link = a_tag["href"]
        link = f"https://habr.com{link}"

        preview_text = article.text.lower()

        if any(keyword.lower() in preview_text for keyword in KEYWORDS):
            matching_articles.append(f"{pub_time} – {h2_tag} – {link}")
    
    return matching_articles

if __name__ == '__main__':
    articles = get_articles(URL)
    for article in articles:
        print(article)