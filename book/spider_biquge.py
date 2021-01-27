
import time
import requests
from concurrent.futures import ThreadPoolExecutor

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
 		for i in range(1,2552):
 			url = base_url + str(i) +".html"
 			self.getBookInfo(url)
 		pass

 	def getBookInfo(self,url):
 		# html = requests.get(url)
 		# html.encoding = 'utf-8'
 		print(url)
 		# if html.status_code == 200:
 		# 	soup = BeautifulSoup(html.text,'lxml')
 		# 	result = soup.find_all(attrs={"id","info"})
 		pass

 	