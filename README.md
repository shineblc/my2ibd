# my2ibd

介绍

解析mysql8.0的数据文件, 生成相关SQL.

功能
DDL: 生成建表语句(无法区分唯一索引)

利用官方idb2sdi && python脚本 \
适用MySQL 8.0+

ibd_json.sh ：用来解析解析ibd文件，生成sdi的JSON信息  \
innodb_ibd.py : 用来提取JSON中的表结构和索引信息

示例： \
1、
先执行ibd_json.sh，解析ibd的SDI信息并生成JSON文件

```shell
[root@cluster-node2 opt]# sh ibd_json.sh
请输入路径，示例：/data/app:  /opt  #存放ibd文件的目录，解析后后会生成一个当前日期的文件夹，以ibd_json命名

[root@cluster-node2 opt]# ll
drwxr-xr-x  2 root root       4096 Apr 27 16:48 ibd_json

[root@cluster-node2 opt]# ll ibd_json
total 1564
-rw-r--r-- 1 root root  14039 Apr 27 16:50 cons100.ibd.json
-rw-r--r-- 1 root root  13102 Apr 27 16:50 cons11.ibd.json
-rw-r--r-- 1 root root  14298 Apr 27 16:50 cons1.ibd.json
-rw-r--r-- 1 root root  14771 Apr 27 16:50 cons22221.ibd.json
-rw-r--r-- 1 root root  14797 Apr 27 16:50 cons22223.ibd.json
```

2、
执行innodb_ibd.py文件，当前目录会生成以SQL形式开头的目录

```shell
[root@cluster-node2 opt]# python3.6 innodb_ibd.py

[root@cluster-node2 opt]# ll sql*
drwxr-xr-x  2 root root       4096 Apr 27 16:50 sql2023_04_27
#sql目录下是解析出来的表结构信息，可以通过解析出来的信息，还原到数据库，并通过表空间传输方式恢复
[root@cluster-node2 opt]# ll sql2023_04_27/
total 120
-rw-r--r-- 1 root root  168 Apr 27 16:50 cons100.sql
-rw-r--r-- 1 root root  165 Apr 27 16:50 cons11.sql
-rw-r--r-- 1 root root  182 Apr 27 16:50 cons1.sql

[root@cluster-node2 ~]# cat /opt/sql2023_04_27/cons1.sql
CREATE TABLE cons1(
id bigint NOT NULL AUTO_INCREMENT ,
c1 varchar(40) default 'aaa' ,
id2 bigint DEFAULT NULL ,
id3 bigint NOT NULL ,
PRIMARY KEY(id),index id2(id2)) ENGINE=InnoDB ;
```

