from lxml import etree
import requests
from threading import Thread,enumerate
import os
from time import sleep,time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

def thread_it(func,*args):
    t = Thread(target=func,args=args)
    t.setDaemon(True)
    t.start()

def getAll(url = "http://www.wanbenxiaoshuo.net/files/article/html/0/6/"):
    url = url.replace("index.html","")
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        r.encoding = r.apparent_encoding
        ret = r.text
        page_source = etree.HTML(ret)
        name = page_source.xpath('//*[@id="wp"]/div/div[2]/h1/text()')
        author = page_source.xpath('//*[@id="wp"]/div/div[2]/p/a/text()')
        novel_type = page_source.xpath('//*[@id="wp"]/div/div[2]/p/text()[2]')
        novel_list = page_source.xpath('//*[@id="wp"]/div/div[3]/div/ul/li/a/@href')
        novel_list = [(url+i) for i in novel_list]
        if len(name) > 0:
            return name[0],author[0],novel_type[0],novel_list
        else:
            return None,None,None,None

def getOne(link='http://www.wanbenxiaoshuo.net/files/article/html/0/6/51713.html'):
    r = requests.get(link, headers=headers)
    if r.status_code == 200:
        r.encoding = r.apparent_encoding
        ret = r.text
        page_source = etree.HTML(ret)
        node_title = page_source.xpath('//*[@id="content"]/div[1]/h1/text()')
        node_content = page_source.xpath('//*[@id="content"]/div[2]/text()')
        if len(node_title) > 0:
            content = ''.join(node_content[1:]).replace("\r\n\xa0\xa0\xa0\xa0","").replace("\n\t\t\xa0\xa0\xa0\xa0","")
            content = content.replace("\n\t\t","")
            return node_title[0], content
        else:
            return None, None

def writeOne(title,content):
    txt = "\t\t"+title+"\n"+content+"\n\n"
    return txt

def runApp(novel_list,name,t1,cwd=''):
    article_num = len(novel_list)
    xc_num = article_num//20+1
    print(f"待开启线程数量为{xc_num}")

    def inter(link,f,i):
        try:
            title, content = getOne(link)
            txt = writeOne(title, content)
            f.write(txt)
            print(f"\r线程{i}正在写入 {title}", end="")
        except Exception as e:
            print("\n爬得太快被拒绝连接，等1s递归继续")
            sleep(1)
            inter(link,f,i)

    def inner(name,i,begin,end,cwd):
        f = open(f"{cwd}downloads/{name}/{i}.txt", mode='w+', encoding='utf-8')
        for link in novel_list[begin:end]:
            inter(link, f,i)
            if link == novel_list[end - 1]:
                print(f"\n线程{i}执行完毕")
                print(f"\n剩余线程数量{len(enumerate())}")
                base_xc = 2 if not cwd else 4
                if len(enumerate()) <= base_xc:
                    print(enumerate())
                    print("\n全本下载完毕")
                    t2 = time()
                    print(f"\n本次下载小说总共耗时{round(t2 - t1)}s")
                    hebing(f"{cwd}downloads/{name}")

        f.close()

    for i in range(1,xc_num+1):
        begin = 20*(i-1)
        end = 20*i if i != xc_num else article_num
        if i == xc_num:
            print(f"\n全部线程开启完毕")
        thread_it(inner,name,i,begin,end,cwd)
        sleep(0.5)

def paixuRule(elem):
    return int(elem.split(".")[0])

def hebing(path):
    dirs = os.listdir(path)
    dirs.sort(key=paixuRule, reverse=False)
    f = open(path+".txt",mode='w+',encoding='utf-8')
    for file in dirs:
        with open(path+"/"+file,mode="r",encoding="utf-8") as f1:
            f.write(f1.read())
    f.close()
    print("小说合并完成")

if __name__ == '__main__':
    t1 = time()
    name,_,_,novel_list = getAll(url = "http://www.wanbenxiaoshuo.net/files/article/html/0/68/index.html")
    if not os.path.exists("downloads/" + name):
        os.mkdir("downloads/" + name)
    runApp(novel_list,name,t1)
    while True:
        pass