因为飞虎脚本运行的文件名是：webserver
所以文件：webserver 其实是文件：manage.py 的复制品
所以如果更改了manage.py 记得同步更新 webserver

//可以使用如下2种方式启动django
python manage.py runserver 0.0.0.0:9999
python webserver runserver 0.0.0.0:9999
