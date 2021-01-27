
import time
import requests
import threadpool
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

from .config import global_config
from .db.mysql import MYSQL

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

 	def saveBookListsToMysql(self):
 		sql = "select version()"
 		host = global_config.getRaw('mysql', 'host')
 		port = global_config.getRaw('mysql', 'port')
 		user = global_config.getRaw('mysql', 'user')
 		password = global_config.getRaw('mysql', 'password')
 		database = global_config.getRaw('mysql', 'database')
 		mysql = MYSQL(host,port,user,password, database)
 		print(mysql.ExecQuery(sql))

 	@timer
 	def getBiqugeUrl(self):
 		base_url = global_config.getRaw('config', 'url')
 		url_list = []
 		for i in range(1,2552):
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
 		for i in range(1,2):
 			url_list.append(base_url + str(i) +".html")
 		with ThreadPoolExecutor(5) as executor:
 			executor.map(self.getBookInfo,url_list)			
 	@timer
 	def getBiqugeUrlPool(self):
 		base_url = global_config.getRaw('config','url')
 		for i in range(1,2552):
 			url = base_url+str(i)+".html"
 			self.getBookInfo(url)

 	def getBookInfo(self,url):
 		html = requests.get(url)
 		html.encoding = 'utf-8'
 		if html.status_code == 200:
 			soup = BeautifulSoup(html.text,features='lxml',from_encoding='utf-8')
 			bookList = soup.find_all("li")
 			# print(soup.original_encoding)
 			# print(soup.prettify())
 			print(soup.span.encode('utf-8'))
 			# result = soup.find_all("div",class_="novelslistss")
 			for book in bookList:
 				soup_book = BeautifulSoup(str(book),'lxml')
 				bootType = soup_book.find('span',class_='s1',from_encoding='utf-8')
 				name = soup_book.find('span',class_='s2',from_encoding='utf-8')
 				lastCapter = soup_book.find('span',class_='s3',from_encoding='utf-8')
 				author = soup_book.find('span',class_='s4',from_encoding='utf-8')
 				lastUpdateTime = soup_book.find('span',class_='s5',from_encoding='utf-8')
 				# print(bookInfo)
 		pass

 	