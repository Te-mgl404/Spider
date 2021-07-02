# Spider
爬取网页指定深度所有URL
##### 用法示例
python3 spider.py -u https://www.bilibili.com/ -d 5 -f 路径 -l 4  -k html

- -u --url: 指定网址（必要参数）
- -d --deep: 指定深度（必要参数）
- -f --logfile: 指定保存路径默认当前路径
- -l --loglevel: 指定打印详情等级默认1
- -k --key: 指定爬取含有关键字的网页url默认没有关键字
