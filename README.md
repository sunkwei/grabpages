# 抓取文章内容
这个项目希望抓取网站的文章，使用 requests + bs4。主要提供两个函数：

 * get_matched_link(logger, pattern, url, cb_get_urls): 从指定页面(url)，根据模式(pattern)匹配找到对应的 html tags，然后调用 cb_get_urls(tag) 个到url;
 * get_page_content(logger, pattern, url, cb_get_content): 从url指定的页面中，提取匹配的正文，本质与 get_matched_link() 一样 :)



## 使用百度百科搜索
本项目通过百度百科搜索关键词，并保存关键词正文。data/ 目录中为需要搜索的关键词文件，每个关键词为一行，然后调用

	GET baike.baidu.com/search/word?word=<kw>

项目内置了成语的关键词文件。提取所有关键词

	python3 baike_baidu.py all 

提取指定关键词

	python3 baike_baidu.py 勾股定理

## 正文的存储
使用 sqlite3 存储，数据结构：

 * hashid: md5(url) 用于防止重复获取
 * url: url
 * txt: 正文内容

