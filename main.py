import json
import os
import sys
from rss_tool import Tool
from update_authors import update_authors  # 导入 update_authors 函数

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
    urls_path = '/data/links/rss/urls.json'
    moments_path = '/data/links/rss/json/moments.json'
    timeout_path = '/data/links/rss/json/timeout.json'
    site_info_path = '/data/links/rss/json/site_info.json'

    try:
        with open(urls_path, 'r', encoding='utf-8') as file:
            urls = json.load(file)
    except FileNotFoundError:
        print(f"文件 '{urls_path}' 未找到")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"读取 '{urls_path}' 时发生 JSON 解码错误")
        sys.exit(1)

    moments = []
    tool = Tool(urls, moments)
    try:
        tool.parseInfo()
    except KeyboardInterrupt:
        print("\n您取消了解析操作")
        sys.exit(0)
    except Exception as e:
        print(f"解析过程中发生错误: {e}")
        sys.exit(1)

    try:
        tool.writeContent(moments_path, timeout_path)
    except Exception as e:
        print(f"写入文件时发生错误: {e}")
        sys.exit(1)

    # 直接调用 update_authors 函数
    update_authors(moments_path, site_info_path)

    try:
        with open(moments_path, 'r', encoding='utf-8') as file:
            updated_moments = json.load(file)
    except FileNotFoundError:
        print(f"文件 '{moments_path}' 未找到")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"读取 '{moments_path}' 时发生 JSON 解码错误")
        sys.exit(1)

    # 打印前十个条目
    printFirstTen(updated_moments)

    print("主函数处理完成\n")
