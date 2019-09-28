#!/usr/bin/env python3
#coding: utf-8

''' 抓取 www.cnbeta.com
'''

from grab_stack import get_matched_link, get_page_content
from db import DB


_www_cnbeta_com = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["main-wrap"],
    }),
    ("div", {
        "class": ["cnbeta-update"],
    }),
    ("div", {
        "class": ["w1200"],
    }),
    ("div", {
        "class": ["cnbeta-update-list"],
    }),
    ("div", {
        "class": ["items-area"],
    }),
    ("div", {
        "class": ["item"],
    }),
    ("dl", None),
    ("dt", None),
]


_content_pattern = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["main-wrap"],
    }),
    ("div", {
        "class": ["cnbeta-article-wrapper"],
    }),
    ("div", {
        "class": ["cnbeta-update"],
    }),
    ("div", {
        "class": ["w1200"],
    }),
    ("div", {
        "class": ["cnbeta-article"],
    }),
    ("div", {
        "class": ["cnbeta-article-body"],
    }),
    ("div", {
        "class": ["article-content"],
    }),
]


def my_get_urls(tag):
    aa = tag.find_all("a")
    return [ a["href"] for a in aa ]


def my_get_content(tag):
    return tag.text


def grab(logger):
    db = DB()
    urls = get_matched_link(logger, _www_cnbeta_com, "https://www.cnbeta.com", my_get_urls, show_path=False)
    for url in urls:
        if url[:2] == "//":
            url = "https:" + url

        if db.has(url):
            continue

        contents = get_page_content(logger, _content_pattern, url, my_get_content)
        cs = ""
        for c in contents:
            if isinstance(c, str):
                cs += c
            db.save(url, cs)