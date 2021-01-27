笔趣阁小说爬取
===============

https://www.52bqg.net/top/allvote/

通过对笔趣阁中排行榜单——总排行榜的小说进行爬取

小说基本信息存入mysql中
将小说的url存入redis
通过分布式读取redis中的数据，将文本内容插入到mongo中