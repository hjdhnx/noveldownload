import requests
import execjs

def search_novel(name="万古杀帝"):
    url = "https://www.bookbao8.com/Search/q_"
    name_encode = execjs.eval(f"encodeURIComponent(escape('{name}'))")
    seach_link = url + name_encode
    return seach_link

if __name__ == '__main__':
    url = search_novel()
    r = requests.get(url)
    print(r.text)