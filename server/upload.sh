#!/bin/bash
ftp_user=pengcongsheng
ftp_pass='EL1vtt6/jlPZaqkpxaSzbYyMO78Zo8gr3oOE/MLYd9w='
ftp_addr=103.215.44.162
file=$1
args=$#

err_echo(){

    echo -e "\\033[31m[Error]: $1 \\033[0m"
    exit 1
}

check_args(){

    if [ ${args} -ne 1 ];then
        err_echo "useage: bash `basename $0` filename"
        exit 7
    fi
}

check_file(){

    if [ ! -f ${file} ];then
        err_echo "${file} not found"
        exit 7
    fi
}

check_lftp(){
    
    if !( which lftp &>/dev/null);then
        yum -y install lftp
        ! grep "set ssl:verify-certificate no" /etc/lftp.conf
        echo "set ssl:verify-certificate no" >>/etc/lftp.conf 
        echo "set xfer:clobber on" >>/etc/lftp.conf
    fi
}


main(){

    check_args
    check_lftp
    check_file
    lftp ${ftp_addr} -u${ftp_user},"${ftp_pass}" -e"cd update; put ${file}; bye"

}

main
