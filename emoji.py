import requests
from urllib.error import URLError
import urllib.request as ur
from bs4 import BeautifulSoup
import time
import logging
import socket
import json
import re

REG = re.compile('<[^>]*>')
reImg = re.compile('(https).*/.jpg')


def extract_answer(s):
    temp_list = REG.sub("", s).replace("\n", "").replace(" ", "")
    return temp_list


def extract_imgs(s):
    temp_list = BeautifulSoup(s, 'html.parser').find_all('img')
    res = []
    for temp in temp_list:
        # print(temp)
        res.append(temp['src'])
    return res


def save_img(index, url):
    if '.jpg' not in url:
        return
    # print('正在存储,', url)
    filename = '../' + 'emoji' + '/' + str(index) + '.jpg'
    while True:
        try:
            data = ur.urlopen(url, timeout=5).read()
            f = open(filename, 'wb')
            f.write(data)
            f.close()
            break
        except socket.timeout:
            time.sleep(10)
        except URLError:
            time.sleep(10)
        except Exception:
            pass


headers = {
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://www.zhihu.com',
    'referer': 'https://www.zhihu.com/question/290268306',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

start_url = 'https://www.zhihu.com/api/v4/questions/286837417/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics\u0026limit=5\u0026offset=0\u0026platform=desktop\u0026sort_by=default'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
next_url = [start_url]
answers = []
imgs = []
isEnd = False
countImg = 1
for url in next_url:
    print(url)
    while True:
        try:
            logging.info(url)
            html = requests.get(url, headers=headers)
            html.encoding = html.apparent_encoding
            soup = BeautifulSoup(html.text, "lxml")
            # print(soup)
            content = str(soup.p).split("<p>")[1].split("</p>")[0]
            c = json.loads(content)
            # print(c["data"][0]["content"])
            imgs = []
            answers += [extract_answer(item["content"]) for item in c["data"] if extract_answer(item["content"]) != ""]
            for item in c['data']:
                imgs.extend(extract_imgs(item["content"]))
            next_url.append(c["paging"]["next"])

            for img in imgs:
                if imgs.index(img) % 10 == 0:
                    print('进度 ', imgs.index(img) / len(imgs))
                save_img(countImg, img)
                countImg += 1

            if c["paging"]["is_end"]:
                isEnd = True

            break

        except requests.exceptions.SSLError as e:
            print("SSL ERROR")
    if isEnd:
        break

for item in answers:
    print(item)
print(len(answers))
print(imgs)
