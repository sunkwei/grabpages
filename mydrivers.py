#!/usr/bin/env python3
#coding: utf-8


from grab_stack import get_matched_link, get_page_content
from db import DB

_www_mydrivers_com = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["main"],
    }),
    ("div", {
        "class": ["main_left"],
    }),
    ("div", None),
    ("div", {
        "class": ["news_info1"],
    }),
    ("ul", {
        "class": ["newslist"],
    }),
    ("li", None),
    ("span", {
        "class": ["titl"],
    }),
]


def my_get_links(tag):
    aa = tag.find_all("a")
    return [a["href"] for a in aa]


_content_pattern1 = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["news_box"],
    }),
    ("div", {
        "class": ["news_left"],
    }),
    ("div", {
        "class": ["news_n"],
    }),
    ("div", {
        "class": ["news_info"],
    }),
]


_content_pattern2 = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["pc_box"],
    }),
    ("div", {
        "class": ["pc_info"],
    })
]


def my_get_content(tag):
    return tag.text


def grab(logger):
    db = DB()
    urls = get_matched_link(logger, _www_mydrivers_com, "http://www.mydrivers.com", my_get_links)
    for url in urls:
        if db.has(url):
            continue

        txt = ""
        cs = get_page_content(logger, _content_pattern1, url, my_get_content, True)
        if not cs:
            cs = get_page_content(logger, _content_pattern2, url, my_get_content, True)
        if not cs:
            logger.warning("{} no content".format(url))
            continue

        for c in cs:
            txt += c
        db.save(url, txt)
        logger.info("{} saved, {} bytes".format(url, len(txt)))