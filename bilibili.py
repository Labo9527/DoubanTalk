from selenium import webdriver
import requests
import pandas as pd
import time


class Spider(object):
    def __init__(self):
        self.start_time = time.time()
        self.page = 0
        self.number = 0
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.url = 'https://space.bilibili.com/927587/video'
        self.data = {
            'titles': [],
            'play_number': [],
            'date': [],
            'url': [],
            'vote': [],
            'coin': [],
            'collection': [],
            'share': []
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36 "
        }
        self.session = requests.session()

    def run(self):
        self.driver.get(self.url)
        time.sleep(1)
        elements = self.driver.find_elements_by_class_name('title')
        plays = self.driver.find_elements_by_class_name('play')
        times = self.driver.find_elements_by_class_name('time')
        flag = False

        while True:
            flag = False
            for i in range(len(elements)):
                if i == 0:
                    continue
                self.number = self.number + 1
                self.data['titles'].append(elements[i].get_attribute('textContent'))
                self.data['url'].append(elements[i].get_attribute('href'))
                self.data['play_number'].append(plays[i - 1].get_attribute('textContent'))
                self.data['date'].append(times[i - 1].get_attribute('textContent'))
                self.driver.get(elements[i].get_attribute('href'))
                while True:
                    time.sleep(1)
                    if '点赞数0' not in self.driver.find_element_by_class_name('like').get_attribute('title'):
                        break
                print(self.driver.find_element_by_class_name('like').get_attribute('title').replace('点赞数', ''))
                self.data['vote'].append(
                    self.driver.find_element_by_class_name('like').get_attribute('title').replace('点赞数', ''))
                self.data['coin'].append(self.driver.find_element_by_class_name('coin').get_attribute('textContent'))
                self.data['collection'].append(
                    self.driver.find_element_by_class_name('collect').get_attribute('textContent'))
                self.data['share'].append(self.driver.find_element_by_class_name('share').get_attribute('textContent'))
                self.driver.back()
                time.sleep(1)
                elements = self.driver.find_elements_by_class_name('title')
                plays = self.driver.find_elements_by_class_name('play')
                times = self.driver.find_elements_by_class_name('time')

                print("第", self.page, '页，第', self.number, '个视频，', '用时', time.time() - self.start_time, '秒')

            try:
                self.driver.find_element_by_link_text('下一页').click()
                time.sleep(1)
                elements = self.driver.find_elements_by_class_name('title')
                plays = self.driver.find_elements_by_class_name('play')
                times = self.driver.find_elements_by_class_name('time')
                flag = True
                # break
            finally:
                self.page = self.page + 1
                self.number = 0
                if not flag:
                    break

        mypanda = pd.DataFrame(self.data)
        mypanda.to_csv('data.csv')

        self.driver.close()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
