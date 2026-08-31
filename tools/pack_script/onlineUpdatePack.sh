#!/bin/bash

if [ $# -le 0 ];
then
  echo "请输入参数！"
  exit 0
fi

svndir=/data/fish_pack/onlineUpdateSvn

curpath=`pwd`
echo $curpath

function cp2packdir()
{
    if [ -d '/data/fish/dbserver_01' ];
    then
        /bin/cp -rf /data/fish/dbserver_01/* /data/fish_pack/dbserver/
        echo 'dbserver_01 exist, cp done'
    fi

    if [ -d '/data/fish/gameserver_01' ];
    then
        /bin/cp -rf /data/fish/gameserver_01/* /data/fish_pack/gameserver/
        echo 'gameserver_01 exist, cp done'
    fi 

    if [ -d '/data/fish/gateserver_01' ];
    then
        /bin/cp -rf /data/fish/gateserver_01/* /data/fish_pack/gateserver/
        echo 'gateserver_01 exist, cp done'
    fi

    if [ -d '/data/fish/globalserver_01' ];
    then
        /bin/cp -rf /data/fish/globalserver_01/* /data/fish_pack/globalserver/
        echo 'globalserver_01 exist, cp done'
    fi
 
    if [ -d '/data/fish/loginserver_01' ];
    then
        /bin/cp -rf /data/fish/loginserver_01/* /data/fish_pack/loginserver/
        echo 'loginserver_01 exist, cp done'
    fi

    if [ -d '/data/fish/platformserver_01' ];
    then
        /bin/cp -rf /data/fish/platformserver_01/* /data/fish_pack/platformserver/
        echo 'platformserver_01 exist, cp done'
    fi

    if [ -d '/data/fish/serveradmin_01' ];
    then
        /bin/cp -rf /data/fish/serveradmin_01/* /data/fish_pack/serveradmin/
        echo 'serveradmin_01 exist, cp done'
    fi
    
    if [ -d '/data/fish/unionserver_01' ];
    then
        /bin/cp -rf /data/fish/unionserver_01/* /data/fish_pack/unionserver/
        echo 'unionserver_01 exist, cp done'
    fi

    if [ -d '/data/fish/web_server' ];
    then
        /bin/cp -rf /data/fish/web_server/* /data/fish_pack/web_server/
        echo 'web_server exist, cp done'
    fi

    if [ -d '/data/fish/webserver_01' ];
    then
        /bin/cp -rf /data/fish/webserver_01/* /data/fish_pack/webserver/
        echo 'webserver exist, cp done'
    fi

    if [ -d '/data/fish/webadmin_01' ];
    then
        /bin/cp -rf /data/fish/webadmin_01/* /data/fish_pack/webadmin/
        echo 'webadmin exist, cp done'
    fi

    if [ -d '/data/fish/csv' ];
    then
        /bin/cp -rf /data/fish/csv/* /data/fish_pack/csv/
        echo 'csv exist, cp done'
    fi
   
    if [ -d '/data/fish/pyconfig' ];
    then
        /bin/cp -rf /data/fish/pyconfig/*.pyc /data/fish_pack/pyconfig/
        echo 'pyconfig exist, cp done'
    fi 

    if [ -d '/data/fish/pygameconfig' ];
    then
        /bin/cp -rf /data/fish/pygameconfig/* /data/fish_pack/pygameconfig/
        echo 'pygameconfig exist, cp done'
    fi  
   
}

#外测服需要cp到打包路径
cp2packdir

args=$*
#echo $args

for arg in "$@"
do
    if [ -d $arg  ];  
    then
       if [ $arg != "." -a $arg != ".." -a $arg != ".svn" ];then
          #忽略.svn文件
          for svnfile in `find $arg -name .svn`
          do
              exFile=`echo ${svnfile}|sed 's@.svn@*.svn*@g'`
              #echo $exFile
              args=${args}" -x "${exFile}
          done
          #如果data目录存在
          if [ -d $arg/data/ ];
          then
            args=${args}" -r pygameconfig/"
          fi
          #如果本身打包的就是data目录
          if [ $arg == gameserver/pyscript/data ] || [ $arg == gameserver/pyscript/data/ ];
          then
            args=${args}" -r pygameconfig/"
          fi
       fi  
    fi 

    #如果打包的是data的配置文件
    if [ -f $arg ];
    then
        name=${arg%.*}
        suffix=${arg#*.}
        findname=gameserver/pyscript/data/
        result=$(echo $name | grep "${findname}")
        if [ $suffix == 'pyc' ]; 
        then
            if [[ "$result" != "" ]]
            then
                name=pygameconfig/${name##*/}.py
                args=${args}" -r ${name}"
            fi
        fi
    fi 
done



#不打包server.csv，如确定要打包，注释下条语句
args=${args}" -x csv/Server.csv"

#不能打包config.py文件！
args=${args}" -x serveradmin/config.py"
args=${args}" -x webserver/conf/webserver.py"
args=${args}" -x webadmin/conf/webadmin.py"
args=${args}" -x webserver/sbin/*.sh"
args=${args}" -x webadmin/sbin/*.sh"
args=${args}" -x webserver/sbin/*.log"
args=${args}" -x webadmin/sbin/*.log"

#过滤py文件, 预设四级子文件夹
args=${args}" -x gameserver/pyscript/*.py"
args=${args}" -x gameserver/pyscript/*/*.py"
args=${args}" -x gameserver/pyscript/*/*/*.py"
args=${args}" -x gameserver/pyscript/*/*/*/*.py"

args=${args}" -x unionserver/pyscript/*.py"
args=${args}" -x unionserver/pyscript/*/*.py"
args=${args}" -x unionserver/pyscript/*/*/*.py"
args=${args}" -x unionserver/pyscript/*/*/*/*.py"


curTime=`date "+%Y%m%d%H%M"`
fileName=fish_server-${curTime}
zipFileName=${fileName}.zip
md5FileName=${fileName}.md5
ymlfilename=fileUpdateMd5.py

zip -r ${zipFileName} $args
#先删除yml里的所有文件
rm -rf yml/*

#调用python脚本把更改的文件MD5写进入对应的目录
python ${ymlfilename} ${zipFileName}

#先删除旧的把yml的添加再打包
rm ${zipFileName}
args=${args}" -r yml/"

zip -r ${zipFileName} $args
mv ${zipFileName} ${svndir}
cd ${svndir}
md5sum ${zipFileName} > ${md5FileName}
echo ${zipFileName} ${md5FileName}
#svn add ${fileName}.*
#svn commit -m "${fileName}" ${fileName}.*
cd ${curpath}
./upload.sh ${svndir}/${zipFileName}
./upload.sh ${svndir}/${md5FileName}
echo "打包完成，已上传FTP，${zipFileName} ${md5FileName}"
