#!/usr/bin/python3
#coding: utf-8


from xinhuanet import get
from db import DB
from bs4 import BeautifulSoup as bs
import re


def get_urls(logger):
    res = get("http://www.qdaily.com/")
    ct = res.content.decode("utf-8")
    # /articles/64618.html
    p = re.compile(r"/articles/\d+\.html")
    urls = []
    m = p.search(ct)
    while m:
        url = m.group(0)
        url = "http://www.qdaily.com" + url
        urls.append(url)
        ct = ct[m.span()[1]:]
        m = p.search(ct)
    return urls


def get_content(logger, url):
    res = get(url)
    ct = res.content.decode("utf-8")
    s = bs(ct, features="html.parser")
    detail = s.find("div", attrs={"class": "detail"})
    if detail:
        ps = detail.find_all("p")
        ts = [p.text for p in ps]
        return '\n'.join(ts)
    else:
        logger.warning("cannot get class='detail' for {}".format(url))
        return ""


def grab(logger):
    db = DB()
    urls = get_urls(logger)
    for url in urls:
        if db.has(url):
            continue

        txt = get_content(logger, url)
        logger.info("grab {} got {} bytes".format(url, len(txt)))
        db.save(url, txt)