#!/usr/bin/env python3
#coding: utf-8


from grab_stack import get_matched_link, get_page_content
from db import DB
import os
import os.path as osp


# 从 data/key_words.txt 中加载
keywords_fname = "data/key_words.txt"
_key_words = [
]

for name in os.listdir("data"):
    fname = osp.join("data", name)
    if osp.isfile(fname):
        with open(fname) as f:
            data = f.read()
            _key_words.extend(data.split())

print("ennn, there are {} key_words".format(len(_key_words)))

_sites = [
    "http://baike.baidu.com/wenhua",
    "http://baike.baidu.com/ziran",
    "http://baike.baidu.com/dili",
    "http://baike.baidu.com/lishi",
    "http://baike.baidu.com/shenghuo",
    "http://baike.baidu.com/shehui",
    "http://baike.baidu.com/yishu",
    "http://baike.baidu.com/renwu",
    "http://baike.baidu.com/jingji",
    "http://baike.baidu.com/keji",
    "http://baike.baidu.com/tiyu",
]


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
    ("div", None),
    ("div", {
        "class": ["news-list"]
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


def grab_site(logger, baseurl):
    logger.info("to grab {}".format(baseurl))
    urls = get_matched_link(logger, _renwu, baseurl, my_get_urls)
    db = DB()
    for url in urls:
        if db.has(url):
            continue
        txt = ""
        cs = get_page_content(logger, _content_pattern, url, my_get_content)
        for c in cs:
            txt += c
        if txt:
            db.save(url, txt)
        logger.info("{} saved {} bytes".format(url, len(txt)))


def grab(logger):
    for baseurl in _sites:
        grab_site(logger, baseurl)


def grab_search(logger, word):
    import requests
    url = "http://baike.baidu.com/search/word?word={}".format(word)
    sess = requests.session()
    sess.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
    while 1:
        res = sess.get(url)
        if res.status_code == 200:
            break
        elif res.status_code == 302:
            url = res.headers["Location"]
            if url[:2] == "//":
                url = "http:" + url
            elif url[0] == '/':
                url = "http://baike.baidu.com" + url
            logger.info("GET redir url: {}".format(url))
        else:
            logger.error("GET {} err, status ={}".format(url, res.status_code))
            return

    db = DB()
    if db.has(url):
        logger.info("word: {} exists".format(word))
        return

    logger.info("using item url: {}".format(url))    
    txt = ""
    cs = get_page_content(logger, _content_pattern, url, my_get_content)
    for c in cs:
        txt += c

    db.save(url, txt)
    logger.info("{} saved {} bytes".format(url, len(txt)))



def grab_key_words(logger):
    for word in _key_words:
        grab_search(logger, word)



if __name__ == "__main__":
    import logging
    import argparse

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    ap = argparse.ArgumentParser()
    ap.add_argument("word")
    args = ap.parse_args()

    if args.word == "all":
        grab_key_words(logger)
    else:
        grab_search(logger, args.word)
