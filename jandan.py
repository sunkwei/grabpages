#!/usr/bin/env python3
#coding: utf-8

from grab_stack import get_matched_link, get_page_content
from db import DB


_jandan_net = [
    ("html", None),
    ("body", None),
    ("div", {
        "id": "wrapper"
    }),
    ("div", {
        "id": "body"
    }),
    ("div", {
        "id": "content",
    }),
    ("div", {
        "class": ["post"],
    }),
    ("div", {
        "class": ["indexs"],
    }),
    ("h2", None),
]


def my_get_urls(tag):
    # tag 为 <h2><a href="..." ...></h2>
    aa = tag.find_all("a")
    return [a["href"] for a in aa]


_content_pattern = [
    ("html", None),
    ("body", None),
    ("div", {
        "id": "wrapper"
    }),
    ("div", {
        "id": "body",
    }),
    ("div", {
        "id": "content",
    }),
    ("div", {
        "class": ["post", "f"],
    }),
    ("p", None)
]


def my_get_content(tag):
    return tag.text


def grab(logger):
    db = DB()
    urls = get_matched_link(logger, _jandan_net, "http://jandan.net", my_get_urls)
    for url in urls:
        if db.has(url):
            continue
        content = ""
        cs = get_page_content(logger, _content_pattern, url, my_get_content)
        for c in cs:
            if isinstance(c, str):
                content += c
        if content:
            db.save(url, content)
        logger.info("{} saved, {} bytes".format(url, len(content)))