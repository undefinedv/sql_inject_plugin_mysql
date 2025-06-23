<?php
// init.php
$mysqli = new mysqli("127.0.0.1", "root", "");

if ($mysqli->connect_error) {
    die("连接失败: " . $mysqli->connect_error);
}

// 创建数据库（如果不存在）
if (!$mysqli->query("CREATE DATABASE IF NOT EXISTS testdb")) {
    die("创建数据库失败: " . $mysqli->error);
}
$mysqli->select_db("testdb");

// 创建 user 表
$createTable = "
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
)";
if (!$mysqli->query($createTable)) {
    die("创建表失败: " . $mysqli->error);
}

// 插入测试用户数据
$mysqli->query("TRUNCATE TABLE user"); // 使用 TRUNCATE 清空旧数据
$mysqli->query("INSERT INTO user (username, password) VALUES ('admin', 'admin123')");
$mysqli->query("INSERT INTO user (username, password) VALUES ('alice', 'password1')");
$mysqli->query("INSERT INTO user (username, password) VALUES ('bob', 'qwerty')");

echo "数据库初始化完成！";

$mysqli->close();
?>
