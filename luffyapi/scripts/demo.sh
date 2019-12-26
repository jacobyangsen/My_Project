#! /bin/bash

echo "导出数据库"
mysqldump -uroot -p luffy > ./luffy.sql
echo "执行完成"