<?php
// index.php
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>登录页面</title>
    <style>
        body { font-family: sans-serif; }
        form { border: 1px solid #ccc; padding: 20px; border-radius: 5px; width: 300px; }
        input { margin-bottom: 10px; padding: 8px; width: 95%; }
        input[type="submit"] { background-color: #4CAF50; color: white; cursor: pointer; }
    </style>
</head>
<body>

    <h2>用户登录</h2>
    <form action="index.php" method="GET">
        <label for="username">用户名:</label>
        <input type="text" id="username" name="username">
        <label for="password">密码:</label>
        <input type="password" id="password" name="password">
        <input type="submit" value="登录">
    </form>

<?php
// 检查是否有表单提交
if (isset($_REQUEST['username']) && isset($_REQUEST['password'])) {
    $mysqli = new mysqli("127.0.0.1", "root", "", "testdb");

    if ($mysqli->connect_error) {
        die("连接失败: " . $mysqli->connect_error);
    }

    $username = $_REQUEST['username'];
    $password = $_REQUEST['password'];

    // 漏洞点：直接将用户输入拼接进 SQL
    $sql = "SELECT * FROM user WHERE username = '$username' AND password = '$password'";
    var_dump($sql);
    $result = $mysqli->query($sql);


    if ($result && $result->num_rows > 0) {
        echo "<h3>登录成功</h3>";
    } else {
        echo "<h3>登录失败</h3>";
    }

    // 为了演示注入效果，显示拼接的SQL
    echo "<p><strong>执行的SQL查询:</strong> " . htmlspecialchars($sql) . "</p>"; 

    $mysqli->close();
}
?>
</body>
</html>
