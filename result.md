# MySQL SQL注入测试报告
生成时间: 2025-06-24 01:14:28

## 📊 总体统计
- **总操作数**: 13
- **总请求数**: 770
- **总耗时**: 4.25秒
- **平均耗时**: 0.006秒/请求

## 📋 详细操作记录
### 1. 列枚举 (testdb.user)
- **时间**: 2025-06-24 01:14:25
- **请求数**: 167
- **耗时**: 1.03秒
- **结果**:
```
['id', 'password', 'username']
```

### 2. 列枚举 (testdb.user)
- **时间**: 2025-06-24 01:14:26
- **请求数**: 167
- **耗时**: 1.03秒
- **结果**:
```
['id', 'password', 'username']
```

### 3. 数据提取 (testdb.user.id)
- **时间**: 2025-06-24 01:14:26
- **请求数**: 20
- **耗时**: 0.10秒
- **结果**:
  4

### 4. 数据提取 (testdb.user.password)
- **时间**: 2025-06-24 01:14:26
- **请求数**: 64
- **耗时**: 0.37秒
- **结果**:
  admin123

### 5. 数据提取 (testdb.user.username)
- **时间**: 2025-06-24 01:14:27
- **请求数**: 45
- **耗时**: 0.23秒
- **结果**:
  admin

### 6. 数据提取 (testdb.user.id)
- **时间**: 2025-06-24 01:14:27
- **请求数**: 20
- **耗时**: 0.10秒
- **结果**:
  5

### 7. 数据提取 (testdb.user.password)
- **时间**: 2025-06-24 01:14:27
- **请求数**: 71
- **耗时**: 0.35秒
- **结果**:
  password1

### 8. 数据提取 (testdb.user.username)
- **时间**: 2025-06-24 01:14:27
- **请求数**: 46
- **耗时**: 0.22秒
- **结果**:
  alice

### 9. 数据提取 (testdb.user.id)
- **时间**: 2025-06-24 01:14:28
- **请求数**: 21
- **耗时**: 0.11秒
- **结果**:
  6

### 10. 数据提取 (testdb.user.password)
- **时间**: 2025-06-24 01:14:28
- **请求数**: 53
- **耗时**: 0.27秒
- **结果**:
  qwerty

### 11. 数据提取 (testdb.user.username)
- **时间**: 2025-06-24 01:14:28
- **请求数**: 32
- **耗时**: 0.14秒
- **结果**:
  bob

### 12. 全表数据提取 (testdb.user)
- **时间**: 2025-06-24 01:14:28
- **请求数**: 32
- **耗时**: 0.14秒
- **结果**:
```
{'id': '4', 'password': 'admin123', 'username': 'admin'}
{'id': '5', 'password': 'password1', 'username': 'alice'}
{'id': '6', 'password': 'qwerty', 'username': 'bob'}
```

### 13. 快速扫描 (testdb.user)
- **时间**: 2025-06-24 01:14:28
- **请求数**: 32
- **耗时**: 0.14秒
- **结果**:
```
{'id': '4', 'password': 'admin123', 'username': 'admin'}
{'id': '5', 'password': 'password1', 'username': 'alice'}
{'id': '6', 'password': 'qwerty', 'username': 'bob'}
```
