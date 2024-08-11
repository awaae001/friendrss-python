import json
import os
from urllib.parse import urlparse

def compare_urls(urls_filename, site_info_filename, output_filename):
    # 读取 URLs 文件
    if os.path.exists(urls_filename):
        with open(urls_filename, 'r', encoding='utf-8') as file:
            urls = json.load(file)
    else:
        print(f"文件 '{urls_filename}' 未找到")
        return

    # 读取站点信息文件
    if os.path.exists(site_info_filename):
        with open(site_info_filename, 'r', encoding='utf-8') as file:
            site_info = json.load(file)
    else:
        print(f"文件 '{site_info_filename}' 未找到")
        site_info = {}

    # 提取站点根 URL 集合
    site_info_urls = set(site_info.keys())
    
    # 比对并收集未找到的链接
    missing_urls = []
    for url in urls:
        if url:
            parsed_url = urlparse(url)
            site_root = f"{parsed_url.scheme}://{parsed_url.netloc}"
            if site_root not in site_info_urls:
                missing_urls.append(url)

    # 将未找到的链接保存到文件
    if missing_urls:
        with open(output_filename, 'w', encoding='utf-8') as file:
            json.dump(missing_urls, file, ensure_ascii=False, indent=4)
        print(f"未找到的链接已保存到 '{output_filename}'")
    else:
        print("所有链接在站点信息中都有记录。")

# 如果直接运行该脚本，将调用 compare_urls 函数
if __name__ == '__main__':
    urls_path = '/data/links/rss/urls.json'
    site_info_path = '/data/links/rss/json/site_info.json'
    missing_urls_path = '/data/links/rss/json/missing_urls.json'

    compare_urls(urls_path, site_info_path, missing_urls_path)
