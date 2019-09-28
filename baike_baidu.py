#!/usr/bin/env python3
#coding: utf-8


from grab_stack import get_matched_link, get_page_content
from db import DB


_renwu = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["grid"]
    }),
    ("div", {
        "class": ["g-row", "container"]
    }),
    ("div", {
        "class": ["g69"],
    }),
    ("div", {
        "class": ["g-row", "field-common"]
    }),
    ("div", {
        "class": ["field"]
    }),
    ("div", {
        "class": ["new-list"]
    }),
    ("ul", {
        "class": ["nslog:6522"]
    }),
    ("li", None)
]


def my_get_urls(tag):
    links = tag.find_all("a")
    urls = []
    for link in links:
        if link["href"] not in urls:
            urls.append(link["href"])
    return urls


_content_pattern = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["body-wrapper"]
    }),
    ("div", {
        "class": ["content-wrapper"]
    }),
    ("div", {
        "class": ["content"]
    }),
    ("div", {
        "class": ["main-content"]
    }),
    ("div", {
        "class": ["para"]
    })
]


def my_get_content(tag):
    return tag.text


def grab(logger):
    urls = get_matched_link(logger, _renwu, "http://baike.baidu.com/renwu", my_get_urls, True)
    db = DB()
    for url in urls:
        if db.has(url):
            continue
        txt = ""
        cs = get_page_content(logger, _content_pattern, url, my_get_content, True)
        for c in cs:
            txt += c
        if txt:
            db.save(url, txt)