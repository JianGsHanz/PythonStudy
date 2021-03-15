import json
import os
import random
import re
import time
from collections import deque
from urllib.parse import urljoin

import bs4
import requests
from selenium import webdriver

LI_A_PATTERN = re.compile(r'<li class="item">.*?</li>')
A_TEXT_PATTERN = re.compile(r'<a\s+[^>]*?>(.*?)</a>')
A_HREF_PATTERN = re.compile(r'<a\s+[^>]*?href="(.*?)"\s*[^>]*?>')


def decode_page(page_bytes, charsets):
    """通过指定的字符集对页面进行解码"""
    for charset in charsets:
        try:
            return page_bytes.decode(charset)
        except UnicodeDecodeError:
            pass


def get_matched_parts(content_string, pattern):
    """从字符串中提取所有跟正则表达式匹配的内容"""
    return pattern.findall(content_string, re.I) \
        if content_string else []


def get_matched_part(content_string, pattern, group_no=1):
    """从字符串中提取跟正则表达式匹配的内容"""
    match = pattern.search(content_string)
    if match:
        return match.group(group_no)


def get_page_html(seed_url, *, charsets=('utf-8',)):
    """获取页面的HTML代码"""
    resp = requests.get(seed_url)
    if resp.status_code == 200:
        return decode_page(resp.content, charsets)


def repair_incorrect_href(current_url, href):
    """修正获取的href属性"""
    if href.startswith('//'):
        href = urljoin('http://', href)
    elif href.startswith('/'):
        href = urljoin(current_url, href)
    return href if href.startswith('http') else ''


def start_crawl(seed_url, pattern, *, max_depth=-1):
    """开始爬取数据"""
    new_urls, visited_urls = deque(), set()
    new_urls.append((seed_url, 0))
    while new_urls:
        current_url, depth = new_urls.popleft()
        if depth != max_depth:
            page_html = get_page_html(current_url, charsets=('utf-8', 'gbk'))
            contents = get_matched_parts(page_html, pattern)
            for content in contents:
                text = get_matched_part(content, A_TEXT_PATTERN)
                href = get_matched_part(content, A_HREF_PATTERN)
                if href:
                    href = repair_incorrect_href(current_url, href)
                print(text, href)
                if href and href not in visited_urls:
                    new_urls.append((href, depth + 1))


def re_crawl_use():
    """主函数"""
    start_crawl(
        seed_url='http://sports.sohu.com/nba_a.shtml',
        pattern=LI_A_PATTERN,
        max_depth=2
    )


def requestsuse():
    resp = requests.get('http://www.baidu.com')
    print(resp.status_code)
    print(resp.headers)
    print(resp.cookies)
    print(resp.content.decode('utf-8'))
    resp = requests.post('http://httpbin.org/post', data={'name': 'zyh', 'age': 10})
    print(resp.text)
    print(resp.json())
    # URL参数和请求头。
    resp = requests.get(url='https://movie.douban.com/top250', headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;'
                  'q=0.9,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3;q=0.9',
    })
    print(resp.status_code)
    # 设置代理服务器
    requests.get('https://www.taobao.com', proxies={
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:1080',
    })


def re_use():
    PATTERN = re.compile(r'<a[^>]*?>\s*<span class="title">(.*?)</span>')
    for page in range(10):
        resp = requests.get(f'https://movie.douban.com/top250?start={page * 25}', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3;q=0.9',
        })
        items = PATTERN.findall(resp.text)
        for item in items:
            print(item)
        time.sleep(random.randint(1, 5))


def bs4_use():
    for page in range(10):
        resp = requests.post(url='https://movie.douban.com/top250', headers={  # F12 -> NetWork -> header
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome / "
                          "86.0.4240.111 Safari/537.36FS",
            "Accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, "
                      "image / webp, image / apng, * / *;q = 0.8, application/signed - exchange; v = b3; q = 0.9 ",
            "Accept-Language": "zh - CN, zh;q = 0.9, zh - TW;q = 0.8, en - US;q = 0.7, en;q = 0.6, zh - HK;q = 0.5"
        })

        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        elements = soup.select('.info>div>a')  # .info>div>a 表示 作用到info下一级div的下一级a标签,后面的必须是前面的直接子节点才行
        for element in elements:
            span = element.select_one('.title')
            print(span.text)
        time.sleep(random.random() * 5)


def re_bs4_use():
    base_url = 'https://www.zhihu.com/'
    resp = requests.get(urljoin(base_url, 'explore'), headers={
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome / "
                      "86.0.4240.111 Safari/537.36FS",
        "Accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, "
                  "image / webp, image / apng, * / *;q = 0.8, application/signed - exchange; v = b3; q = 0.9 ",
        "Accept-Language": "zh - CN, zh;q = 0.9, zh - TW;q = 0.8, en - US;q = 0.7, en;q = 0.6, zh - HK;q = 0.5"
    })
    # print(resp.text)
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    pattern = re.compile(r'^/question')
    items = soup.find_all('a', {'href': pattern})
    for item in items:
        url = urljoin(base_url, item.attrs['href'])
        print(url)
    print(soup.img.get('src'))


def get_page_text(url):
    req = requests.get(url, headers={
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome / "
                      "86.0.4240.111 Safari/537.36FS",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8, application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5"
    })

    req.encoding = 'utf8'
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    find = soup.find('div', class_='chapter_content')
    return find.text


def bs4_crawl_sanguo():
    global text
    req = requests.get('https://www.shicimingju.com/book/sanguoyanyi.html', headers={
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome / "
                      "86.0.4240.111 Safari/537.36FS",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8, application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5"
    })
    # print(req.encoding)
    req.encoding = 'utf8'
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    a_list = soup.select('.book-mulu>ul>li>a')
    print(soup.select('a')[0])
    print(soup.find_all('a'))
    f = open('三国演义.txt', 'w', encoding='utf-8')
    for a in a_list:
        print(f'开始下载...{a.text}')
        text = get_page_text('https://www.shicimingju.com' + a['href'])
        f.write(a.text + '\n' + text + '\n')
        print(f'结束下载...{a.text}')
        time.sleep(1)
    f.close()


uid_id_pattern = re.compile(r'.*?uid=(\d+).*?picid=(\d+).*?')
header = {
    "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.111Safari / 537.36FS"
}


# 下载图片
def save_image(url, uid, id):
    try:
        req = requests.get(url, stream=True)
        # 获取文件扩展名
        file_name_prefix, file_name_ext = os.path.splitext(url)
        save_path = os.path.join('C:/Users/agoto/Desktop/temp', uid + '_' + id + file_name_ext)
        with open(save_path, 'wb') as f:
            f.write(req.content)
        # print(f'image saved! {url}')
    except IOError as e:
        print(f'save error {e} {url}')
    pass


# 打开大图
def open_images_url(img_url):
    uid_id_match = uid_id_pattern.search(img_url)
    if not uid_id_match:
        return
    else:
        uid = uid_id_match.group(1)
        id = uid_id_match.group(2)

    req = requests.get(img_url, headers=header)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    results = soup.select('div.bm_c div.c a')
    for result in results:
        save_image(result.img['src'], uid, id)


# 解析图片url
def parser_image_url(page_url):
    req = requests.get(page_url, headers=header)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    results = soup.select('div.ptw li div.c a')
    for result in results:
        # 打开相册
        req = requests.get(result['href'], headers=header)
        soup1 = bs4.BeautifulSoup(req.text, 'html.parser')
        results = soup1.select('div.bm_c ul li a')
        for res in results:
            open_images_url(res['href'])

    # 爬取下一页
    next_page = soup.select_one('a.nxt')
    if next_page:
        print(next_page['href'].replace('amp;', ''))
        parser_image_url(next_page['href'].replace('amp;', ''))


base_url = "http://www.kuwo.cn/"


def parser_music(name, rid):
    req = requests.get(
        'http://www.kuwo.cn/url?format=mp3&rid=' + rid + '&response=url&type=convert_url3&br=128kmp3&from=web&t=1613803964479&httpsStatus=1&reqId=3be78401-7348-11eb-aabf-65bf1bc40149',
        headers={
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.111Safari / 537.36FS",
            "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9",
            "Cookie": "_ga = GA1.2.1315607311.1613724954;_gid = GA1.2.1053286323.1613724954;SL_GWPT_Show_Hide_tmp = 1;SL_wptGlobTipTmp = 1;gid = bf9a41d2 - bc73 - 4ff3 - b154 - 99f137ce3584;Hm_lvt_cdb524f42f0ce19b169a8071123a4797 = 1613724954, 1613725720, 1613730199, 1613785391;_gat = 1;Hm_lpvt_cdb524f42f0ce19b169a8071123a4797 = 1613786178;kw_token = 8EDCG6HQTG",
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "max-age=0",
            "Host": "www.kuwo.cn",
            "If-None-Match": "2812f-2mZh1gRxSFf1Az+O5yWKgXhxq1o",
            "Upgrade-Insecure-Requests": "1",
            "Connection": "keep-alive"

        })
    dict_json = json.loads(req.text)
    print(dict_json['url'])
    req = requests.get(dict_json['url'], stream=True)
    with open(f'C:/Users/agoto/Desktop/temp/{name.replace(" ", "")}.mp3', 'wb') as f:
        f.write(req.content)
    print(f'{name} download success')


def kuwo_music(wd, beforePage=None):
    time.sleep(10)
    soup = bs4.BeautifulSoup(wd.page_source, 'html.parser')
    results = soup.select('div.list_out div ul.rank_list li div.song_name')
    for result in results:
        # parser_music(result.a.attrs['title'], result.a.attrs['href'][13:])
        print(result.a.attrs['title'])
    elements = wd.find_element_by_css_selector('i.li-page.iconfont.icon-icon_pagedown')
    page = wd.find_element_by_css_selector('span.notCursor.currentPage')
    if beforePage != page.text:
        beforePage = page.text
        wd.execute_script('arguments[0].click();', elements)
        kuwo_music(wd, beforePage)
    else:
        wd.quit()
    pass


if __name__ == '__main__':
    # re_crawl_use()
    # requestsuse()

    # 解析豆瓣top250中文
    # 正则
    # re_use()
    # BeautifulSoup
    # bs4_use()

    # 解析获取知乎问题链接
    # re_bs4_use()

    # 爬取三国演义txt
    # bs4_crawl_sanguo()

    # 爬取空姐网图片
    # parser_image_url('http://www.kongjie.com/home.php?mod=space&do=album&view=all')
    # 爬酷我音乐VIP
    # web = webdriver.Chrome()
    # web.get('http://www.kuwo.cn/rankList')
    # time.sleep(10)
    # element = web.find_elements_by_class_name('name')[4]
    # web.execute_script('arguments[0].click();', element)
    # kuwo_music(web)

    wd = webdriver.Chrome()
    wd.get('https://home.vip.youku.com/?spm=a2ha1.14919748_WEBHOME_GRAY.drawer4.d_zj2_1')
    soup = bs4.BeautifulSoup(wd.page_source,'html.parser')
    items = soup.select('div.m-basic-drawer div.c-basiclist div.c-basiclist-wrapper div.c-basiclist-slide div.c-basicitem')
    for item in items:
        print(json.loads(item.a['data-trackinfo'])['object_title'])
        print(item.a['href'])
        req = requests.get(item.a['href'], stream=True)
        print(req.content)
    wd.quit()
    pass
