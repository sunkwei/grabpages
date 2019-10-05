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

# 指定多个分站点
_sites = [
    {
        "baseurl": "http://www.people.com.cn",
        # "encoding": "gb2312",
        "pattern": r"https?://[^/\.]+\.people(\.com)?\.cn/n[0-9]+/[0-9]+/[0-9]+/[^\./]+\.html",
    },
    {
        "baseurl": "http://politics.people.com.cn",
        # "encoding": "utf-8",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://world.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://finance.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://tw.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://military.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://opinion.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://leaders.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://renshi.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://theory.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://legal.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://society.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://industry.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://edu.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://kpzg.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://sports.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://culture.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://art.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://health.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
    {
        "baseurl": "http://scitech.people.com.cn",
        "pattern": r"/n\d/\d+/\d+/[^\./]+\.html",
    },
]

def get_article_urls(db, cfg):
    base_url = cfg["baseurl"]
    res = requests.get(base_url)
    enc = cfg["encoding"] if "encoding" in cfg else res.apparent_encoding
    try:
        page_cont = res.content.decode(enc)
    except:
        try:
            page_cont = res.content.decode("utf-8")
        except:
            print("cannot decode page ... for {}".format(base_url))
            return []

    p = re.compile(cfg["pattern"])
    rc = page_cont
    urls = []
    m = p.search(rc)
    while m:
        url = m.group(0)
        if url[0] == '/':
            url = base_url + url
        elif url[:2] == "//":
            url = "http:" + url
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
        "box_text",
        "artDet",
        "content"
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
    for site in _sites:
        urls = get_article_urls(db, site)
        logger.info("there are {} new articles in {}".format(len(urls), site["baseurl"]))
        for url in urls:
            if db.has(url):
                continue
            
            txt = ""
            soup = None
            try:
                res = requests.get(url)
                ct = res.content.decode(site["encoding"] if "encoding" in site else res.apparent_encoding, errors="replace")
                soup = bs(ct, "html.parser")
            except Exception as e:
                logger.error("excp parse {}, {}".format(url, e))
                continue

            cs = my_get_cont(soup)
            for c in cs:
                txt += c
            db.save(url, txt)
            logger.info("{} saving {} bytes".format(url, len(txt)))