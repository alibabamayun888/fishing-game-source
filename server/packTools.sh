#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
from datetime import timedelta
import zipfile
import hashlib
import os
import re
import subprocess
import socket
import fcntl
import struct

GAME_NAME = "fish"       #圣手
#GAME_NAME = "zlfish"     #追龙
#GAME_NAME = "qmfish"     #掌门人
#GAME_NAME = "qm2fish"     #全民2

class UpdateHelper:

    def __init__(self):
        self.curDir = self.getCurDir()
        self.ymlDir = os.path.join(self.curDir, 'yml')
        self.svnDir = os.path.join(self.curDir, 'onlineUpdateSvn')
        self.sqlDir = os.path.join(self.curDir, 'sql')
        self.redisDir = os.path.join(self.curDir, 'redis')
        self.pygameconfigDir = os.path.join(self.curDir, 'pygameconfig')
        self.gamePrefix = self.getGamePrefix()    #游戏前缀 圣手:没有 追龙:zl 掌门人:qm
        
        self.makeSureDirExists(self.ymlDir)
        self.makeSureDirExists(self.svnDir)
        self.makeSureDirExists(self.sqlDir)
        self.makeSureDirExists(self.redisDir)
        self.makeSureDirExists(self.pygameconfigDir)

        self.ftpUser = 'pengcongsheng'
        self.ftpPass = 'EL1vtt6/jlPZaqkpxaSzbYyMO78Zo8gr3oOE/MLYd9w='
        self.ftpAddr = '103.215.44.162'

    def getCurDir(self):
        return os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    
    def makeSureDirExists(self, dirPath):
        if os.path.exists(dirPath):
            return
        os.makedirs(dirPath)

    def getGamePrefix(self):
        str_index = GAME_NAME.find("fish")
        if str_index > -1:
            return GAME_NAME[0:str_index]
        
        print('获取游戏前缀失败!...')
        sys.exit(0)

    def isHavePath(self, dstPath):
        tmpPath = dstPath
        if tmpPath.count('/*') > 0:
            tmpPath = tmpPath[0:tmpPath.rfind('/')]    # /data/xxx/* ---> /data/xxx
        retVal = os.path.exists(tmpPath)
        if retVal:  #目录存在，并且有权限操作才行
            if not os.access(tmpPath, os.R_OK):
                retVal = False
                print('无权读:{}'.format(tmpPath))
            if not os.access(tmpPath, os.W_OK):
                retVal = False
                print('无权写:{}'.format(tmpPath))
        return retVal

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    #外测需要先把文件拷贝到打包目录
    def cp2packdir(self):
        cpPackDirDict = {}

        local_ip = self.get_ip_address('eth0')
        if local_ip.find('192.168') >= 0:
            log = "local_ip %s 是内测.."%(local_ip)
            print(log)
            cpPackDirDict["./gameserver/pyscript/data/*.py"]      = "./pygameconfig/"
 
        else:
            log = "local_ip %s 是外测.."%(local_ip)
            print(log)
            #外测
            cpPackDirDict["/data/{}/dbserver_01/*"]       = "/data/{}_pack/dbserver/"
            cpPackDirDict["/data/{}/gameserver_01/*"]     = "/data/{}_pack/gameserver/"
            cpPackDirDict["/data/{}/gateserver_01/*"]     = "/data/{}_pack/gateserver/"
            cpPackDirDict["/data/{}/globalserver_01/*"]   = "/data/{}_pack/globalserver/"
            cpPackDirDict["/data/{}/loginserver_01/*"]    = "/data/{}_pack/loginserver/"
            cpPackDirDict["/data/{}/platformserver_01/*"] = "/data/{}_pack/platformserver/"
            cpPackDirDict["/data/{}/unionserver_01/*"]    = "/data/{}_pack/unionserver/"
            cpPackDirDict["/data/{}/webserver_01/*"]      = "/data/{}_pack/webserver/"
            cpPackDirDict["/data/{}/webadmin_01/*"]       = "/data/{}_pack/webadmin/"
            cpPackDirDict["/data/{}/csv/*"]               = "/data/{}_pack/csv/"
            cpPackDirDict["/data/{}/pygameconfig/*"]      = "/data/{}_pack/pygameconfig/"
            cpPackDirDict["/data/{}/webadminconf/*"]      = "/data/{}_pack/webadminconf/"
            cpPackDirDict["/data/{}/webserverconf/*"]     = "/data/{}_pack/webserverconf/"

        #内测
        #cpPackDirDict["/data/{}/gameserver/pyscript/data/*.py"]="/data/{}/pygameconfig/"
        #cpPackDirDict["/home/qmby/by/gameserver/pyscript/data/*.py"]="/home/qmby/by/pygameconfig/"
        #cpPackDirDict["/home/huangyx/game/qmfish/gameserver/pyscript/data/*.py"]="/home/huangyx/game/qmfish/pygameconfig/"
        
        
        for k,v in cpPackDirDict.items():
            srcDir = k
            dstDir = v
            if srcDir.count('{}') > 0:
                srcDir = k.format(GAME_NAME)
            if dstDir.count('{}') > 0:   
                dstDir = v.format(GAME_NAME)

            if self.isHavePath(srcDir) and self.isHavePath(dstDir):
                log = "cp2packdir copy %s ------------>>>>>> %s"%(srcDir, dstDir)
                print(log)
                cmd = "/bin/cp -rf %s %s"%(srcDir, dstDir)
                self.runCmd(cmd)

    
    def runCmd(self, cmd):
        # logList = os.popen(cmd).readlines()
        # for log in logList:
        #     print(log)

        subprocess.call(cmd, shell=True)
    
    def delFile(self, filePath):
        if os.path.isfile(filePath):
            os.remove(filePath)

    def getFileMD5(self, filepath):
        if os.path.isfile(filepath):
            md5obj = hashlib.md5()
            maxbuf = 8192
            f = open(filepath,'rb')
            while True:
                buf = f.read(maxbuf)
                if not buf:
                    break
                md5obj.update(buf)
            f.close()
            hash = md5obj.hexdigest()
            return str(hash)
        return None
    
    def uploadFtpFile(self, filePath):
        #lftp ${ftp_addr} -u${ftp_user},"${ftp_pass}" -e"cd update; put ${file}; bye"
        cmd = 'lftp {} -u{},"{}" -e"cd update; put {}; bye" '.format(self.ftpAddr, self.ftpUser, self.ftpPass, filePath)
        self.runCmd(cmd)

    def makeZipMd5(self, zipFileName):
        #ver = re.sub("\D", "", zipFileName) #版本号
        b_index = zipFileName.find('-') + 1
        e_index = zipFileName.find('.')
        ver = zipFileName[b_index:e_index]
        content_dict = {}
        zip_file = zipfile.ZipFile(os.path.join(self.curDir, zipFileName))
        for zfile_name in zip_file.namelist():
            s_str = zfile_name.split("/")
            file_name = s_str[0] + ".yml"
            if not content_dict.has_key(file_name):
                content_dict[file_name] = ""
            str_md5 = self.getFileMD5(zfile_name)
            if str_md5:
                s_str.pop(0)
                z_str = "/".join(s_str)
                content_dict[file_name] += "./" + z_str + ": " + str_md5 + "\n"

        #写文件
        for f_name, f_content in  content_dict.items():
            f_path = os.path.join(self.ymlDir, f_name)
            content = "ver: " + ver + "\n" + f_content
            f_handler = open(f_path, "w")
            f_handler.write(content)
            f_handler.close()

        print "makeZipMd5 finish..."

    def showPackTip(self):
        print('*********************** 打包需要注意的地方 ***********************')

        print('[1] 新功能更新记得写进： doc/服务端修改更新明细记录.xlsx ')
        print('[2] gameserver  只打pyc文件 ')
        print('[3] unionserver 只打pyc文件 ')
        print('[4] django webserver 只打py文件 ')
        print('[5] django webadmin  只打py文件 ')
        print('[6] redis和sql文件更新，打多几个换行，避免运维的shell脚本读取文件漏行 ')
        print('[7] sql\\xxx.sql     只保存sql   更新文件，  禁止有xxx.redis 更新文件 ')
        print('[8] redis\\xxx.redis 只保存redis 更新文件，  禁止有xxx.sql   更新文件 ')

        print('*****************************************************************')

    #是否打包游戏配置文件目录
    def isPackGameDataDir(self, argList):
        retVal = False
        for arg in argList:
            if (arg.count('gameserver/pyscript/data') >= 1 or arg.count('gameserver/pyscript') >= 1) and arg.count('.py') <= 0:
                retVal = True
                break
        return retVal
    
    #把.pyc对应的配置文件也打包
    def addGameDataFile(self, argList):
        dataFileList = []
        for arg in argList:
            if (arg.count('gameserver/pyscript/data') >= 1 or arg.count('gameserver/pyscript') >= 1) and arg.count('.pyc') >= 1:
                pyDataFile = arg[arg.rfind('/') + 1:].replace('.pyc', '.py')
                item = '-r pygameconfig/{}'.format(pyDataFile)
                dataFileList.append(item)
        for item in dataFileList:
            argList.append(item)
    
    def getDirFileList(self, dirPath):
        if not os.path.exists(dirPath):
            return []
        fileList = []
        tmpList = os.listdir(dirPath)
        for fileName in tmpList:
            path = os.path.join(dirPath, fileName)
            if os.path.isfile(path):
                fileList.append(path)
        return fileList
    
    def getFileLines(self, filePath):
        f = open(filePath)
        lines = f.readlines()
        f.close()
        return lines

    def isFileHaveNewLine(self, filePath):
        retVal = False
        lines = self.getFileLines(filePath)
        for line in lines:
            if line.count('\n') > 0:
                retVal = True
                break
        return retVal

    def checkSqlScript(self):
        sqlScriptList = self.getDirFileList(self.sqlDir)

        #fishdb-    webadmin-    webserver-
        #zlfishdb-  zlwebadmin-  zlwebserver-
        #qmfishdb-  qmwebadmin-  qmwebserver-
        fishPrefix      = '{}db-'.format(GAME_NAME)
        webadminPrefix  = '{}webadmin-'.format(self.gamePrefix)
        webserverPrefix = '{}webserver-'.format(self.gamePrefix)

        for filePath in sqlScriptList:
            if not filePath.endswith('.sql'):
                self.showPackTip()
                print('发现非.sql后缀文件:{}'.format(filePath))
                sys.exit(0)

            fileName = os.path.basename(filePath)
            isPrefixOk = False
            if fileName.count(fishPrefix) > 0:
                isPrefixOk = True
            if fileName.count(webadminPrefix) > 0:
                isPrefixOk = True
            if fileName.count(webserverPrefix) > 0:
                isPrefixOk = True
            
            if not isPrefixOk:
                self.showPackTip()
                print('文件名前缀错误:{}'.format(filePath))
                print('参考前缀:{}'.format(fishPrefix))
                print('参考前缀:{}'.format(webadminPrefix))
                print('参考前缀:{}'.format(webserverPrefix))
                sys.exit(0)

            #是否有换行符
            if not self.isFileHaveNewLine(filePath):
                self.showPackTip()
                print('文件没有换行符:{} '.format(filePath))
                sys.exit(0)
    
    def checkRedisScript(self):
        redisScriptList = self.getDirFileList(self.redisDir)
        for filePath in redisScriptList:
            if not filePath.endswith('.redis'):
                self.showPackTip()
                print('发现非.redis后缀文件:{}'.format(filePath))
                sys.exit(0)

            #fishdb-
            #zlfishdb-
            #qmfishdb-
            fileName = os.path.basename(filePath)
            prefix = '{}db-'.format(GAME_NAME)
            dbName = ' {}db.'.format(GAME_NAME)
            if fileName.count(prefix) <= 0:
                self.showPackTip()
                print('文件前缀错误:{},正确的前缀是:{}'.format(filePath, prefix))
                sys.exit(0)

            #是否有换行符
            if not self.isFileHaveNewLine(filePath):
                self.showPackTip()
                print('文件没有换行符:{} '.format(filePath))
                sys.exit(0)
            
            #HDEL fishdb.tbl_sys_info.30001 8
            lines = self.getFileLines(filePath)
            for line in lines:
                if len(line) <= 5: #只有换行符吧
                    continue
                if line.count(dbName) <= 0:
                    self.showPackTip()
                    print('文件数据库名字写错了:{} '.format(filePath))
                    print('{}'.format(line))
                    print('正确数据库名字是:{} '.format(dbName))
                    sys.exit(0)

    def pack(self, argList):
        self.checkSqlScript()
        self.checkRedisScript()

        argList.append('-x *.svn/*')    #.svn文件夹不用打包

        if self.isPackGameDataDir(argList):
            argList.append('-r pygameconfig/')
        else:
            self.addGameDataFile(argList)

        #不打包server.csv，如确定要打包，注释下条语句
        argList.append('-x csv/Server.csv')

        #django配置文件不能打包进去
        argList.append('-x webserver/conf/webserver.py')
        argList.append('-x webadmin/conf/webadmin.py')

        #django只打py文件
        argList.append('-x webserver/*.pyc')
        argList.append('-x webadmin/*.pyc')
        argList.append('-x webserver/logs/*')
        argList.append('-x webadmin/logs/*')

        #过滤py文件, 预设四级子文件夹
        argList.append('-x gameserver/pyscript/*.py')
        argList.append('-x gameserver/pyscript/*/*.py')
        argList.append('-x gameserver/pyscript/*/*/*.py')
        argList.append('-x gameserver/pyscript/*/*/*/*.py')

        argList.append('-x unionserver/pyscript/*.py')
        argList.append('-x unionserver/pyscript/*/*.py')
        argList.append('-x unionserver/pyscript/*/*/*.py')
        argList.append('-x unionserver/pyscript/*/*/*/*.py')

        dtNow = datetime.now()
        fileName = '{}_server-{}'.format(GAME_NAME, dtNow.strftime('%Y%m%d%H%M%S'))
        zipFileName = '{}.zip'.format(fileName)
        md5FileName = '{}.md5'.format(fileName)
        
        self.delFile(zipFileName)
        self.delFile(md5FileName)

        args = ' '.join(argList)
        cmd = 'zip -r {} {}'.format(zipFileName, args)
        self.runCmd(cmd)

        #删除yml里的所有文件
        # rm -rf yml/*
        cmd = 'rm -rf {}/*'.format(self.ymlDir)
        self.runCmd(cmd)

        #生成各个被打包文件md5
        self.makeZipMd5(zipFileName)

        #先删除旧的 把yml添加进来 再重新打包
        self.delFile(zipFileName)
        argList.append('-r yml/')
        args = ' '.join(argList)
        cmd = 'zip -r {} {}'.format(zipFileName, args)
        self.runCmd(cmd)

        #清理旧文件
        self.delFile(os.path.join(self.svnDir, zipFileName))
        self.delFile(os.path.join(self.svnDir, md5FileName))

        #产生xxx.zip文件md5
        cmd = "md5sum {} > {}".format(zipFileName, md5FileName)
        self.runCmd(cmd)

        #拷贝文件到更新目录
        self.runCmd("mv {} {}".format(zipFileName, self.svnDir))
        self.runCmd("mv {} {}".format(md5FileName, self.svnDir))

        #上传文件到ftp
        self.uploadFtpFile(os.path.join(self.svnDir, zipFileName))
        self.uploadFtpFile(os.path.join(self.svnDir, md5FileName))

        self.showPackTip()
        log = "pack finish zip:%s md5:%s"%(zipFileName, md5FileName)
        print(log)


def main():
    argList = []
    for i in range(1, len(sys.argv)):
        # print "参数", i, sys.argv[i]
        argList.append(sys.argv[i])

    updateHelper = UpdateHelper()
    updateHelper.cp2packdir()
    updateHelper.pack(argList)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('请输入打包参数')
        sys.exit(0)

    main()
