#!/bin/bash
#管理启动脚本模板更新后，使用这个脚本一键更新到各个server下面的sbin下面去
Action=$1
daemonfile=./daemon.sh
ShellDir=`cd $(dirname $0); pwd`
for sbindir in `find ${ShellDir}/../ -name sbin`;do
	echo up ${sbindir}/daemon.sh
	/bin/cp -rf ${daemonfile} ${sbindir}
done


