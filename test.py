import requests
import re
from bs4 import BeautifulSoup as bs

ttb = "ttbhy_stom2118002"
api_url = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"

request_params = {
    "TTBKey": ttb,
    "ItemIdType": "Isbn",
    "Output": "JS",
    "OptResult": "usedList",
    "Version": "20131101"
}

isbns = [
    9788972915546, # 과학 혁명의 구조
    9788934921318, # 과학에는 뭔가 특별한 게 있다.
    9788925538297, # 스토너
    9788932003979, # 입 속의 검은 잎
    9788937460296, # 농담
    9791189198862, # 종의 기원
    9791130641423, # 지구의 짧은 역사
    9788901163673, # 바른 마음
    9788932030982, # 그리스인 조르바
    9788972914693, # 생은 다른 곳에
    9788991705364, # 어느 무명 철학자의 유쾌한 행복론
    9788925552460, # 발칙한 현대 미술사
    9788991290099, # 명상록
    ]
d = {}
store = {}
books = {}
for isbn in isbns:
    request_params["ItemId"] = str(isbn)
    res = requests.get(api_url, params=request_params).json()
    book_name = res['item'][0]['title']
    origin_price = res['item'][0]['priceSales']
    books[book_name] = int(origin_price)

    URL = res['item'][0]['subInfo']['usedList']['userUsed']['link'].replace('&amp;', '&').replace("TabType=1", "TabType=0")
    cnt = 0
    for name in ["aladinUsed", "userUsed", "spaceUsed"]:
        cnt += res['item'][0]['subInfo']['usedList'][name]['itemCount']

    for i in range(1, (cnt // 20) + 2):
        page_url = URL + '&page={}'.format(i)
        res = requests.get(page_url)
        soup = bs(res.text, "html.parser")
        wrapper = soup.find("div", {"class": "Ere_usedsell_table"})
        ele = wrapper.find_all("tr")

        for i in ele:
            price = i.find("li", {"class": "Ere_sub_pink"})
            seller = i.find("div", {"class": "seller"})
            

            if seller:
                if i.find("span", {"class": "Ere_sub_top"}).text.strip() not in (["상", "최상"]): continue

                ship_price = re.sub('[a-z가-힣 :,]', '', i.find("div", {"class": "price"}).find_all("li")[2].text)
                price = re.sub('[a-z가-힣 :,]', '', price.text)

                seller = seller.text.strip()
                store[seller] = ship_price

                if seller in d:
                    if book_name not in d[seller]:
                        d[seller][book_name] = price
                else:
                    d[seller] = {}
                    d[seller][book_name] = price

for k, v in d.items():
    s1 = 0
    s2 = 0
    rate = 0
    for k1, v1 in v.items():
        s1 += int(v1)
        s2 += books[k1]
    s1 += int(store[k])
    rate = (s1 / s2) * 100
    d[k]["rate"] = rate

d = dict(sorted(d.items(), key=lambda item: item[1]["rate"]))
for k,v in d.items():
    if v["rate"] < 80:
        print(k)
        print(v)
        # print(sum(map(int, v.values())) + int(store[k]))
        print('---------------------------')