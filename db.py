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
import re



curr_path = osp.dirname(osp.abspath(__file__))
db_fname = osp.join(curr_path, "news.db")


class DB:
    def __init__(self, fname=None):
        self.db0_ = sq.connect("allurls.db")

        if not fname:
            import time
            lm = time.localtime(time.time())
            fname = "news_{:04d}-{:02d}-{:02d}.db".format(lm[0], lm[1], lm[2])

        self.fname_ = fname
        self.db_ = sq.connect(self.fname_)
        cmd = "create table if not exists tnews (_hashid char(36) primary key, _url text, _txt text)"
        self.db_.execute(cmd)
        self.db_.execute("create unique index if not exists inews on tnews (_hashid)")
        self.db_.commit()

        # 存储百科关键词索引，方便快速检查是否已经下载
        cmd = "select name from sqlite_master where type='table'"
        cur = self.db_.execute(cmd)
        rs = cur.fetchall()
        found = False
        for r in rs:
            if r[0] == "tkeywords":
                found = True
                break

        if not found:
            cmd = "create table tkeywords (_hashid char(36) primary key)"
            self.db_.execute(cmd)
            cur = self.db_.execute("select _url from tnews")
            p = re.compile(r"word\?word=(.+)$")
            f = cur.fetchone()
            while f:
                url = f[0]
                r = p.search(url)
                if r:
                    kw = r.group(1)
                    h = self.md5(kw)
                    self.db_.execute("insert into tkeywords values (?)", (h,))
                f = cur.fetchone()
            self.db_.commit()


    def __del__(self):
        self.db_.close()


    def has0(self, url_hash):
        cur = self.db0_.cursor()
        cur.execute("select _hashid from turl_hash where _hashid=?", (url_hash,))
        r = cur.fetchone()
        return r is not None


    def md5(self, url):
        m = hashlib.md5()
        m.update(url.encode("utf-8"))
        return m.hexdigest()


    def has(self, url):
        hashid = self.md5(url)
        if self.has0(hashid):
            return True
        cmd = "select count(_hashid) from tnews where _hashid=?"
        cur = self.db_.cursor()
        cur.execute(cmd, (hashid,))
        r = cur.fetchone()
        cur.close()
        return r[0] > 0


    def has_keyword(self, word):
        # 搜索 tkeyword，word 是否存在
        hashid = self.md5(word)
        cur = self.db_.cursor()
        cur.execute("select count(*) from tkeywords where _hashid=?", (hashid,))
        r = cur.fetchone()
        cur.close()
        return r[0] == 1


    def save(self, url, txt):
        if not self.has(url):
            hashid = self.md5(url)
            cmd = "insert into tnews values(?,?,?)"
            cur = self.db_.cursor()
            cur.execute(cmd, (hashid, url, txt))
            cur.close()

            self.db0_.execute("insert into turl_hash values(?)", (hashid,))
            self.db0_.commit()

            # 检查是否时百度百科的搜索 ...
            p = re.compile(r"word\?word=(.+)$")
            m = p.search(url)
            if m:
                word = m.group(1)
                h = self.md5(word)
                self.db_.execute("insert into tkeywords values (?)", (h,))

            self.db_.commit()
            return 0
        else:
            return 1




if __name__ == "__main__":
    db0 = sq.connect("allurls.db")
    db0.execute("create table if not exists turl_hash (_hashid char(36) primary key)")

    def get_ids(fname):
        ids = []
        db = sq.connect(sys.argv[1])
        cur = db.cursor()
        cur.execute("select _hashid from tnews")
        r = cur.fetchone()
        while r:
            ids.append(r[0])
            r = cur.fetchone()
        cur.close()
        db.close()
        return ids

    ids = get_ids(sys.argv[1])

    print("got {} urls".format(len(ids)))
    for idx in ids:
        db0.execute("insert or replace into turl_hash values (?)", (idx,))

    db0.commit()
    db0.close()