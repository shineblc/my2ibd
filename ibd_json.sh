#!/bin/bash
#print the directory and file
read -p "请输入路径，示例：/data/app:  " basedir
  if [ ! -n "$basedir" ]; then
    echo "#######请输入路径，格式：/data/app，注意后面不加/#######"
  fi
  dir_json=./ibd_json
  TIME1=`date +"%Y-%m-%d"`
  if [ ! -f "$dir_json" ]; then
     mv $dir_json ${dir_json}_${TIME1}  && mkdir $dir_json
  else
     mkdir $dir_json
  fi

for file in $basedir/*.ibd
do
data=${file##*/}
ibd2sdi $file >$dir_json/$data.json
#因为全局索引是会生成fts_0000000000开头的文件，解析时候并不需要，所以rm即可,注意此处也可以自行rm
#rm -rf $dir_json/fts_00000000*
done
