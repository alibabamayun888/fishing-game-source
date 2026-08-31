#! /usr/bin/python
# -*- coding: utf-8 -*-
#捕鱼渲染配置文件
#by mox 2018-07-30
#根据.config.ini和模板文件生成配置文件，传入游戏根目录(即.config.ini的目录)和模板tpl的路径。如 python configure.py /data/fish/ ./fish/
#脚本会在游戏根目录找到.config.ini，再在模板的目录找到tpl文件夹，生成配置文件到模板的目录下面的tpl_out文件夹里面
#如果要tpl_out文件夹下面的配置文件一键复制到各个server下面的conf目录下，则需要生成好配置文件后，再运行 fish_up.sh 脚本
from jinja2 import Environment, FileSystemLoader
import ConfigParser
import os, sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


#判断文件夹是否存在，不存在则创建
def chk_mkdir(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

#从ini文件中读取配置
def load_config(server_name):
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)
    server_name_values = cf.items(server_name)
    global_values = cf.items('global')
    discard_str=re.compile('py$')
    server_name_info = discard_str.sub('',server_name)
    log_dir = cf.get( 'global', 'log_root') + "/" + server_name_info
    log_dir_value = [['log_dir', log_dir]]
    values = server_name_values + global_values + log_dir_value
    return values

def get_server_name():
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)
    server_names = {}
    for server_name in cf.sections():
        try:
            use_template = cf.get(server_name, "use_template")
        except Exception,e:
            use_template = server_name.split('_')[0]
        server_names[server_name]=use_template

    return server_names

#用jinja渲染模板生成最终配置文件的主函数
def render_to_file(template_dir):
    env = Environment(loader = FileSystemLoader(template_dir))
    # 渲染tpl目录下的server_name.conf模板
    tpl_list = os.listdir(template_dir)
    for tpl_file in tpl_list:
        tpl_name = tpl_file.split('.')[0]  
        suffix = tpl_file.split('.')[1]
        server_names = get_server_name()
        for server_name in server_names.keys():
            if server_names[server_name] == tpl_name:
                output_dir = '{update_dir}/tpl_out/'.format(update_dir=update_dir,server_name=server_name)
                chk_mkdir(output_dir)
                tpl = env.get_template(tpl_file)
                info = load_config(server_name)
                output = tpl.render(info)
                output_file = output_dir + server_name + "." + suffix
                with open(output_file, 'w') as out:
                    out.write(output)
                print "渲染{output_file} OK".format(output_file=output_file) 

if __name__ == "__main__":
    game_root = sys.argv [1]
    update_dir = sys.argv[2]
    config_file = game_root + "/.config.ini"
    template_dir = '{update_dir}/tpl/'.format(update_dir=update_dir)
    render_to_file(template_dir)
