CREATE DATABASE IF NOT EXISTS switchmap CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE switchmap;

CREATE USER IF NOT EXISTS 'switchmap'@'%' IDENTIFIED WITH mysql_native_password BY '${DB_PASSWORD}';

GRANT ALL PRIVILEGES ON switchmap.* TO 'switchmap'@'%';

FLUSH PRIVILEGES;

