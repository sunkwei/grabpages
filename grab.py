#!/usr/bin/env python3
#coding: utf-8


''' 抓取指定网站的文章正文

    python3 grab.py sohu
    python3 grab.py 
'''


import os, sys, logging, argparse
import os.path as osp
from urllib.parse import urlparse
import importlib



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ap = argparse.ArgumentParser()
ap.add_argument("site")
args = ap.parse_args()


site = args.site
mod_fname = '.'.join((site, "py"))
if not osp.isfile(mod_fname):
    logging.warning("no grab mod for '{}'".format(site))
else:
    pr = importlib.import_module(site)
    pr.grab(logger)
