
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json

from .config import global_config
from .db.mysql import MYSQL
from .db.redis import REDIS
from .db.mongo import MONGO
from .util import (parse_json)

def timer(func):
	def decor(*args):
		start_time = time.time()
		func(*args)
		end_time = time.time()
		d_time = end_time-start_time
		print("the running time is : ",d_time)
	return decor

executor = ThreadPoolExecutor(max_workers=5)

class SpiderBiquge:
 	"""docstring for ClassName"""
 	def __init__(self):
 		pass

 	def saveBookListsToMysql(self,sql):
 		host = global_config.getRaw('mysql', 'host')
 		port = global_config.getRaw('mysql', 'port')
 		user = global_config.getRaw('mysql', 'user')
 		password = global_config.getRaw('mysql', 'password')
 		database = global_config.getRaw('mysql', 'database')
 		mysql = MYSQL(host,port,user,password, database)
 		mysql.ExecNonQuery(sql)

 	def getRedisConnection(self):
 		host = global_config.getRaw('redis','host')
 		port = global_config.getRaw('redis','port')
 		password = global_config.getRaw('redis','password')
 		redis = REDIS(host,port,password)
 		return redis
 		pass

 	def saveBookUrlToRedis(self,key,value):
 		redis = self.getRedisConnection()
 		redis.setKey(key,value)
 		pass

 	def getMongoConnection(self):
 		host = global_config.getRaw('mongo','host')
 		port = global_config.getRaw('mongo','port')
 		password = global_config.getRaw('mongo','password')
 		user = global_config.getRaw('mongo','user')
 		db = global_config.getRaw('mongo','db')
 		mongo = MONGO(host,int(port),user,password,db)
 		return mongo

 	def saveBookContentToMongo(self,collection,s):
 		mongo = self.getMongoConnection()
 		mongo.save(collection,s)
 		pass

 	@timer
 	def getBiqugeUrl(self):
 		base_url = global_config.getRaw('config', 'url')
 		url_list = []
 		for i in range(1,3):
 			url_list.append(base_url + str(i) +".html")
 			# self.getBookInfo(url)
 		task_pool = threadpool.ThreadPool(5)
 		requests = threadpool.makeRequests(self.getBookInfo,url_list)
 		for req in requests:
 			task_pool.putRequest(req)
 		pass

 	@timer
 	def getBiqugeUrlThreadPoolExecutor(self):
 		base_url = global_config.getRaw('config', 'url')
 		url_list = []
 		for i in range(1,2552):
 			url_list.append(base_url + str(i) +".html")
 		with ThreadPoolExecutor(5) as executor:
 			for each in url_list:
 				executor.submit(self.getBookInfo,each)

 	@timer
 	def getBiqugeUrlThreadPoolExecutorByMap(self):
 		base_url = global_config.getRaw('config', 'url')
 		url_list = []
 		for i in range(1,2552):
 			url_list.append(base_url + str(i) +".html")
 		with ThreadPoolExecutor(5) as executor:
 			executor.map(self.getBookInfo,url_list)			
 	@timer
 	def getBiqugeUrlPool(self):
 		base_url = global_config.getRaw('config','url')
 		for i in range(1,2552):
 			url = base_url+str(i)+".html"
 			self.getBookInfo(url)

 	def getBookTypeId(self,bookType):
 		book_types = {
 		"[玄幻小说]": 0,
			"[仙侠小说]": 1,
			"[都市小说]": 2,
			"[言情小说]": 3,
			"[历史小说]": 4,
			"[网游小说]": 5,
			"[科幻小说]": 6,
			"[恐怖小说]": 7
 		}
 		return book_types.get(bookType,8)
 		pass

 	def getBookInfo(self,url):
 		html = requests.get(url)
 		html.encoding = 'gb18030'
 		if html.status_code == 200:
 			soup = BeautifulSoup(html.text,features='lxml',from_encoding='utf-8')
 			# print(soup.prettify())
 			result = soup.find_all("div",class_="novelslistss")
 			soup_li = BeautifulSoup(str(result),'lxml')
 			bookList = soup_li.find_all("li")
 			book_sql_list = ''
 			book_url_list = []
 			for book in bookList:
 				bookType = self.getBookTypeId(book.contents[0].text)
 				name = book.contents[1].text
 				name_url = book.contents[1].a['href']
 				lastChapter = book.contents[2].text
 				author = book.contents[3].text
 				lastUpdateTime = book.contents[4].text
 				# print(bookType,name,lastChapter,author,lastUpdateTime)
 				book_sql = '("%s","%s","%s",%d),'%(name,author,lastUpdateTime,bookType)
 				book_sql_list += book_sql
 				book_url_list.append(name_url)
 			pre_sql = 'insert into book_info (name,author,update_time,type) values '
 			#strip去掉字符串最后一个指定的字符
 			# print(sql + book_sql_list.strip(','))
 			sql = pre_sql+book_sql_list.strip(',')
 			# self.saveBookListsToMysql(sql)
 			self.saveBookUrlToRedis('book_url_list',book_url_list)
 		pass

 	@timer
 	def getBookUrlFromRedis(self):
 		redis = self.getRedisConnection()
 		book_url_str = redis.getValue('book_url_list')
 		# book_url_list = [v for v in book_url_str]
 		book_url_list = book_url_str.split(',')
 		book_url_lists = []
 		for url in book_url_list:
 			# pass
 			url = self.formatUrl(url)
 			# self.getBookContent(url)
 			book_url_lists.append(url)
 		with ThreadPoolExecutor(5) as executor:
 			executor.map(self.getBookChapter,book_url_lists)
 		pass

 	def formatUrl(self,url):
 		url = url.replace('[','').replace(']','').replace("'","").replace("'","")
 		return url
 		pass

 	def getBookChapter(self,url):
 		html = requests.get(url)
 		html.encoding = 'utf-8'
 		if html.status_code == 200:
 			soup = BeautifulSoup(html.text,'lxml')
 			result = soup.find_all(attrs={'id','info'})
 			text = soup.find('div',id='content')
 			contents = soup.find_all('dd')
 			# title = soup.find_all('dt')
 			# title = contents[-1].text
 			book_chapter_url_str = []
 			href = ''
 			for content in contents:
 				if content.text == '':
 					pass
 				else:
 					href = content.a['href']
 				book_chapter_url_str.append(url+href)
 				# self.getBookContent(href)
 			with ThreadPoolExecutor(5) as executor:
 				executor.map(self.getBookContent,book_chapter_url_str)
 		else:
 			print('error')
 		pass

 	def getBookContent(self,url):
 		html = requests.get(url)
 		html.encoding = 'gb18030'
 		if html.status_code == 200:
 			soup = BeautifulSoup(html.text,'lxml')
 			result = soup.find_all(attrs={'id','info'})
 			content = soup.find('div',id='content').text
 			chapter = soup.find('div',attrs={'class':'bookname'}).h1.text
 			title_str = soup.find('div',attrs={'class':'con_top'}).text
 			collection = title_str.split('>')[1]
 			s = '{"chapter":"%s","content":"%s"}'%(chapter,content)
 			self.saveBookContentToMongo(collection,json.loads(s))
 		else:
 			print('error')
