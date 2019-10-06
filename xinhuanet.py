#!/usr/bin/env python3
#coding: utf-8

''' 抓取 www.xinhuanet.com 新闻
'''

# url = "http://www.sd.xinhuanet.com/news/2019-10/03/c_1125069429.htm"
_baseurl = "http://www.xinhuanet.com"

import requests
from bs4 import BeautifulSoup as bs
import re
from db import DB


def get(url):
    sess = requests.session()
    # to simulite browser
    sess.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
    res = sess.get(url)
    return res


_sites = [
    {
        "title": "主页",
        "url": "http://www.xinhuanet.com",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "时政",
        "url": "http://www.xinhuanet.com/politics/",
        # http://www.xinhuanet.com/politics/2019-10/03/c_1125070507.htm
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "地方",
        "url": "http://www.xinhuanet.com/local/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "法制",
        "url": "http://www.xinhuanet.com/legal/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "高层",
        "url": "http://www.xinhuanet.com/politics/leaders/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "人事",
        "url": "http://www.xinhuanet.com/renshi/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "理论",
        "url": "http://www.xinhuanet.com/politics/xhll.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },

    {
        "title": "国际",
        "url": "http://www.xinhuanet.com/world/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    
    {
        "title": "军事",
        "url": "http://www.xinhuanet.com/mil/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    
    {
        "title": "访谈",
        "url": "http://www.xinhuanet.com/video/xhft.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    
    {
        "title": "港澳",
        "url": "http://www.xinhuanet.com/gangao/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    
    {
        "title": "台湾",
        "url": "http://www.xinhuanet.com/tw/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    
    {
        "title": "广播",
        "url": "http://www.xinhuanet.com/video/xinhuaradio/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "财经",
        "url": "http://www.xinhuanet.com/fortune",
        # http://www.xinhuanet.com/fortune/2019-10/05/c_1125072611.htm
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    
    {
        "title": "教育",
        "url": "http://education.news.cn/",
        #http://education.news.cn/2019-09/29/c_1210296480.htm
        "pattern": r"https?://education\.news\.cn/\d+-\d+/\d+/[^\.]+\.html?",
    },
    
    {
        "title": "科技",
        "url": "http://www.xinhuanet.com/tech/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    
    {
        "title": "能源",
        "url": "http://www.xinhuanet.com/energy/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    
    {
        "title": "一带一路",
        "url": "http://www.xinhuanet.com/silkroad/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "文化",
        "url": "http://www.xinhuanet.com/culture/",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "数据",
        "url": "http://www.xinhuanet.com/datanews/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "能源",
        "url": "http://www.xinhuanet.com/energy/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "信息化",
        "url": "http://www.xinhuanet.com/info/index.htm",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "健康",
        "url": "http://www.xinhuanet.com/health",
        "pattern": r"https?://www\.([^\.]+\.)?xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    {
        "title": "体育",
        "url": "http://www.xinhuanet.com/sports",
        # http://sports.xinhuanet.com/c/2019-10/03/c_1125069344.htm
        "pattern": r"https?://sports\.xinhuanet\.com/[^/]+/\d+-\d+/\d+/[^\.]+\.html?",
    },
    
]


def get_main_links(logger, site):
    urls = []
    res = get(site["url"])
    ct = res.content.decode(res.apparent_encoding)
    p = re.compile(site["pattern"])
    m = p.search(ct)
    while m:
        urls.append(m.group(0))
        ct = ct[m.span()[1]:]
        m = p.search(ct)
    return urls


def get_page_content(url):
    res = get(url)
    soup = bs(res.content, features="html.parser")

    div_id_names = [
        "p-detail",
        "contentMain",
    ]

    div_class_names = [
        "container",
        "article",
    ]

    for idname in div_id_names:
        t = soup.find("div", attrs={"id": idname})
        if t:
            ps = t.find_all("p")
            return [p.text for p in ps]

    for clsname in div_class_names:
        t = soup.find("div", attrs={"class": clsname})
        if t:
            ps = t.find_all("p")
            return [p.text for p in ps]
    
    return []


def grab(logger):
    db = DB()
    for site in _sites:
        urls = get_main_links(logger, site)
        logger.info("grab {} urls from {}".format(len(urls), site["title"]))
        for url in urls:
            if db.has(url):
                continue
            txt_list = get_page_content(url)
            txt = ""
            if txt_list:
                txt = "\n".join(txt_list)
            db.save(url, txt)
            logger.info("grab {} got {} bytes".format(url, len(txt)))
