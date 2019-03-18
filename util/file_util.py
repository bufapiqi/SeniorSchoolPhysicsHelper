""" 该类的作用主要是  对文件的增删改查操作
    读取配置文件：返回一个dict
    写配置文件：传入key-value值，根据相应的key值，修改配置文件
    可以照着其他的类写，所有的变量都要求是私有的，用@property来进行获取或者赋值，可参照其他类
"""
import configparser
#import os


# _*_ coding:utf-8 _*_

class FileUtil(object):
    def __init__(self, file: str):
        self.__configfile = file
        self.__cfg = configparser.ConfigParser()

    # def cfg_read(self):
    # self.__cfg.read(self.__configfile,encoding='utf8')
    # d = dict(self.__cfg.sections())   # 这里不能直接dict会报错
    # sections() 返回的是section的列表并不是所有的key-value
    # for k in d:
    # d[k] = dict(d[k])
    # return d

    def del_item(self, section: str, key: str):
        self.__cfg.remove_option(section, key)

    def del_section(self, section: str):
        self.__cfg.remove_section(section)

    def add_section1(self, section: str):
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


class MyParser(configparser.ConfigParser):  # 读取并返回字典

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
        return d


if __name__ == '__main__':
    a = FileUtil("../resources/static.config")
    b = MyParser()
    b.read("../resources/static.config", encoding="utf8")
    c = b.as_dict()
    # print(b.as_dict().get('C')+'123')
    print(c)
    print(a.add_section1("C"))
    print(a.save())
    print(a.set_item("C", "X", "4"))
    print(a.set_item("C", "M", "4"))
    print(a.save())
    print(a.add_section1("d"))
    print(a.save())
    print(a.set_item("d", 'length', '4'))
    print(a.set_item('d', 'width', '5'))
    print(a.save())
    #print(a.del_section("C"))
    #print(a.save())

    # 每次进行一次增删改操作，都要写入文件一次，即调用save()一次