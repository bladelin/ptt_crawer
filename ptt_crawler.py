import requests
import re
from bs4 import BeautifulSoup

class Post:
    def __init__(self,Id, title, url, date):
        self.Id = Id
        self.title = title
        self.url = url
        self.date = date

    def format_line_msg(self):
        url = "https://www.ptt.cc%s" % (self.url)
        return f"{self.title} \n傳送門： {url} \n"

    def __str__(self):
        return f"Id: {self.Id}\n,Title: {self.title}\nURL: {self.url}\nDate: {self.date}\n"

def crawl_ptt_lifeismoney(url):

    posts_list = []
    # 使用 requests 庫來獲取網頁內容
    response = requests.get(url)
    
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML 內容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找出所有 class 為 r-ent 的元素
        posts = soup.find_all(class_="r-ent")
        
        # 提取每個元素內 class 為 title 的內容和超連結的網址，並抓取日期

        for post in posts:
            title_element = post.find(class_="title")
            title = title_element.text.strip()

            # 檢查是否有超連結，並取得超連結的 URL
            if title_element.find('a'):
                url = title_element.find('a')['href']
            else:
                url = None


            # 使用正则表达式从 URL 中提取目标部分
            pattern = r"/([^/]+)\.html$"
            matches = re.search(pattern, url)

            if matches:
                Id = matches.group(1)
            else:
                print("未找到匹配的部分")

            # 提取日期
            date = post.find(class_="date").text.strip()

            # 將資料封裝為 Post 物件並加入列表中
            new_post = Post(Id, title, url, date)
            posts_list.append(new_post)
    return posts_list

if __name__ == "__main__":
    # 要爬取的 PTT Lifeismoney 版的網址
    target_url = "https://www.ptt.cc/bbs/Lifeismoney/search?q=GoShare"
    
    crawled_posts = crawl_ptt_lifeismoney(target_url)

    # 印出每個貼文的資料
    for post in crawled_posts:
        print(post)

