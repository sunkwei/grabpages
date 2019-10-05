#!/usr/bin/python3
#coding: utf-8


# 从 news.db 中提取句子，保存到指定的文件名中，每行为一句话

import os, sys, logging, argparse
import os.path as osp
import sqlite3 as sq


curr_path = osp.dirname(osp.abspath(__file__))
txt_fname = osp.join(curr_path, "output.txt")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("extract sentences")

ap = argparse.ArgumentParser()
ap.add_argument("dbname")
ap.add_argument("--output", default=txt_fname, help="the text file name for saving sentences")
ap.add_argument("--num", default=sys.maxsize, type=int)
args = ap.parse_args()

db = sq.connect(args.dbname)

cur = db.cursor()
cmd = "select count(*) from tnews"
cur.execute(cmd)
r = cur.fetchone()
cur.close()

logger.info("there are {} articles".format(r[0]))

cur = db.cursor()
cmd = "select * from tnews"
cur.execute(cmd)

r = cur.fetchone()
n = 0
f = open("out_{}.txt".format(n), "w")
while r:
    txt = r[2]
    f.write(txt)
    n += 1
    r = cur.fetchone()
    if n % args.num == 0:
        f.close()
        f = open("out_{}.txt".format(n), "w")

f.close()
cur.close()
db.close()
