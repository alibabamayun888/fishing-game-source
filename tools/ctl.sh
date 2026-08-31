#!/bin/bash
#统一启动停止重启脚本，如果要放到项目根目录下运行, 如 /data/fish/下面则需要修改下面的for循环的寻找路径即可
#检测当前目录下的文件夹里面是否有sbin文件夹，有就执行sbin下面的启动脚本
Action=$1
ShellDir=`cd $(dirname $0); pwd`
for sbindir in `find ${ShellDir}/../ -name sbin`;do
	echo ${sbindir}
	cd ${sbindir}
	bash daemon.sh $Action
done


