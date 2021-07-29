#!/usr/bin/python
# coding:utf-8

"""
配置文件管理
"""
import configparser


class Configer(object):

    def __init__(self, recordfile):
        self.logfile = recordfile
        self.cfg = configparser.ConfigParser()

    def cfg_load(self):
        self.cfg.read(self.logfile)

    def cfg_dump(self):
        se_list = self.cfg.sections()
        print('=' * 30)
        for se in se_list:
            print(se)
            print(self.cfg.items(se))
        print('=' * 30)

    def delete_item(self, section, key):
        return self.cfg.remove_option(section, key)

    def delete_section(self, section):
        return self.cfg.remove_section(section)

    def has_section(self, section):
        return self.cfg.has_section(section)

    def add_section(self, section):
        return self.cfg.add_section(section)

    def set_item(self, section, key, value):
        return self.cfg.set(section, key, value)

    def get_item(self, section, key):
        return self.cfg.get(section, key)

    def has_item(self, section, key):
        return self.cfg.has_option(section, key)

    def save(self):
        fp = open(self.logfile, 'w')
        self.cfg.write(fp)
        fp.close()


if __name__ == '__main__':
    ini = Configer('joke_config.ini')
    ini.cfg_load()
    ini.cfg_dump()

    ini.add_section('le8wu')
    ini.set_item('le8wu', 'page_pic', '1')
    ini.cfg_dump()

    # ini.save()
