#!/usr/bin/env python3
#coding: utf-8


from grab_stack import get_matched_link, get_page_content
from db import DB


# 抓取简书首页
_jianshu_com = [
    ("div", {
        "id": "list-container",
    }),
    ("ul", None),
    ("li", None),
    ("div", {
        "class": ["content"]
    }),
    ("a", {
        "class": ["title"]
    })
]


def my_get_urls(tag):
    # tag: <a class="title" href="...">
    url = tag["href"]
    return [url]    # 返回列表


# 文章页面
_content_pattern = [
    ("div", {
        "id": "__next",
    }),
    ("div", None),  # class="_21bLU4 _3kbg6I"
    ("div", None),  # class="_3VRLsv" role="main"
    ("div", None),  # class="_gp-ck"
    ("section", None), # class="ouvJEz"
    ("article", None),  # class="_2rhmJa"
]


def my_get_content(tag):
    return tag.text


def grab(logger):
    db = DB()
    urls = get_matched_link(logger, _jianshu_com, "https://jianshu.com", my_get_urls)
    for url in urls:
        if url[0] == "/":
            url = "https://jianshu.com" + url
        if db.has(url):
            continue

        txt = ""
        cs = get_page_content(logger, _content_pattern, url, my_get_content, True)
        for c in cs:
            txt += c

        if txt:
            db.save(url, txt)
        logger.info("{} saved {} bytes".format(url, len(txt)))
