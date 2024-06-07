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
                    feed = feedparser.parse(url)
                    for entry in feed.entries[::-1]:
                        entry.published = self.uniformDate(entry.published)
                        soup = BeautifulSoup(entry.summary, 'html.parser', from_encoding='utf-8')
                        summary_text = soup.get_text()
                        moment = {
                            "title": entry.title,
                            "link": entry.link,
                            "published": entry.published,
                            "summary": summary_text,
                            "author": "Unknown Site"  # 将作者设置为 Unknown Site
                        }
                        self.moments.append(moment)
                    progress = (idx - 1) / total_urls * 100
                    sys.stdout.write("\rProgress: [{:<50}] {:.2f}%".format('=' * int(progress / 2), progress))
                except (URLError, HTTPError, Exception) as e:
                    self.failed_urls.append(url)
                    print(f"\n解析失败: {url}\n错误信息: {e}")
                sys.stdout.flush()
        print("\n解析完成！")
        self.sortByTime()

    def writeContent(self, filename, failed_filename):
        moments_to_save = self.moments[:999]
        print("解析后的条目数量:", len(self.moments))
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(moments_to_save, file, ensure_ascii=False, indent=4)
        print("数据写入完成！")
        with open(failed_filename, 'w', encoding='utf-8') as file:
            json.dump(self.failed_urls, file, ensure_ascii=False, indent=4)
        print("解析失败的链接已写入文件:", failed_filename)

    def sortByTime(self):
        self.moments = sorted(self.moments, key=lambda x: x["published"], reverse=True)

    def uniformDate(self, date_string):
        try:
            date = date_parser.parse(date_string)
            return date.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return date_string

