import pprint
import sys
import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from pymongo import MongoClient

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2145291155',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
client = MongoClient()
db = client['weibo']
collection = db['weibo']
max_page = 1


def get_page(page):
    params = {
        'type': 'uid',
        'value': '2145291155',
        'containerid': '1076032145291155',
        'page': page
    }
    url = base_url + urlencode(params)
    # print(url)
    # sys.exit(0)

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json):
    if json:
        # print(pprint.pformat(json.get("data")))
        json = json.get("data")
        # print(list(json.keys()))  # ['cardlistInfo', 'cards', 'scheme']
        # print(type(json))
        # print(json.keys())
        # sys.exit(0)
        items = json.get('cards')
        # print(items)
        # sys.exit(0)
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            print(weibo)
            # sys.exit(0)
            yield weibo


# def save_to_mongo(result):
#     if collection.insert(result):
#         print('Saved to Mongo')


if __name__ == '__main__':
    for page in range(1, max_page + 1):
        json = get_page(page)
        # print(json)
        # sys.exit(0)
        results = parse_page(json)
        for result in results:
            print(result)
            # save_to_mongo(result)
