#!/usr/bin/env python3
#coding: utf-8

import requests
from bs4 import BeautifulSoup as bs
from db import DB
import re


_base_urls = [
    "http://www.sohu.com",
    "http://learning.sohu.com",
    "http://news.sohu.com",
    "http://history.sohu.com",
    "http://mil.sohu.com",
    "http://business.sohu.com",
    "http://it.sohu.com",
    "http://sports.sohu.com",
    "http://yule.sohu.com",
    "http://auto.sohu.com",
    # "http://fasion.sohu.com",
    "http://travel.sohu.com",
    "http://baobao.sohu.com",
    "http://health.sohu.com",
    "http://cul.sohu.com",
]


def get(url):
    sess = requests.session()
    # to simulite browser
    sess.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
    res = sess.get(url)
    return res


def get_article_link_urls(baseurl):
    urls = []
    res = get(baseurl)
    ct = res.content.decode(res.apparent_encoding)
    # http://www.sohu.com/a/345049418_428290?g=0&spm=smpc.news-home.pol-news.2.1570232553803xawophZ
    p = re.compile(r"(https?:)?//www\.sohu\.com/a/\d+_\d+")    # 忽略 ? 之后部分
    m = p.search(ct)
    while m:
        url = m.group(0)
        if url[:2] == "//":
            url = "http:" + url
        urls.append(url)
        ct = ct[m.span()[1]:]
        m = p.search(ct)
    return urls


def get_article_contents(url):
    article_classes = [
        "article",
        "article-text",
    ]

    res = get(url)
    # FIXME: 有时候 requests 无法正确判断 encoding，使用 utf-8 默认吧
    try:
        ct = res.content.decode(res.apparent_encoding)
        s = bs(ct, features="html.parser")
    except Exception as e:
        s = bs(res.content, features="html.parser")

    for name in article_classes:
        tag = s.find("article", attrs={"class": name})
        if tag:
            ps = tag.find_all("p")
            return [p.text for p in ps]

    return []


def grab(logger):
    for baseurl in _base_urls:
        urls = get_article_link_urls(baseurl)
        logger.info("enn, there are {} articles links for {}".format(len(urls), baseurl))
        db = DB()
        for url in urls:
            if db.has(url):
                continue
            ct = get_article_contents(url)
            txt = '\n'.join(ct)
            db.save(url, txt)
            logger.info("grab {} save {} bytes".format(url, len(txt)))