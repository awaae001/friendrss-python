import json
import os
import sys
from rss_tool import Tool

def printFirstTen(moments):
    print("前十个条目：")
    for moment in moments[:10]:
        print("-" * 30)
        print("标题:", moment["title"])
        print("链接:", moment["link"])
        print("发布时间:", moment["published"])
        print("摘要:", moment["summary"])
        print("作者:", moment["author"])

if __name__ == '__main__':
    with open('./urls.json', 'r', encoding='utf-8') as file:
        urls = json.load(file)
    
    moments = []
    tool = Tool(urls, moments)
    try:
        tool.parseInfo()
    except KeyboardInterrupt:
        print("\n您取消了解析操作")
        sys.exit(0)

    tool.writeContent("./json/moments.json", "./json/timeout.json")
    os.system('./ENV_DIR/bin/python3 ./update_authors.py')
    with open("./json/moments.json", 'r', encoding='utf-8') as file:
        updated_moments = json.load(file)

    # 打印前十个条目
    printFirstTen(updated_moments)

    print("主函数处理完成\n")
