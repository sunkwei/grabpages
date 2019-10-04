#!/usr/bin/env python3
#coding: utf-8

from db import DB
import re
import requests
from bs4 import BeautifulSoup as bs


''' 抓取 http://www.people.com.cn 网站新闻内容

        <a href="http://opinion.people.com.cn/n1/2019/0930/c1003-31380640.html" target="_blank">爱国是中国青年最亮丽的青春底色</a>

        1. 首页抓取 "$https?://[^\.]+\.people\.com\.cn/n1/[0-9]+/[0-9]+/[^\.]\.html$"
        2. 
'''

def get_article_urls(db):
    main_url = "http://www.people.com.cn"
    res = requests.get(main_url)
    enc = res.apparent_encoding
    page_cont = res.content.decode(enc)
    p = re.compile(r"https?://[^/\.]+\.people(\.com)?\.cn/n[0-9]+/[0-9]+/[0-9]+/[^\./]+\.html")
    rc = page_cont
    urls = []
    m = p.search(rc)
    while m:
        url = m.group(0)
        if not db.has(url):
            urls.append(url)
        e = m.span()[1]
        rc = rc[e:]
        m = p.search(rc)
    return urls



def my_get_cont(soup):
    ''' TODO: 抓取不同格式的页面内容 

            <div class="text_c">
             ...
            <div class="show_text">
              抓这里的内容
            </div>
            </div>
    '''
    div_id_names = [
        "rwb_zw",
    ]
    div_class_names = [
        "show_text",
        "box_con",
        "text_wz",
        "gray,box_text",
        "artDet",
        "content,clear,clearfix"
    ]

    for id_ in div_id_names:
        c = soup.find("div", attrs={"id": id_})
        if c:
            ps = c.find_all("p")
            return [p.text for p in ps]

    for class_ in div_class_names:
        c = soup.find("div", attrs={"class": class_})
        if c:
            ps = c.find_all("p")
            return [p.text for p in ps]

    return []



def grab(logger):
    db = DB()
    urls = get_article_urls(db)
    logger.info("there are {} new articles".format(len(urls)))
    for url in urls:
        if db.has(url):
            continue
        
        txt = ""
        soup = None
        try:
            res = requests.get(url)
            soup = bs(res.content, "html")
        except Exception as e:
            logger.error("excp parse {}, {}".format(url, e))
            continue

        cs = my_get_cont(soup)
        for c in cs:
            txt += c
        db.save(url, txt)
        logger.info("{} saving {} bytes".format(url, len(txt)))