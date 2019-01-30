""" 该类的作用主要是  对文件的增删改查操作
    读取配置文件：返回一个dict
    写配置文件：传入key-value值，根据相应的key值，修改配置文件
    可以照着其他的类写，所有的变量都要求是私有的，用@property来进行获取或者赋值，可参照其他类
"""
import configparser


class FileUtil(object):
    def __init__(self, file):
        self.__configfile = file
        self.__cfg = configparser.ConfigParser()

    def cfg_read(self):
        self.__cfg.read(self.__configfile)
        d = dict(self.__cfg._sections)
        for k in d:
            d[k] = dict(d[k])
        return d

        # 返回字典
    def del_item(self, section, key):
        self.__cfg.remove_option(section, key)

    def del_section(self, section):
        self.__cfg.remove_section(section)

    def add_section(self, section):
        self.__cfg.add_section(section)

    def set_item(self, section, key, value):
        self.__cfg.set(section, key, value)

    def save(self):
        fp = open(self.__configfile, 'w')
        self.__cfg.write(fp)
        fp.close()

    @property
    def configfile(self):
        return self.__configfile

    @property
    def conf(self):
        return self.__cfg

