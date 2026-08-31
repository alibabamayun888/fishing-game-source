#!/bin/bash
#根据指定版本中转配置文件.config.ini生成新的配置文件
#by mox 20190318
#新搭建项目时使用，根据指定路径下面的.config.ini生成新的.config.ini
#该脚本会在csv_path目录下生成Server.csv文件

help_arg(){

    echo '
    --input_file= 必要参数.config中转配置文件路径, 如--input_file=/data/fish/.config.ini
    --prefix= 安装目录前缀,如追龙捕鱼--prefix=zl
    --port_prefix= 端口前三位, 如 --port_prefix=135
    --env= 安装环境，如 --env=test
    --domain= 使用的域名, 内测使用ip，留空--domain=
    --output_file= 生成的配置文件路径和文件名, 如--output_file=/data/zlfish/.config.ini
    --csv_path= 生成的Server.csv文件的路径，如 --csv_path=/data/fish/csv/
'
    exit 7
}

get_arg_value(){
    
    local arg=$1
    echo ${arg}|awk -F= '{print $2}'
}

read_args(){
    
    local args=$1
    for arg in ${args};do
        if (echo ${arg}|grep "^--prefix=" &>/dev/null);then
            prefix=`get_arg_value ${arg}`
        elif (echo ${arg}|grep "^--input_file=" &>/dev/null);then
            input_file=`get_arg_value ${arg}`
        elif (echo ${arg}|grep "^--port_prefix=" &>/dev/null);then
            port_prefix=`get_arg_value ${arg}`
        elif (echo ${arg}|grep "^--env=" &>/dev/null);then
            env=`get_arg_value ${arg}`
        elif (echo ${arg}|grep "^--domain=" &>/dev/null);then
            domain=`get_arg_value ${arg}`
        elif (echo ${arg}|grep "^--output_file=" &>/dev/null);then
            output_file=`get_arg_value ${arg}`
        elif (echo ${arg}|grep "^--csv_path=" &>/dev/null);then
            csv_path=`get_arg_value ${arg}`
        elif (echo ${arg}|grep "^-h|--help=" &>/dev/null);then
            help_arg
        fi
    done

    #变量默认值
    port_prefix=${port_prefix:=120}
    domain=${domain:=nb1768.com}
    output_file=${output_file:=/tmp/${prefix}fish.ini}
    csv_path=${csv_path:=/tmp/}
    csv_file=${csv_file:=${csv_path}/Server.csv}
    svraddr=${svraddr:=127.0.0.1}
    #备份旧的server.csv
    if [ -f ${csv_file} ];then
        cp ${csv_file} ${csv_file}.bak
    fi

    let admin_port_prefix=port_prefix+1
    svrid_tag=${admin_port_prefix:1:2}
    let semkey_tag=svrid_tag+1
    if [ -f /data/${prefix}fish/csv/Server.csv ];then
        csv_file=/data/${prefix}fish/csv/Server.csv
    fi

    if [ -z "${input_file}" ];then
        help_arg
    fi

}

create_csv_title(){

cat >${csv_file} <<EOF
//标记用途,填充颜色
//服务器和客户端公用
//服务器端专用
//客户端专用
//不导出
//结束标志


//int,//int,//string,//int,//int,//int
ServerList
//服务器ID,//服务器类型,//服务器地址,//服务器端口,//是否全局服,//是否开服
server_id,server_type,addr,port,global,open
EOF

}

create_config(){

    local input_file=$1
    >${output_file}
    while read line;do
        option=`echo ${line}|awk -F= '{print $1}'`
        if (echo ${line}|grep "^\[");then
            tag=`echo ${line}|sed 's@\[@@;s@\]@@'` 
            tag_prefix=`echo ${tag}|awk -F_ '{print $1}'`
            if [ ${tag} == global ];then
                db_name=${prefix}fishdb
            else
                db_name=${prefix}${tag_prefix}
            fi
            db_user=${db_name}_user
            echo ${line} >>${output_file}
        #更新数据名
        elif (echo ${line}|grep "db_name=" &>/dev/null);then
            echo ${option}=${db_name} >>${output_file}
        #更新数据库用户名
        #elif (echo ${line}|grep "db_user=" &>/dev/null);then
        #    echo ${option}=${db_user} >>${output_file}
        #更新数据库密码
        #elif (echo ${line}|grep "db_password=" &>/dev/null);then
        #    password=`openssl rand -base64 25|md5sum |awk '{print $1}'`
        #    echo ${option}=${password} >>${output_file}
        #更新日志目录
        elif (echo ${line}|grep "^log_root=" &>/dev/null);then
            log_root=/log/${prefix}fish
            echo ${option}=${log_root} >>${output_file}
        #更新skd bi日志目录
        elif (echo ${line}|grep "^operate_log_path=" &>/dev/null);then
            operate_log_path=/log/${prefix}fish/operatelog
            echo ${option}=${operate_log_path} >>${output_file}
        #更新webadmin域名
        elif (echo ${line}|grep "^webadmin_host=" &>/dev/null);then
            domain_prefix=`echo ${line}|awk -F '[=|.|:]' -v OFS=. '{print $3}'`
            old_port=`echo ${line}|awk -F: '{print $NF}'`
            old_port_postfix=${old_port:3:4}
            webadmin_port=${port_prefix}${old_port_postfix}
            #webadmin_host=http:${domain_prefix}.${prefix}fish.${domain}:${webadmin_port}
            #内测使用ip不用域名，直接替换端口就行
            domain_ip=`echo ${line}|awk -F '[=|:|:]' -v OFS=. '{print $3}'`
            webadmin_host=http:${domain_ip}:${webadmin_port}
            echo ${option}=${webadmin_host} >>${output_file}
        #更新shmkey
        elif (echo ${line}|grep "^shmkey=" &>/dev/null);then
            oldshmkey=`echo ${line}|awk -F= '{print $2}'`
            oldshmkey_prefix=${oldshmkey:0:2}
            #shmkey=${oldshmkey_prefix}${svrid_tag}
            #前缀字符串后面加1
            shmkey=${port_prefix}1
            echo ${option}=${shmkey} >>${output_file}
        #更新semkey
        elif (echo ${line}|grep "^semkey=" &>/dev/null);then
            oldsemkey=`echo ${line}|awk -F= '{print $2}'`
            oldsemkey_prefix=${oldsemkey:0:2}
            #semkey=${oldsemkey_prefix}${semkey_tag}
            semkey=${port_prefix}2
            echo ${option}=${semkey} >>${output_file}
        #更新网关域名
        #elif (echo ${line}|grep "^gate_ip=" &>/dev/null);then
        #    domain_prefix=`echo ${line}|awk -F'[=|.]' -v OFS=. '{print $2}'`
        #    gate_ip=${domain_prefix}.${prefix}fish.${domain}
        #    echo ${option}=${gate_ip} >>${output_file}
        #更新端口
        elif (echo ${line}|grep "^port" &>/dev/null);then
            old_port=`echo ${line}|awk -F= '{print $2}'`
            old_port_postfix=${old_port:3:4}
            new_port=${port_prefix}${old_port_postfix}
            echo ${option}=${new_port} >>${output_file}
        #更新全局thirft端口
        elif (echo ${line}|grep "^global_thrift_port" &>/dev/null);then
            global_thrift_port=${port_prefix}90
            echo ${option}=${global_thrift_port} >>${output_file}
        #更新thrift端口
        elif (echo ${line}|grep "^thrift_port" &>/dev/null);then
            thrift_port=${admin_port_prefix}90
            echo ${option}=${thrift_port} >>${output_file}
        #更新admin端口
        elif (echo ${line}|grep "^admin_port" &>/dev/null);then
            old_admin_port=`echo ${line}|awk -F= '{print $2}'`
            old_admin_port_postfix=${old_admin_port:3:2}
            new_admin_port=${admin_port_prefix}${old_admin_port_postfix}
            echo ${option}=${new_admin_port} >>${output_file}
        #更新svrid
        elif (echo ${line}|grep "^svrid" &>/dev/null);then
            svrid=`echo ${line}|awk -F= '{print $2}'`
            svrid_prefix=${svrid:0:1}
            svrid_postfix=${svrid:3:2}
            svrid=${svrid_prefix}${svrid_tag}${svrid_postfix}
            echo ${option}=${svrid} >>${output_file}
        #更新plat公钥地址
        elif (echo ${line}|grep "^exchange_pubkeyfile" &>/dev/null);then
            pubkeyfile=/data/${prefix}fish/cert/pubkey.pem
            echo ${option}=${pubkeyfile} >>${output_file}
        #更新plat私钥地址
        elif (echo ${line}|grep "^exchange_prikeyfile" &>/dev/null);then
            pubkeyfile=/data/${prefix}fish/cert/prikey.pem
            echo ${option}=${pubkeyfile} >>${output_file}
        #获取svr_type的值
        elif (echo ${line}|grep "^svr_type" &>/dev/null);then
            svr_type=`echo ${line}|awk -F= '{print $2}'`
            echo ${line} >>${output_file}
        else
            echo $line >> ${output_file}
        fi
        
        #生成csv文件
        if [ -z "${line}" ];then
            if (echo ${svr_type} |egrep "\b1\b|\b5\b" &>/dev/null);then
                global_flag=1
            else
                global_flag=0
            fi
            if [ -n "${svr_type}" ];then
                if ! (grep "^${svrid}" ${csv_file} &>/dev/null);then
                    echo ${svrid},${svr_type},${svraddr},${new_port},${global_flag},1 >>${csv_file}
                fi
            fi
        fi
    done <${input_file}

}

main(){

    read_args "${args}"
    create_csv_title
    create_config ${input_file}

}

args=$*
main
