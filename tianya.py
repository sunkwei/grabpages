#!/usr/bin/env python3
#coding: utf-8

import requests, re
from db import DB
from bs4 import BeautifulSoup as bs


_sites = [
    {
        "title": "天涯杂谈",
        "baseurl": "http://bbs.tianya.cn/list-free-1.shtml",
        "pattern": r"/post-free-\d+-1\.shtml",
    },
    {
        "title": "新闻众评",
        "baseurl": "http://bbs.tianya.cn/list-news-1.shtml",
        "pattern": r"/post-news-\d+-1\.shtml",
    },
    {
        "title": "我的大学",
        "baseurl": "http://bbs.tianya.cn/list-university-1.shtml",
        "pattern": r"/post-university-\d+-1\.shtml",
    },
    {
        "title": "关天茶馆",
        "baseurl": "http://bbs.tianya.cn/list-no01-1.shtml",
        "pattern": r"/post-no01-\d+-1\.shtml",
    },
    {
        "title": "闲闲书话",
        "baseurl": "http://bbs.tianya.cn/list-books-1.shtml",
        "pattern": r"/post-books-\d+-1\.shtml",
    },
    {
        "title": "国际观察",
        "baseurl": "http://bbs.tianya.cn/list-worldlook-1.shtml",
        "pattern": r"/post-worldlook-\d+-1\.shtml",
    },
    {
        "title": "心灵热线",
        "baseurl": "http://bbs.tianya.cn/list-spirit-1.shtml",
        "pattern": r"/post-spirit-\d+-1\.shtml",
    },
    {
        "title": "学术中国",
        "baseurl": "http://bbs.tianya.cn/list-666-1.shtml",
        "pattern": r"/post-666-\d+-1\.shtml",
    },
    {
        "title": "人物研究",
        "baseurl": "http://bbs.tianya.cn/list-113-1.shtml",
        "pattern": r"/post-113-\d+-1\.shtml",
    },
    {
        "title": "语文学习",
        "baseurl": "http://bbs.tianya.cn/list-1170-1.shtml",
        "pattern": r"/post-1170-\d+-1\.shtml",
    },
    {
        "title": "文学批评",
        "baseurl": "http://bbs.tianya.cn/list-187-1.shtml",
        "pattern": r"/post-187-\d+-1\.shtml",
    },
    {
        "title": "煮酒论史",
        "baseurl": "http://bbs.tianya.cn/list-no05-1.shtml",
        # http://bbs.tianya.cn/post-no05-507160-1.shtml
        "pattern": r"/post-no05-\d+-1\.shtml"
    },
    {
        "title": "舞文弄墨",
        "baseurl": "http://bbs.tianya.cn/list-culture-1.shtml",
        "pattern": r"/post-culture-\d+-1\.shtml"
    },
    {
        "title": "影视评论",
        "baseurl": "http://bbs.tianya.cn/list-filmtv-1.shtml",
        "pattern": r"/post-filmtv-\d+-1\.shtml"
    },
    {
        "title": "法制天地",
        "baseurl": "http://bbs.tianya.cn/list-law-1.shtml",
        "pattern": r"/post-law-\d+-1\.shtml"
    }
]

def get(url):
    sess = requests.session()
    # to simulite browser
    sess.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
    res = sess.get(url)
    return res



def get_urls(logger, site):
    logger.info("grab {}".format(site["title"]))
    res = get(site["baseurl"])
    ct = res.content.decode(res.apparent_encoding)
    p = re.compile(site["pattern"])
    urls = []
    m = p.search(ct)
    while m:
        url = m.group(0)
        url = "http://bbs.tianya.cn" + url
        urls.append(url)
        ct = ct[m.span()[1]:]
        m = p.search(ct)
    return urls


def get_content(logger, url):
    res = get(url)
    ct = res.content.decode(res.apparent_encoding)
    s = bs(ct, features="html.parser")
    cs = s.find_all("div", attrs={"class": "bbs-content"})
    txt = '\n'.join([c.text for c in cs])
    return txt


def grab(logger):
    db = DB()
    for site in _sites:
        urls = get_urls(logger, site)
        for url in urls:
            if db.has(url):
                continue
            txt = get_content(logger, url)
            db.save(url, txt)
            logger.info("\tgrab {} got {} bytes".format(url, len(txt)))
        