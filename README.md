# friendrss-python

一个简单的小脚本，用来识别RSS并生成一个json文件供给友链区使用。

## 运行

你需要安装以下库：

- `feedparser`：用于解析 RSS 订阅源。
- `beautifulsoup4`：用于解析 HTML 文档。
- `requests`：用于发起 HTTP 请求。

并确保再你解析器文件夹下面存在**pytho虚拟环境**

如果你要使用计划任务；

请修改，将相对路径替换为绝对路径

```python
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
```
