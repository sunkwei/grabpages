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
_novel_main = [
    ("div", {
        "id": "list"
    }),
    ("dl", None),
]

# 文章模式
_art_pattern = [
    ("div", {
        "id": "content"
    }),
    ("p", None),
]


def my_get_urls(tag):
    return [tag["href"]]


def my_get_urls2(tag):
    aa = tag.find_all("a")
    return [a["href"] for a in aa]


def my_get_cont(tag):
    return tag.text


def grab(logger):
    baseurl = "http://www.deyuxs.net"
    db = DB("deyuxs.db")
    n_urls = get_matched_link(logger, _deyuxs_net_all, baseurl + "/all", my_get_urls, max_url_count=3)
    for n_url in n_urls:
        n_url = baseurl + n_url
        a_urls = get_matched_link(logger, _novel_main, n_url, my_get_urls2)
        for a_url in a_urls:
            a_url = baseurl + a_url
            txt = ""
            cs = get_page_content(logger, _art_pattern, a_url, my_get_cont)
            for c in cs:
                txt += c

            if txt:
                db.save(a_url, txt)
            logger.info("{} saved, {} bytes".format(a_url, len(txt)))
            