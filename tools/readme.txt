1、这是tools文件夹下的脚本功能说明

2、create_config.sh 是新搭建项目时根据旧的.config.ini生成新的.config.ini 用的，具体看脚本文件的注释和说明

3、configure.py 用来根据tpl配置文件模板和.config.ini生成配置文件，具体操作看脚本文件说明

4、fish_up.sh 是跟configure.py 配合使用，把生成的配置文件复制到各个server下面去

5、ctl.sh 是一键启停所有server的脚本

6、daemon.sh 是管理启动脚本的模板, 跟up_daemon.sh 配合使用，一键更新到各个server的sbin下面

7、up_daemon.sh 更新管理启动脚本，把daemon.sh 更新到各个server下的sbin里面去
