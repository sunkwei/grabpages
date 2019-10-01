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

with open(args.output, "w") as f:
    r = cur.fetchone()
    n = 0
    while r:
        txt = r[2]
        
        # TODO: 这里断句，并保存到 f
        f.write(txt)
        n += 1
        if n >= 1000:
            break
        r = cur.fetchone()

cur.close()
db.close()
