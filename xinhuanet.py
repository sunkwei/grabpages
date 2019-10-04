#!/usr/bin/env python3
#coding: utf-8

''' 抓取 www.xinhuanet.com 新闻
'''

# url = "http://www.sd.xinhuanet.com/news/2019-10/03/c_1125069429.htm"
_baseurl = "http://www.xinhuanet.com"

import requests
from bs4 import BeautifulSoup as bs
import re
from db import DB


def get(url):
    sess = requests.session()
    # to simulite browser
    sess.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
    res = sess.get(url)
    return res

def get_main_links(url):
    urls = []
    res = get(url)
    ct = res.content.decode(res.apparent_encoding)
    p = re.compile(r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?")
    m = p.search(ct)
    while m:
        urls.append(m.group(0))
        ct = ct[m.span()[1]:]
        m = p.search(ct)
    return urls


def get_page_content(url):
    res = get(url)
    soup = bs(res.content, "html")

    div_id_names = [
        "p-detail",
        "contentMain",
    ]

    div_class_names = [
        "container",
        "article",
    ]

    for idname in div_id_names:
        t = soup.find("div", attrs={"id": idname})
        if t:
            ps = t.find_all("p")
            return [p.text for p in ps]

    for clsname in div_class_names:
        t = soup.find("div", attrs={"class": clsname})
        if t:
            ps = t.find_all("p")
            return [p.text for p in ps]
    
    return []


def grab(logger):
    db = DB()
    urls = get_main_links(_baseurl)
    for url in urls:
        if db.has(url):
            continue
        txt_list = get_page_content(url)
        txt = ""
        if txt_list:
            txt = "\n".join(txt_list)
        db.save(url, txt)
        logger.info("grab {} got {} bytes".format(url, len(txt)))
