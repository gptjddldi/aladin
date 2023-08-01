import requests
import re
from bs4 import BeautifulSoup as bs
from math import ceil
from fetcher import FetchBookInfo


def gen_book_table(fetcher, isbns):
    book_table = []

    for isbn in isbns:
        res = fetcher.fetch(isbn)

        book_name = res['item'][0]['title']
        origin_price = res['item'][0]['priceSales']
        url = res['item'][0]['subInfo']['usedList']['userUsed']['link'].replace('&amp;', '&').replace("TabType=1", "TabType=0")

        cnt = 0
        for name in ["aladinUsed", "userUsed", "spaceUsed"]:
            cnt += res['item'][0]['subInfo']['usedList'][name]['itemCount']

        book_table.append({
            'title': book_name, 
            'origin_price': int(origin_price),
            'url': url,
            'page_cnt': ceil(cnt// 20) + 1
            })
    return book_table

def gen_store_table(book_table):
    store_table = []

    for book in book_table:
        for page in range(1, book['page_cnt']):
            url = f"{book['url']}&page={page}"
            res = requests.get(url)

            soup = bs(res.text, "html.parser")
            wrapper = soup.find("div", {"class": "Ere_usedsell_table"})
            ele = wrapper.find_all("tr")

            for i in ele:
                price = i.find("li", {"class": "Ere_sub_pink"})
                store_name = i.find("div", {"class": "seller"})
                
                if store_name:
                    if i.find("span", {"class": "Ere_sub_top"}).text.strip() not in (["상", "최상"]): continue

                    ship_price = re.sub('[a-z가-힣 :,]', '', i.find("div", {"class": "price"}).find_all("li")[2].text)
                    price = re.sub('[a-z가-힣 :,]', '', price.text)
                    store_name = store_name.text.strip()

                    store = next((x for x in store_table if x["name"] == store_name), None)
                    tmp_book = {
                        "title": book["title"],
                        "price": price
                    }
                    if store is not None:
                        store["books"].append(tmp_book)
                    else:
                        store_table.append({
                            "url": "123",
                            "ship_price": ship_price,
                            "name": store_name,
                            "books": [tmp_book]
                        })
    return store_table

ttb = "ttbhy_stom2118002"
fbi = FetchBookInfo(ttb)

isbns = [
    9788972915546, # 과학 혁명의 구조
    # 9788934921318, # 과학에는 뭔가 특별한 게 있다.
    # 9788925538297, # 스토너
    # 9788932003979, # 입 속의 검은 잎
    # 9788937460296, # 농담
    9791189198862, # 종의 기원
    9791130641423, # 지구의 짧은 역사
    9788901163673, # 바른 마음
    # 9788932030982, # 그리스인 조르바
    9788972914693, # 생은 다른 곳에
    9788991705364, # 어느 무명 철학자의 유쾌한 행복론
    9788925552460, # 발칙한 현대 미술사
    9788991290099, # 명상록
    ]

book_table = gen_book_table(fbi, isbns)
store_table = gen_store_table(book_table)

for i in store_table:
    print(i)