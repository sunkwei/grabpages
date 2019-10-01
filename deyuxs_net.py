#!/usr/bin/env python3
#coding: utf-8

from grab_stack import get_matched_link, get_page_content
from db import DB


# 主页模式
_deyuxs_net_all = [
    ("div", {
        "id": "main"
    }),
    ("div", {
        "class": ["novellist"]
    }),
    ("ul", None),
    ("li", None),
    ("a", None),
]


# 小说总章模式
# _novel_main = [
#     ("div", {
#         "id": "list"
#     }),
#     ("dl", None),
# ]

# 文章模式
_art_pattern = [
    ("div", {
        "id": "content"
    }),
    ("p", None),
]


def my_get_urls(tag):
    return [tag["href"]]


# def my_get_urls2(tag):
#     aa = tag.find_all("a")
#     return [a["href"] for a in aa]

def my_get_article_url(logger, url):
    ''' url: http://www.deyuxs.net/detail/<aid>/
        从中提取 aid

        然后在收到的 body 中，匹配 /detail/<aid>/<cid>.html 链接返回
    '''
    import requests
    import re
    
    m = re.search(r"/detail/([0-9]+)/", url)
    if m is None:
        logger.warning("there is no links in {}".format(url))
        return []

    aid = m[1]
    p = re.compile(r"/detail/{}/[0-9]+\.html".format(aid))

    try:
        res = requests.get(url)
        cn = res.content.decode("gbk")
    except Exception as e:
        logger.warning("request excp: url:{}, {}".format(url, e))
        return []

    urls = []
    m = p.search(cn)
    while m is not None:
        u = m.group(0)
        if u not in urls:
            urls.append(u)
        span = m.span()
        cn = cn[span[1]:]
        m = p.search(cn)

    return urls

    


def my_get_cont(tag):
    return tag.text



def grab(logger):
    baseurl = "http://www.deyuxs.net"
    db = DB("deyuxs.db")
    n_urls = get_matched_link(logger, _deyuxs_net_all, baseurl + "/all", my_get_urls, max_url_count=3)
    for n_url in n_urls:
        n_url = baseurl + n_url
        #a_urls = get_matched_link(logger, _novel_main, n_url, my_get_urls2, True)
        # 文档不准确，需要手动提取 url 列表
        # <dd><a href="/detail/11770/5230228.html" class="f-green">1</a></a></dd>  多了一个 </a> 导致 bs4 解析失败
        a_urls = my_get_article_url(logger, n_url)
        for a_url in a_urls:
            a_url = baseurl + a_url
            txt = ""
            cs = get_page_content(logger, _art_pattern, a_url, my_get_cont)
            for c in cs:
                txt += c

            if txt:
                db.save(a_url, txt)
            logger.info("{} saved, {} bytes".format(a_url, len(txt)))
            