import requests
from bs4 import BeautifulSoup
import time

"""
登录可以用：POST实现，但是可能会被ban ip
比较稳妥的方法是：手动复制浏览器窗口cookies先验证程序，然后用selenium模拟登录自动保存cookies给session
"""


class DouBanLogin(object):
    def __init__(self, account, password):
        self.url = "https://accounts.douban.com/j/mobile/login/basic"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        """初始化数据"""
        self.data = {
            "ck": "",
            "name": account,
            "password": password,
            "remember": "true",
            "ticket": ""
        }
        self.session = requests.Session()
        self.storage = []

    def get_cookie(self):
        """模拟登陆获取cookie"""
        html = self.session.post(
            url=self.url,
            headers=self.headers,
            data=self.data
        ).json()
        if html["status"] == "success":
            print("恭喜你，登陆成功")
        else:
            cookies = 'bid=wfSMUo5YPs0; douban-fav-remind=1; ll="118281"; douban-profile-remind=1; gr_user_id=f4da66a7-01a0-4ba9-830a-8ceb9564bdc4; _vwo_uuid_v2=D73E6116BDE614E12C493E5BD473F397C|e40f1cad4cc4ecc5aebb24b384336d23; push_doumail_num=0; __utmv=30149280.20601; viewed="1858164_6058992"; __utmz=30149280.1581608430.12.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=30149280; ct=y; ap_v=0,6.0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1585210820%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DeEXGV4xs39p4boYL6mPz-_8Am8QPZeWoDgOJZhGNX5yWuu3was83KmEP8Z2PTlsq%26wd%3D%26eqid%3Da3f3ed6b0002dfa8000000065e456dde%22%5D; _pk_ses.100001.8cb4=*; push_noty_num=0; __utma=30149280.1233736280.1577424517.1585205646.1585210829.18; dbcl2="206013216:7bdTiZMTYPg"; ck=ON_k; _pk_id.100001.8cb4=e023f81f4291a5b8.1571901009.75.1585211662.1585208908.; __utmt=1; __utmb=30149280.27.7.1585211667701'
            cookies2 = self.cookie_to_dic(cookies)
            print(cookies2)
            for k, v in cookies2.items():
                self.session.cookies.set(k,v)

    def cookie_to_dic(self, cookie):
        cookie_dic = {}
        for i in cookie.split('; '):
            cookie_dic[i.split('=')[0]] = i.split('=')[1]
        return cookie_dic

    def get_user_data(self):
        """获取用户数据表明登陆成功"""
        # TODO: 这里填写你用户主页的url
        url = "https://www.douban.com/group/?start=50"
        # 获取用户信息页面
        html = self.session.get(url, headers=self.headers).text
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        # 获取所有的链接
        links = soup.find_all('a', 'title')
        titles = [link.string for link in links]

        if len(titles) == 0:
            print("Wrong!")

        for title in titles:
            if title not in self.storage:
                self.storage.append(title)
                response = self.Talk(title)
                self.Post(links[titles.index(title)]['href'], response)
                print(title)
                print("回复:", response)
                time.sleep(3)

        # print(links)
        # print(links[0]['href'])

    def Talk(self, text):
        res = self.session.post("https://api.ownthink.com/bot?appid=xiaosi&userid=user&spoken="+text)
        # print(res.json()['data']['info']['text'])
        return res.json()['data']['info']['text']

    def Post(self, url, text):
        print(url)
        # self.Post("https://www.douban.com/group/topic/169115463/")
        data = {
            'ck': 'ON_k', # 这个参数会变，有点烦的
            'rv_comment': text,
            'img': '(binary)',
            'start': '0',
            'submit_btn': '发送'
        }
        print(self.session.post(url+"add_comment", headers=self.headers, data=data))


    def run(self):
        """运行程序"""
        # self.Talk("你好")
        self.get_cookie()

        while True:
            print("Refresh!")
            self.get_user_data()
            self.Talk("你好")
            time.sleep(10)


if __name__ == '__main__':
    account = '18027479799' # input("请输入你的账号:")
    password = '123123qqq' # input("请输入你的密码:")
    login = DouBanLogin(account, password)
    login.run()