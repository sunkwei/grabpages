#!/usr/bin/python3
#coding: utf-8

# https://bbs.hupu.com/cycling

from xinhuanet import get
from db import DB
from bs4 import BeautifulSoup as bs
import re


class Site:
    def __init__(self, baseurl, title, pattern=None, encoding=None):
        self.baseurl_ = baseurl
        # /29676449.html
        self.pattern_ = r"/\d+\.html"
        if pattern:
            self.pattern_ = pattern
        self.title_ = title
        self.encoding_ = "utf-8"
        if encoding:
            self.encoding_ = encoding


_sites = [
    Site("https://bbs.hupu.com/sports", "运动场"),
    Site("https://bbs.hupu.com/cycling", "自行车"),
    Site("https://bbs.hupu.com/bxj", "步行街"),
    Site("https://bbs.hupu.com/digital", "数码"),
    
]


def get_urls(logger, site):
    res = get(site.baseurl_)
    p = re.compile(site.pattern_)
    ct = res.content.decode(site.encoding_)
    urls = []
    m = p.search(ct)
    while m:
        url = m.group(0)
        url = "https://bbs.hupu.com" + url
        urls.append(url)
        ct = ct[m.span()[1]:]
        m = p.search(ct)
    return urls


def get_txt(logger, url):
    # FIXME: 这里无法抓取内容，可能是 res 做了什么处理？
    res = get(url)
    if res.status_code == 404:
        logger.error("{} got 404".format(url))
        return ""
        
    ct = res.content.decode("utf-8")
    s = bs(ct, features="html.parser")
    tbodies = s.find_all("tbody")
    ts = [tb.text for tb in tbodies]
    return '\n'.join(ts)


def grab(logger):
    db = DB()
    for site in _sites:
        urls = get_urls(logger, site)
        logger.info("there are {} urls in {}".format(len(urls), site.title_))

        for url in urls:
            if db.has(url):
                continue

            txt = get_txt(logger, url)
            db.save(url, txt)
            logger.info("\t{} saved {} bytes".format(url, len(txt)))