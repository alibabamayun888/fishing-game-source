#!/usr/bin/env python
import os
import sys
import conf.webserver
import conf.system

def addPath():
    for dstDir in conf.system.PROJECT_FILE_SEARCH_DIR:
        sys.path.append(sys.path[0] + dstDir)

if __name__ == "__main__":
    addPath()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoserver.settings")

    from django.core.management import execute_from_command_line

    server = str(conf.webserver.SERVER_ADDR) + ':' + str(conf.webserver.SERVER_PORT)
    listArgv = ['manage.py', 'runserver', server]

    # execute_from_command_line(sys.argv)
    execute_from_command_line(listArgv)
