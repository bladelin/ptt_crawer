from ptt_crawler import crawl_ptt_lifeismoney
from line_notify import send
import sqlite3

# 创建 SQLite 连接和游标
conn = sqlite3.connect('posts.db')
cursor = conn.cursor()

# 创建一个名为 posts 的表格
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        Id TEXT PRIMARY KEY,
        title TEXT,
        url TEXT,
        date TEXT
    )
''')

def save_to_database(posts):
    for post in posts:
        # 检查数据库中是否已存在相同的 ID
        cursor.execute('SELECT Id FROM posts WHERE Id=?', (post.Id,))
        existing_post = cursor.fetchone()

        if existing_post is None:
            # 如果 ID 不存在，则插入新的帖子数据
            cursor.execute('''
                INSERT INTO posts (Id, title, url, date)
                VALUES (?, ?, ?, ?)
            ''', (post.Id, post.title, post.url, post.date))

            print(f"帖子 {post.Id} 已成功插入数据库")

            msg = post.format_line_msg()
            send(msg)
        else:
            print(f"帖子 {post.Id} 已存在于数据库中")

    # 提交更改并关闭连接
    conn.commit()

if __name__ == "__main__":
    # 要爬取的 PTT Lifeismoney 版的網址
    target_url = "https://www.ptt.cc/bbs/Lifeismoney/search?q=GoShare"

    crawled_posts = crawl_ptt_lifeismoney(target_url)

    # 将数据保存到数据库
    save_to_database(crawled_posts)

    # 关闭连接
    conn.close()
