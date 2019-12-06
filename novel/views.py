from django.shortcuts import render,HttpResponse
from .models import Novel
from .novel_download import *
from django.http import StreamingHttpResponse
import pypinyin
# Create your views here.

# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

# 带声调的(默认)
def yinjie(word):
    s = ''
    # heteronym=True开启多音字
    for i in pypinyin.pinyin(word, heteronym=True):
        s = s + ''.join(i) + " "
    return s

def index(request):
    return HttpResponse("django work<br><a href='novel/'>测试</a></br><a href='/admin'>后台</a></br><a href='/novel/edit/'>小说下载页面</a>")

def novel_index(request):
    return render(request,'novel/index.html')

def novel_list(request):
    return render(request,'novel/novel_list.html')

def novel_edit(request):
    return render(request,'novel/novel_edit.html')
def download_action(request):
    def file_iterator(file_name,chunk_size=512):
        with open(file_name,encoding='utf-8') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    a = request.GET
    if a.get('name'):
        name = a.get('name')
        filepath = os.getcwd() + "/novel/downloads/"+name
        if os.path.exists(filepath):
            # print(filepath)
            response =  StreamingHttpResponse(file_iterator(filepath))
            response['Content-Type'] = 'application/octet-stream'
            name_pinyin = pinyin(name)
            response['Content-Disposition'] = f'attachment; filename={name_pinyin}'
            return response
    return HttpResponse("错误，未找到该文件的相关下载！<br>也许还在后台下载中，请隔段时间再试")

def edit_action(request):
    novelindex = request.POST["novelindex"]  #得到小说章节列表链接
    name,author,noveltype,_ = getAll(url=novelindex)
    if name:
        Novel.objects.create(name = name,author = author,noveltype = noveltype,novelindex = novelindex)
        t1 = time()
        name, _, _, novel_list = getAll(url=novelindex)
        cwd = os.getcwd()+"/novel/"
        if not os.path.exists(f"{cwd}downloads/" + name):
            os.mkdir(f"{cwd}downloads/" + name)
        runApp(novel_list, name,t1,cwd)
        return HttpResponse(f"it's ok<br>{name} {author} {noveltype}<br><a href='/novel/download/?name={name}.txt'>大约等三分钟点击下载</a>")
    else:
        return HttpResponse("错误，未找到该文件的相关下载！")