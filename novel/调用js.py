import requests
import execjs
import json
import urllib.parse

def encodeURI(URIstring,encoding='gbk'):
    encode_text = URIstring.encode(encoding)
    encode_text = urllib.parse.quote(encode_text)
    return encode_text

def decodeURI(URIstring,encoding='gbk'):
    encode_text = urllib.parse.unquote(URIstring,encoding)
    return encode_text

def search_novel(name="万古杀帝"):
    url = "https://www.bookbao8.com/Search/q_"
    name_encode = execjs.eval(f"encodeURIComponent(escape('{name}'))")
    seach_link = url + name_encode
    return seach_link

def url_encode(unicode_text="万古杀帝"):
    data = {
    'data': unicode_text,
    'type': 'urlencode',
    'arg': 's=gb2312_j=0_t=0'
    }
    r = requests.post('http://web.chacuo.net/charseturlencode',data=data)
    encode_text = ''
    if r.status_code == requests.codes.ok:
        json_text = json.loads(r.text)
        encode_text = json_text['data'][0]
    return encode_text
    # '%CD%F2%B9%C5%C9%B1%B5%DB'
    # '%CD%F2%B9%C5%C9%B1'

if __name__ == '__main__':
    url = search_novel()
    print(url_encode('万古杀帝'))
    print(encodeURI("万古杀帝"))
    r = requests.get(url)
    print(r.text)
