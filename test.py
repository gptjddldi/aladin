import requests
import re

from bs4 import BeautifulSoup as bs
from math import ceil

from fetcher import FetchBookInfo
from book import Book
from store import Store

def gen_book_table(fetcher, isbns):
    book_table: list[Book] = []

    for isbn in isbns:
        res = fetcher.fetch(isbn)
        book_name = res['item'][0]['title']
        origin_price = res['item'][0]['priceSales']
        url = res['item'][0]['subInfo']['usedList']['userUsed']['link'].replace('&amp;', '&').replace("TabType=1", "TabType=0")

        cnt = 0
        for name in ["aladinUsed", "userUsed", "spaceUsed"]:
            cnt += res['item'][0]['subInfo']['usedList'][name]['itemCount']

        book_table.append(
            Book(book_name, origin_price, url, ceil(cnt// 20) + 1)
        )
    return book_table

def gen_store_table(book_table: list[Book]):
    store_table: list[Store] = []

    for book in book_table:
        for page in range(1, book.page_cnt):
            url = f"{book.url}&page={page}"
            res = requests.get(url)

            soup = bs(res.text, "html.parser")
            wrapper = soup.find("div", {"class": "Ere_usedsell_table"})
            ele = wrapper.find_all("tr")

            for i in ele:
                price = i.find("li", {"class": "Ere_sub_pink"})
                store_name = i.find("div", {"class": "seller"})
                
                if store_name:
                    if i.find("span", {"class": "Ere_sub_top"}).text.strip() not in (["상", "최상"]): continue

                    ship_price = int(re.sub('[a-z가-힣 :,]', '', i.find("div", {"class": "price"}).find_all("li")[2].text))
                    price = int(re.sub('[a-z가-힣 :,]', '', price.text))
                    store_url = store_name.find('a', href=True)['href']
                    store_name = store_name.text.strip()

                    b = Book(book.title, price)
                    store = next((x for x in store_table if x.name == store_name), None)
                    if store:
                        store.add_book(b)
                        store.total_price += b.price
                        store.total_origin_price += book.price
                    else:
                        store_table.append(Store(f"https://www.aladin.co.kr/{store_url}", ship_price, store_name, [b], b.price, book.price))
    return store_table

if __name__ == '__main__':
    ttb = "ttbhy_stom2118002"
    fbi = FetchBookInfo(ttb)

    isbns = [
        9788972915546, # 과학 혁명의 구조
        9788934921318, # 과학에는 뭔가 특별한 게 있다.
        9788925538297, # 스토너
        9791189198862, # 종의 기원
        9791130641423, # 지구의 짧은 역사
        9788901163673, # 바른 마음
        9788932030982, # 그리스인 조르바
        9788972914693, # 생은 다른 곳에
        9788991705364, # 어느 무명 철학자의 유쾌한 행복론
        9788925552460, # 발칙한 현대 미술사
        9788970840659, # 곰브리치 서양미술사
        9788991290099, # 명상록
        9791161750712, # kotlin in action
        ]

    book_table = gen_book_table(fbi, isbns)
    store_table = gen_store_table(book_table)

    sorted_store_table = sorted(store_table,key=lambda obj: obj.discount_rate())

    for i in sorted_store_table:
        print(i)