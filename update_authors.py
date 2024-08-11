import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_site_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').string
        return title if title else "Unknown Site"
    except (requests.RequestException, Exception) as e:
        print(f"\n无法获取站点标题: {url}\n错误信息: {e}")
        return "Unknown Site"

def update_authors(moments_filename, site_info_filename):
    # 读取现有的站点信息
    if os.path.exists(site_info_filename):
        with open(site_info_filename, 'r', encoding='utf-8') as file:
            site_info = json.load(file)
    else:
        site_info = {}

    # 读取解析后的 moments 文件
    if os.path.exists(moments_filename):
        with open(moments_filename, 'r', encoding='utf-8') as file:
            moments = json.load(file)
    else:
        print(f"文件 '{moments_filename}' 未找到")
        return

    # 标志位，用于判断是否有新站点被添加
    updated = False

    for moment in moments:
        parsed_url = urlparse(moment["link"])
        site_root = f"{parsed_url.scheme}://{parsed_url.netloc}"

        if site_root not in site_info:
            site_title = get_site_title(site_root)
            site_info[site_root] = site_title
            updated = True

        if moment["author"] == "Unknown Site":
            moment["author"] = site_info.get(site_root, "Unknown Site")

    # 如果有新站点被添加，更新站点信息文件
    if updated:
        with open(site_info_filename, 'w', encoding='utf-8') as file:
            json.dump(site_info, file, ensure_ascii=False, indent=4)
        print("站点信息文件已更新！")

    # 直接覆盖写入 moments 数据到原始文件
    with open(moments_filename, 'w', encoding='utf-8') as file:
        json.dump(moments, file, ensure_ascii=False, indent=4)
    print("moments.json 文件已更新！")
