import feedparser
import json
from bs4 import BeautifulSoup
import sys
import warnings
from datetime import datetime
from dateutil import parser as date_parser
from urllib.error import URLError, HTTPError

warnings.filterwarnings("ignore", category=UserWarning)

class Tool:
    def __init__(self, urls, moments):
        self.urls = urls
        self.moments = moments
        self.failed_urls = []  # 用于存储解析失败的链接

    def parseInfo(self):
        total_urls = len(self.urls)
        print("开始解析 RSS 订阅源...")
        for idx, url in enumerate(self.urls, 1):
            if url:
                try:
                    # 解析 RSS 订阅源
                    feed = feedparser.parse(url)
                    # 遍历解析后的条目，并将其转换为字典格式
                    for entry in feed.entries[::-1]:  # 逆序遍历条目，确保最新的条目在列表的末尾
                        # 统一日期格式
                        entry.published = self.uniformDate(entry.published)
                        # 使用 BeautifulSoup 处理 HTML 文本，提取纯文本内容
                        soup = BeautifulSoup(entry.summary, 'html.parser', from_encoding='utf-8')
                        summary_text = soup.get_text()
                        moment = {
                            "title": entry.title,
                            "link": entry.link,
                            "published": entry.published,
                            "summary": summary_text
                        }
                        self.moments.append(moment)  # 将新的条目添加到列表中
                    # 更新进度条
                    progress = (idx - 1) / total_urls * 100  # 注意索引从0开始，所以要减1
                    sys.stdout.write("\rProgress: [{:<50}] {:.2f}%".format('=' * int(progress / 2), progress))
                except (URLError, HTTPError, Exception) as e:
                    self.failed_urls.append(url)  # 记录解析失败的链接
                    print(f"\n解析失败: {url}\n错误信息: {e}")
                sys.stdout.flush()

        print("\n解析完成！")
        # 按时间排序，越新的越靠前
        self.sortByTime()

    def writeContent(self, filename, failed_filename):
        # 只保留前250个条目
        moments_to_save = self.moments[:250]
        print("解析后的条目数量:", len(self.moments))
        # 将解析后的条目列表转换为 JSON 格式并写入文件
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(moments_to_save, file, ensure_ascii=False, indent=4)
        print("数据写入完成！")
        # 将解析失败的链接写入文件
        with open(failed_filename, 'w', encoding='utf-8') as file:
            json.dump(self.failed_urls, file, ensure_ascii=False, indent=4)
        print("解析失败的链接已写入文件:", failed_filename)

    def printFirstTen(self):
        print("前十个条目：")
        for moment in self.moments[:10]:
            print("-" * 30)
            print("标题:", moment["title"])
            print("链接:", moment["link"])
            print("发布时间:", moment["published"])
            print("摘要:", moment["summary"])

    def sortByTime(self):
        # 使用 sorted 函数对条目列表进行排序，按照发布时间的倒序排列
        self.moments = sorted(self.moments, key=lambda x: x["published"], reverse=True)

    def uniformDate(self, date_string):
        # 将日期字符串转换为 datetime 对象
        try:
            date = date_parser.parse(date_string)
            return date.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return date_string

if __name__ == '__main__':
    # 从 urls.json 文件中读取 urls 列表
    with open('urls.json', 'r', encoding='utf-8') as file:
        urls = json.load(file)
    
    moments = []
    tool = Tool(urls, moments)
    tool.parseInfo()
    tool.printFirstTen()
    tool.writeContent("./moments.json", "./timeout.json")
    print("主函数处理完成\n")
