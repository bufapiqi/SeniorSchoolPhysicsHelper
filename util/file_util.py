""" 该类的作用主要是  对文件的增删改查操作
    读取配置文件：返回一个dict
    写配置文件：传入key-value值，根据相应的key值，修改配置文件
    可以照着其他的类写，所有的变量都要求是私有的，用@property来进行获取或者赋值，可参照其他类
"""
import configparser


class FileUtil(object):
    def __init__(self, file: str):
        self.__configfile = file
        self.__cfg = configparser.ConfigParser()

    def cfg_read(self):
        self.__cfg.read(self.__configfile)
        d = dict(self.__cfg.sections())   # 这里不能直接dict会报错
        # sections() 返回的是section的列表并不是所有的key-value
        for k in d:
            d[k] = dict(d[k])
        return d

    def del_item(self, section: str, key: str):
        self.__cfg.remove_option(section, key)

    def del_section(self, section: str):
        self.__cfg.remove_section(section)

    def add_section(self, section: str):
        self.__cfg.add_section(section)

    def set_item(self, section: str, key: str, value: str):
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


if __name__ == '__main__':
    a = FileUtil("../resources/static.config")
    print(a.cfg_read())

