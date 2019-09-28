#!/usr/bin/env python3
#coding: utf-8

''' 抓取机器之心第一层链接的内容
'''


__all__ = ["grab"]


_www_jiqizhixin_com = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["home", "u-has-header"],
    }),
    ("div", {
        "class": ["u-container"],
    }),
    ("div", {
        "class": ["u-clearfix"],
    }),
    ("div", {
        "class": ["js-article-container"],
    }),
    ("div", {
        "class": ["u-block__body"],
    }),
    ("div", {
        "class": ["u-block__item"],
    }),
    ("article", {
        "class": ["article-item__container"],
    }),
    ("main", {
        "class": ["article-item__right"],
    }),
    ("section", None),
]


# /html/body/div{article}/div{u-min-height-container,u-container}/div{u-col-8,article__inline}/div{article__content}
# /html/body/div{article}/div{u-min-height-container,u-container}/div{u-col-8,article__inline}/div{article__content}
_content_pattern = [
    ("html", None),
    ("body", None),
    ("div", {
        "class": ["article"],
    }),
    ("div", {
        "class": ["u-container"],
    }),
    ("div", {
        "class": ["u-col-8"],
    }),
    ("div", {
        "class": ["article__content"],
    }),
]


from db import DB
import bs4
from bs4 import BeautifulSoup as bs
import requests
from grab_stack import GrabStack, get_matched_link, get_page_content


_db = DB()


def my_get_urls(tag):
    urls = []
    links = tag.find_all("a")
    for link in links:
        url = link["href"]
        urls.append(url)
    return urls


def my_get_content(tag):
    ''' 机器之心内容是 <h1> ...</h1> <p> .. 这些组成，可以简单的删除所有 <...>
    '''
    def remove_html_markup(s):
        tag = False
        quote = False
        out = ""

        for c in s:
                if c == '<' and not quote:
                    tag = True
                elif c == '>' and not quote:
                    tag = False
                elif (c == '"' or c == "'") and tag:
                    quote = not quote
                elif not tag:
                    out = out + c

        return out
    
    return tag.text


def grab(logger):
    urls = get_matched_link(logger, _www_jiqizhixin_com, "https://www.jiqizhixin.com", my_get_urls)
    logger.info("there are {} pages to grab".format(len(urls)))
    for url in urls:
        if url[0] == "/":
            url = "https://www.jiqizhixin.com" + url

            if _db.has(url):
                continue
            
            content = get_page_content(logger, _content_pattern, url, my_get_content)
            cs = ""
            for c in content:
                if isinstance(c, str):
                    cs += c
            if not cs:
                logger.warning("page: {} no data??".format(url))
                continue
            _db.save(url, cs)
            logger.info("page: {} saved {} chars".format(url, len(cs)))
