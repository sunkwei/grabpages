#!/usr/bin/env python3
#coding: utf-8


__all__ = ["grab"]

# 抓取 sohu 几个网站的网页

_www_sohu_com = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["wrapper-box"],
    }),
    ("div", {
        "class": ["area"],
    }),
    ("div", {
        "class": ["main"],
    }),
    ("div", {
        "class": ["main-box"],
    }),
    ("div", {
        "class": ["main-left"],
    }),
    ("div", {
        "class": ["list16"],
    }),
    ("ul", None),
    ("li", None),    
]

_news_sohu_com = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["wrapper-box"],
    }),
    ("div", {
        "class": [],
    }),
    ("div", {
        "class": ["area"],
    }),
    ("div", {
        "class": ["main"],
    }),
    ("div", {
        "class": ["clearfix"],
    }),
    ("div", {
        "class": ["left"],
    }),
    ("div", {
        "class": ["list16"],
    }),
    ("ul", None),
    ("li", None),
]

_it_sohu_com = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["wrapper-box"],
    }),
    ("div", {
        "class": ["area"],
    }),
    ("div", {
        "class": ["z-section"],
    }),
    ("div", {
        "class": ["z-section-left"],
    }),
    ("div", {
        "class": ["z-section-1-main"],
    }),
    ("div", {
        "class": ["clear"],
    }),
    ("div", {
        "class": ["z-c-block"],
    }),
    ("ul", None),
    ("li", None),
]

_learning_sohu_com = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["wrapper-box"],
    }),
    ("div", {
        "class": ["area"],
    }),
    ("div", {
        "class": ["z-section"],
    }),
    ("div", {
        "class": ["z-section-left"],
    }),
    ("div", {
        "class": ["z-section-1-main"],
    }),
    ("div", {
        "class": ["clear"],
    }),
    ("div", {
        "class": ["z-c-block"],
    }),
    ("ul", None),
    ("li", None),
]

_business_sohu_com = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["wrapper-box"],
    }),
    ("div", {
        "class": ["area"],
    }),
    ("div", {
        "class": ["z-section"],
    }),
    ("div", {
        "class": ["z-section-left"],
    }),
    ("div", {
        "class": ["z-section-1-main"],
    }),
    ("div", {
        "class": ["clear"],
    }),
    ("div", {
        "class": ["z-c-block"],
    }),
    ("ul", None),
    ("li", None),    
]

_history_sohu_com = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["wrapper-box"],
    }),
    ("div", {
        "class": ["area"],
    }),
    ("div", {
        "class": ["z-section"],
    }),
    ("div", {
        "class": ["z-section-left"],
    }),
    ("div", {
        "class": ["z-section-1-main"],
    }),
    ("div", {
        "class": ["clear"],
    }),
    ("div", {
        "class": ["z-c-block"],
    }),
    ("ul", None),
    ("li", None),    
]

_sport_sohu_com = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["wrapper-box"],
    }),
    ("div", {
        "class": ["main-wrapper"],
    }),
    ("div", {
        "class": ["s-three"],
    }),
    ("div", {
        "class": ["clear"],
    }),
    ("div", {
        "class": ["s-three_left"],
    }),
    ("div", {
        "class": ["clear"],
    }),
    ("div", {
        "class": ["z-c-block"],
    }),
    ("ul", None),
    ("li", None),    
]


_sites = {
    "http://www.sohu.com": _www_sohu_com,
    "http://news.sohu.com": _news_sohu_com,
    "http://it.sohu.com": _it_sohu_com,
    "http://business.sohu.com": _business_sohu_com,
    "http://sports.sohu.com": _sport_sohu_com,
    "http://learning.sohu.com": _learning_sohu_com,
    "http://history.sohu.com": _history_sohu_com,
}


# 需要提取内容的页面的模式
_content_pattern = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["wrapper-box"],
    }),
    ("div", {
        "class": ["area"],
    }),
    ("div", {
        "class": ["left"],
    }),
    ("div", {
        "data-spm": "content",
    }),
    ("div", {
        "class": ["text"],
    }),
    ("article", {
        "class": ["article"],
    }),
]


from db import DB
import bs4
from bs4 import BeautifulSoup as bs
import requests
from grab_stack import GrabStack


_db = DB()


def parse_tag(pattern: list, tag: bs4.element.Tag, stack: GrabStack, urls: list, logger):
    stack.push(tag.name, tag)
    for o in tag:
        # print("path:'{}', name:'{}', type:'{}'".format(stack.get_path(moreinfo=1), o.name, type(o)))
        if stack.is_match_path(pattern):
            # 找到匹配，....，提取里面的 <a href=....>，将链接保存到 list 中
            logger.debug("fond match: {}".format(tag))
            aa = tag.find_all('a')[0]
            url = aa["href"]
            urls.append(url)
            
        elif isinstance(o, bs4.element.Tag):
            parse_tag(pattern, o, stack, urls, logger)

    stack.pop()


def parse_content(tag, stack, contents, logger):
    stack.push(tag.name, tag)
    # print("path:'{}', name:'{}', type:'{}'".format(stack.get_path(moreinfo=1), tag.name, type(tag)))

    if stack.is_match_path(_content_pattern):
        logger.debug("found matched content!")

        for c in tag:
            if isinstance(c, bs4.element.Tag):
                if "class" in c.attrs and "ql-align-center" in c.attrs["class"]:
                    # 图片,
                    continue
                if c.contents:
                    contents.append(c.contents[0])
        
    for o in tag:
        if isinstance(o, bs4.element.Tag):
            parse_content(o, stack, contents, logger)
    stack.pop()


def grab_page(url, logger):
    if url[0] == '/' and url[1] == '/':
        url = "http:" + url

    if _db.has(url):
        return 0

    logger.info("to grab:{}".format(url))
    res = requests.get(url)
    soup = bs(res.content, features="lxml")
    for o in soup:
        if isinstance(o, bs4.element.Tag):
            stack = GrabStack()
            contents = []
            parse_content(o, stack, contents, logger)
            #artical = ''.join(contents)  # 将段落构造为文章
            artical = ""                  # FIXME: 实际发现，可能包含非句子的情况
            for c in contents:
                if isinstance(c, str):
                    artical += c
            _db.save(url, artical)  # 保存
            logger.info("db save {}".format(url))
            break



def grab_site(baseurl, pattern, logger):
    logger.info("begin grab baseurl='{}'".format(baseurl))
    res = requests.get(baseurl)
    soup = bs(res.content, features="lxml")
    for o in soup:
        if isinstance(o, bs4.element.Tag):
            stack = GrabStack()
            urls = []
            parse_tag(pattern, o, stack, urls, logger)

            # urls 为需要抓取的网页 ...
            for url in urls:
                grab_page(url, logger)

            logger.info("{}: {} pages saved".format(baseurl, len(urls)))



def grab(logger):
    for url,pattern in _sites.items():
        grab_site(url, pattern, logger)
