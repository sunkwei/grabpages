#!/usr/bin/env python3
#coding: utf-8


''' 使用 sqlite3 存储抓取的文章内容：
        1. _hashid: url 的md5，用于索引
        2. _url: 文章的完整路径
        3. _txt: 文章内容


    使用流程：
        if not db.has(url):
            txt = grab(url)
            db.save(url, txt)
'''

import os, sys, logging, argparse
import os.path as osp
import sqlite3 as sq
import hashlib



curr_path = osp.dirname(osp.abspath(__file__))
db_fname = osp.join(curr_path, "news.db")


class DB:
    def __init__(self, fname=db_fname):
        self.fname_ = fname
        self.db_ = sq.connect(self.fname_)
        cmd = "create table if not exists tnews (_hashid char(36) primary key, _url text, _txt text)"
        self.db_.execute(cmd)
        self.db_.commit()


    def __del__(self):
        self.db_.close()


    def md5(self, url):
        m = hashlib.md5()
        m.update(url.encode("utf-8"))
        return m.hexdigest()


    def has(self, url):
        hashid = self.md5(url)
        cmd = "select count(_hashid) from tnews where _hashid=?"
        cur = self.db_.cursor()
        cur.execute(cmd, (hashid,))
        r = cur.fetchone()
        cur.close()
        return r[0] > 0


    def save(self, url, txt):
        if not self.has(url):
            hashid = self.md5(url)
            cmd = "insert into tnews values(?,?,?)"
            cur = self.db_.cursor()
            cur.execute(cmd, (hashid, url, txt))
            cur.close()
            self.db_.commit()
            return 0
        else:
            return 1
