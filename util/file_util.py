""" 该类的作用主要是  对文件的增删改查操作
    读取配置文件：返回一个dict
    写配置文件：传入key-value值，根据相应的key值，修改配置文件
    可以照着其他的类写，所有的变量都要求是私有的，用@property来进行获取或者赋值，可参照其他类
"""


import configparser
#import os
#from resources.static1 import *
class FileUtil(object):
    def __init__(self,file):
        self.configfile=file
        self.cfg=configparser.ConfigParser()
    def cfg_read(self):
        self.cfg.read(self.configfile)
        d=dict(self.cfg._sections)
        for k in d:
            d[k]=dict(d[k])
        return d

        '''返回字典'''
    def del_item(self,section,key):
        self.cfg.remove_option(section,key)
    def del_section(self,section):
        self.cfg.remove_section(section)
    def add_section(self,section):
        self.cfg.add_section(section)
    def set_item(self,section,key,value):
        self.cfg.set(section,key,value)
    def save(self):
        fp=open(self.configfile,'w')
        self.cfg.write(fp)
        fp.close()

