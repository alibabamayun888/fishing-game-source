#!/bin/bash
#fish
#by mox 2018-06-04
#ver 2.4
#update 2018-09-01  解决停服误杀同名组件、解决找不到PID文件卡死进程、解决找不到执行文件没有任何输出
#update 2019-03-19 兼容所有捕鱼组件
#update 2019-03-21 解决pid文件不存输出错误信息的bug
#update 2019-03-29 修改为centos7启动,停止不依赖程序pid文件(程序写的pid有bug有时pid不会生成)

##########################################################################################
#全局变量
##########################################################################################
ShellDir=`cd $(dirname $0); pwd` 
User=by

load_config(){

    LoginUser=`who am i |awk '{print $1}'`
    GlobalConfFile=${ShellDir}/../../.config.ini
    ServerName=`dirname ${ShellDir}|awk -F'/' '{print $NF}'`
    GameType=`echo ${ShellDir}|awk -F'/' '{print $3}'`
    AppLogDir=/log/${GameType}/${ServerName}
    AppLog=${AppLogDir}/syslog/sys_${ServerName}.log
    LogFile=${AppLogDir}/$(echo `basename $0`|sed "s@.sh@.log@")
    ListenIp=`ip addr|awk -F'[/ ]+' '/inet/&&/brd/{print $3}'|egrep "^192.168|^172.|^10\."|sed -n '1p'`
    if (echo ${ServerName}|grep "^cliadmin" &>/dev/null);then
        StartType=flask
        SvrPrefiex=`echo ${ServerName}|awk -F_ '{print $1}'`
        Conf=${ShellDir}/../conf/${SvrPrefiex}.py
        ListenPort=`awk -F= '/APP_PORT/{print $NF}' ${Conf}|sed 's@[[:space:]]@@g'`
        Exec=${ShellDir}/../run.py
        sed -i "1s@.*@#!${ShellDir}/../.env/bin/python@" ${Exec}
        mkdir -p ${AppLogDir}/syslog ${AppLogDir}/operatelog
    elif (echo ${ServerName}|egrep "^webserver|^webadmin" &>/dev/null);then
        StartType=django
        SvrPrefiex=`echo ${ServerName}|awk -F_ '{print $1}'`
        Conf=${ShellDir}/../conf/${SvrPrefiex}.py
        ListenPort=`awk -F= '/SERVER_PORT/{print $NF}' ${Conf}|sed 's@[[:space:]]@@g'`
        BinFile=`ls -ltr ${ShellDir}/../|grep -v "^d"|grep "server$"|awk '{print $NF}'`
        Exec=${ShellDir}/../${BinFile}
        mkdir -p  ${AppLogDir}/syslog
    else
        StartType=c++
        BinFile=`ls ${ShellDir}/../bin/ |grep "server$"`
        Exec=${ShellDir}/../bin/${BinFile}
        chmod +x ${Exec}
        Conf=${ShellDir}/../conf/${ServerName}.conf
        ReloadPort=`grep -A2 "#.*Admin" ${Conf}|tail -n 1|awk '{print $3}'`
        if (echo ${ServerName}|egrep "dbserver" &>/dev/null);then
            ListenPort='null'
        else
            ListenPort=`grep -A2 ".*<1>" $Conf|tail -n 1|awk '{print $3}'`
        fi
        mkdir -p ${AppLogDir}/daylog ${AppLogDir}/syslog ${AppLogDir}/Monitor /log/${GameType}
    fi

    if (sed -n "/\b${ServerName}\]$/,/^$/p" ${GlobalConfFile}|grep "\bsvr_type\b" &>/dev/null);then
        svr_type=`sed -n "/\b${ServerName}\]$/,/^$/p" ${GlobalConfFile}|grep "\bsvr_type\b"|awk -F= '{print $2}'`
    else
        svr_type=null
    fi

    if (grep pid ${Conf} &>/dev/null);then
        PidFile=`awk -F= '/\.pid/{print $NF}' ${Conf}|sed 's@[[:space:]]@@'`
        if [ ! -f ${PidFile} ];then
            PidFile=null
        fi
    else
        PidFile=null
    fi
    log "exec func load_config"
    log "User:${User},LoginUser=${LoginUser},GlobalConfFile:${GlobalConfFile},ServerName:${ServerName},GameType:${GameType},AppLogDir:${AppLogDir},LogFile:${LogFile},ListenIp:${ListenIp},StartType:${StartType},Conf:${Conf},ListenPort:${ListenPort},Exec:${Exec},svr_type:${svr_type},PidFile:${PidFile}"

    chown -R ${User}:${User} `dirname ${ShellDir}`
    chown -R ${User}:${User} `dirname ${AppLogDir}`

}

log(){
	
	DATE_OUT="date +%F-%H:%M:%S"
	echo "[`$DATE_OUT`]: $1" >>$LogFile
	if [ $# -ne 1 ];then
		echo $1
	fi

}


start_flask(){

    log "exec function start_flask"
    log "exec source ${ShellDir}/../.env/bin/activate"
    source ${ShellDir}/../.env/bin/activate
    log "exec cd ${ShellDir}/../"
    cd ${ShellDir}/../
    #log "exec runuser -s /bin/bash ${User} -c \"${Exec}  &> ${AppLog} &\""
    #runuser -s /bin/bash ${User} -c "${Exec}  &> ${AppLog} &"
    log "exec ${Exec}  &> ${AppLog} &"
    ${Exec}  &> ${AppLog} &

}

start_django(){

    log "exec function start_django"
    chmod +x ${Exec}
    #log "exec runuser -s /bin/bash ${User} -c \"${Exec} &>> ${AppLog} &\""
    #runuser -s /bin/bash ${User} -c "${Exec} &>> ${AppLog} &"
    log "exec ${Exec} &>> ${AppLog}"
    ${Exec} &>> ${AppLog} &

}

start_c(){

    log "exec function start_c"
    #centos 6
    #log "run command [runuser -s /bin/bash ${User} -c \"${Exec} ${Conf} &>> ${AppLog} &\"]"
    #runuser -s /bin/bash ${User} -c "${Exec} ${Conf} &>> ${AppLog} &"
    
    #centos7.5
    log "run command [${Exec} ${Conf} &>> ${AppLog} &]"
    ${Exec} ${Conf} &>> ${AppLog} & 

}

start(){

    log "exec function start"
    case ${StartType} in
        flask)
        start_flask
        ;;
        django)
        start_django
        ;;
        c++)
        start_c
        ;;
    esac
    
}


reload() {

    log "exec function reload"
    log "run command [echo "reload"|nc -w1 127.0.0.1 ${ReloadPort}]"
	echo "reload"|nc -w1 127.0.0.1 ${ReloadPort}

}


stop(){

    log "exec function stop"
    
    local  pid=`ps -ef |grep ${Exec}|grep -v grep |awk '{print $2}'`
    log "svr_type:${svr_type}"
    if [ ${svr_type} == 4 ];then
        log "exec kill pid:${pid}"
        kill ${pid}
    else
	    kill -9 ${pid}
        log "exec kill -9 pid:${pid}"
    fi
    
}


####################
#获取进程状态
####################
#变量
	#ProcFlag 进程标识	
	#ListenPort 监听端口
	#ListenIp 监听IP

#返回值
	#运行状态返回0
	#关闭状态返回1

get_stat(){

	local ProcFlag=$1
	local ListenIp=$2
	local ListenPort=$3

    log "exec function get_stat args [ProcFlag=${ProcFlag} ListenIp=${ListenIp} ListenPort=${ListenPort}]"
	if (ps -ef |grep "${ProcFlag}"|grep ${User}|grep -v grep &>/dev/null);then
		log "User:${User} ServerName:${ServerName} ProcFlag:${ProcFlag} ProcFlag exist"
        if [ ${ListenPort} == 'null' ];then
            echo 0
            log "port:null return StatCode:0"
        else
		    if (nc -z -w 3 ${ListenIp} ${ListenPort});then
                log "ListenIp:${ListenIp} port:${ListenPort} is listen return StatCode:0"
			    echo 0 
		    else
                log "ListenIp:${ListenIp} port:${ListenPort} is not listen return StatCode:1"
			    echo 1
		    fi
        fi
	else
        log "User:${User} ServerName:${ServerName} ProcFlag:${ProcFlag} ProcFlag not exist return StatCode:1"
		echo 1
	fi

}


#############
#启停动作检测
#############
#变量
    #ProcFlag 进程标识
    #ServerName 服务名
    #ListenIp 监听IP
    #ListenPort 监听端口
	#Action 动作名[start|stop]
	#SleepTime 每次检测间隔时间
	#CheckSum 检测次数


action_check(){

    local ProcFlag=$1    
	local ServerName=$2  
	local ListenIp=$3    
	local ListenPort=$4  
	local Action=$5      
	local SleepTime=2
	local CheckSum=10

    log "exec function action_check args [ProcFlag=${ProcFlag} ServerName=${ServerName} ListenIp=${ListenIp}  ListenPort=${ListenPort} Action=${Action}]"
	for i in `seq 1 ${CheckSum}`;do
        sleep $SleepTime
        log "start check count ${i}"
        StatCode=`get_stat ${ProcFlag} ${ListenIp} ${ListenPort}`
        log "get StatCode:${StatCode}"

        if [ $Action == 'start' ];then
            if [ ${StatCode} -eq 0 ];then
                log "$Action ${ServerName} OK" yes
                echo "run" >$ShellDir/../status
                return 0
            else
                if [ $i -eq ${CheckSum} ];then
                    log "ERRO: ${Action} ${ServerName} time out port=${ListenPort}" yes
                    exit 7
                fi
            fi
        elif [ $Action == 'stop' ];then
            if [ ${StatCode} -ne 0 ];then
                log "$Action ${ServerName} OK" yes
                return 0
            else
                if [ $i -eq ${CheckSum} ];then
                    log "ERRO: $Action ${ServerName} time out port=${ListenPort}" yes
                    exit 7
                fi
            fi
        fi
    done

}


Action=$1
load_config
log "$Action"
ProcFlag=${Exec}
StatCode=`get_stat ${ProcFlag} ${ListenIp} ${ListenPort}`

case $Action in
	start)
		if [ ${StatCode} -eq 0 ];then
			echo "$Action ${ServerName} OK"
			echo "run" > $ShellDir/../status
			exit  0
		else
			start
			action_check ${ProcFlag} ${ServerName} ${ListenIp} ${ListenPort} ${Action}
		fi
		;;
	stop)
		if [ ${StatCode} -eq 1 ];then
			echo "$Action ${ServerName} OK"
			echo "shutdown" > $ShellDir/../status
			exit  0
		else
			stop
			echo "shutdown" >$ShellDir/../status
			action_check ${ProcFlag} ${ServerName} ${ListenIp} ${ListenPort} ${Action}
		fi
		;;
	restart)
		if [ ${StatCode} -eq 1 ];then
	    	echo "stop ${ServerName} OK"
			echo "shutdown" > $ShellDir/../status
	    else
	        stop
		echo "shutdown" >$ShellDir/../status
	        action_check ${ProcFlag} ${ServerName} ${ListenIp} ${ListenPort} stop
	    fi	    
		start
		action_check ${ProcFlag} ${ServerName} ${ListenIp} ${ListenPort} start
	    ;;
    status)
	    if [ ${StatCode} -eq 0 ];then
	    	echo "run"
	    elif [ ${StatCode} -eq 1 ];then
	    	echo "shutdown"
	    else
	    	echo "unknow stat"
	    fi
	    ;;
    reload)
	    reload
	    ;;
    *)
	    echo "useage:bash `basename $0` [start|stop|status|restart|reload]"
	    exit 7
	    ;;
esac
echo "" >>${LogFile}
