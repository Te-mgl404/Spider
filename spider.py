import optparse
import requests
import os
import re
import threading
import time
from colorama import init

init(autoreset=True)


def spider_run(url):
    """
    爬取网页中的URL
    key: 网页关键字
    url: 目标网页地址
    """

    url_list = []
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',
    }
    pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    try:
        response = requests.get(url, headers=header, timeout=1)
        text = response.text

    except:
        return
    if k == "notset":
        url_list = pattern.findall(text)
    else:
        if k in text:
            url_list = pattern.findall(text)

    return set(url_list)


def print_log():

    if l == 1:
        count = len(open("logfile.txt",'r').readlines())
        print("已爬取网页数量{}--已保存数量{}".format(len(all_url_set), count))
        threading.Timer(10, print_log).start()
    elif l >= 2:
        count = len(open("logfile.txt", 'r').readlines())
        print("\033[0;31m{}: 已爬取网页数量{}--已保存数量{}\033[0m".format(time.strftime("%H:%M:%S", time.localtime()), len(all_url_set), count))
        threading.Timer(10, print_log).start()

def write_2_file(i, url_list, fw):
    """
     写入logfile.txt
     i: 当前爬虫深度
     url_list: url列表
     fw: 保存数据的文件
    """
    for f in url_list:
        fw.write(str(i) + "#" + f + '\n')


def main(url, deep, logfile, loglevel, concurrency, key):
    """
    url: 目标网页地址
    deep: 爬虫深度
    logfile: 日志文档地址
    loglevel: 日志详细程度（1-5）
    concurrency: 线程池大小
    key: 网页关键字
    """

    # 总数据集合用于去重
    global all_url_set
    all_url_set = set()

    # 定义打印等级
    global l
    l = loglevel

    # key
    global k
    k = key

    # 数据列表
    url_set_tree = []

    # 判断必要参数是否存在，不存在则退出程序
    if url is None or deep is None:
        print("\033[0;31m============================================\033[0m")
        print("\033[0;31m==========Error: 必须参数-u  -d  ==========\033[0m")
        print("\033[0;31m============================================\033[0m")
        exit()

    # cd到创建日志的路径并创建日志文件
    os.chdir(r'' + logfile)
    fw = open("logfile.txt", "w")

    # 开启打印线程
    print_log()

    url_set = spider_run(url)

    # 第一次爬取数据保存到总数居集合
    all_url_set = url_set

    # 添加数据到列表
    url_set_tree.append([1, list(url_set)])

    # 保存数据到文件
    write_2_file(1, list(url_set), fw)

    if deep > 1:
        for i in range(2, deep-1):
            print(i)
            for j in url_set_tree[i - 2][1]:
                try:
                    url_set = spider_run(j) - all_url_set
                    all_url_set = url_set | all_url_set
                    url_set_tree.append([i, url_set])
                    write_2_file(i, list(url_set), fw)
                except BaseException:
                    pass
                if l >= 3:
                    print("正在爬取{}层{}下第{}层的URL".format(i, j, i+1))

    fw.close()
    exit()

if __name__ == '__main__':
    # 创建用户输入字典
    parser = optparse.OptionParser(
        usage='spider.py -u url -d deep -f logfile -l loglevel(1-5) --concurrrency number --key="HTML5"')
    parser.add_option(
        '-u',
        '--url',
        dest='targetURL',
        type="string",
        help="target URL ")
    parser.add_option(
        '-d',
        '--deep',
        dest='targetDEEP',
        type="int",
        help='target deep')
    parser.add_option(
        '-f',
        '--logfile',
        dest='targetLOGFILE',
        default=os.getcwd(),
        type='string',
        help='log file address')
    parser.add_option(
        '-l',
        '--loglevel',
        dest='targetLOGLEVEL',
        default='1',
        type='int',
        help='log level(1-5)')
    parser.add_option(
        '-c',
        '--concurrency',
        dest='targetCONCURRENCY',
        default='1',
        type='int',
        help='concurrency number')
    parser.add_option(
        '-k',
        '--key',
        dest='targetKEY',
        default='notset',
        type='string',
        help='keyword')
    # 获取字典值
    option, args = parser.parse_args()
    # 执行主函数

    main(
        option.targetURL,
        option.targetDEEP,
        option.targetLOGFILE,
        option.targetLOGLEVEL,
        option.targetCONCURRENCY,
        option.targetKEY
    )
