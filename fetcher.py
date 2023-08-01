import requests

class FetchBookInfo:
    def __init__(self, ttb):
        self.ttb = ttb
        self.api_url = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"

    def request_params(self):
        return {
            "TTBKey": self.ttb,
            "ItemIdType": "Isbn",
            "Output": "JS",
            "OptResult": "usedList",
            "Version": "20131101"
        }

    def fetch(self, isbn):
        params = self.request_params()
        params["ItemId"] = str(isbn)

        return requests.get(self.api_url, params=params).json()
