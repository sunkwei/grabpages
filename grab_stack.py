#!/usr/bin/env python3
#coding: utf-8


import bs4
import requests
from bs4 import BeautifulSoup as bs


class GrabStack:
    def __init__(self):
        self.stack_ = []


    def push(self, name, obj):
        self.stack_.append((name, obj))


    def pop(self):
        assert(len(self.stack_) > 0)
        del self.stack_[-1]


    def top(self):
        assert(len(self.stack_) > 0)
        return self.stack_[-1]


    def get_path(self, moreinfo=0):
        path = ""
        for o in self.stack_:
            path += "/"
            path += o[0]
            if moreinfo:
                if isinstance(o[1], bs4.element.Tag):
                    tag = o[1]
                    if tag.name == "div" and "class" in tag.attrs and tag["class"]:
                        path += '{' + "{}".format(','.join(tag["class"])) + '}'
        return path


    def is_match_path(self, matchpath=[]):
        # 判断当前堆栈是否符合要求 ...
        if (len(self.stack_) != len(matchpath)) or not self.stack_:
            return False

        for i in range(len(self.stack_)):
            if (matchpath[i][0] != self.stack_[i][0]):
                return False

            m = matchpath[i][1]
            if m is None:   # 匹配所有
                continue

            tag = self.stack_[i][1]

            for k,v in m.items():
                if k not in tag.attrs:
                    return False
                if v is None:
                    # 要求 tag 中不能有 k
                    if k in tag.attrs:
                        return False

                if isinstance(v, list):
                    # 此时要求 tag[k] 为 list，并且 tag[k] 包含 v
                    if k not in tag.attrs:
                        return False

                    if isinstance(tag.attrs[k], list):
                        for vv in v:
                            if vv not in tag[k]:
                                return False
                    elif isinstance(tag.attrs[k], str):
                        if isinstance(v, str):
                            if tag.attrs[k] != v:
                                return False

        return True



def get_matched_link(logger, pattern, baseurl, fc_get_urls):
    logger.info("begin grab size: {}".format(baseurl))
    res = requests.get(baseurl)
    urls = []
    soup = bs(res.content, features="lxml")
    for o in soup:
        if isinstance(o, bs4.element.Tag):
            stack = GrabStack()
            def parse_tag(tag):
                stack.push(tag.name, tag)
                if stack.is_match_path(pattern):
                    for u in fc_get_urls(tag):
                        urls.append(u)
                for o in tag:
                    if isinstance(o, bs4.element.Tag):
                        parse_tag(o)
                stack.pop()
            parse_tag(o)
    return urls


def get_page_content(logger, pattern, url, fc_get_content):
    logger.info("to get url: {}".format(url))
    res = requests.get(url)
    content = []
    soup = bs(res.content, features="lxml")
    for o in soup:
        if isinstance(o, bs4.element.Tag):
            stack = GrabStack()
            def parse_content(tag):
                stack.push(tag.name, tag)
                if stack.is_match_path(pattern):
                    content.append(fc_get_content(tag))
                for o in tag:
                    if isinstance(o, bs4.element.Tag):
                        parse_content(o)
                stack.pop()
            parse_content(o)
    return content