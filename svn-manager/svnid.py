
# -*- coding:UTF-8 -*-
import logging
from svnlog import svn_logger

class SvnId(object):
    """
    svn用户账号模块

    成员变量：
        name
        passwd
        privilege 字典  dir => mode
    方法：
        设置密码
        获取密码
        获得权限对象
        增加权限
        删除权限
        清理权限

    """
    def __init__(self,name,passwd=None):
        svn_logger.debug("id(%s) created" % name)
        self.name   = name
        if passwd:
            self.passwd = passwd
        self.privilege = {}

    def set_pass(self,passwd):
        svn_logger.debug("set password for (%s)" % self.name)
        self.passwd = passwd

    def get_pass(self,passwd):
        svn_logger.debug("get password for (%s)" % self.name)
        return self.passwd

    def get_privilege(self):
        svn_logger.debug("get privilege for (%s)" % self.name)
        return self.privilege

    def add_privilege(self,dir,mode = 'rw'):
        svn_logger.debug("add priv(%s) mode(%s) for (%s)" % (dir,mode,self.name))
        self.privilege[dir] = mode

    def del_privilege(self,dir):
        svn_logger.debug("add priv(%s) for (%s)" % (dir,self.name))
        del self.privilege[dir]

    def clear_privilege(self):
        svn_logger.debug("clear priv for (%s)" % (dir,self.name))
        self.privilege.clear()

    def display(self):
        print("ID: %s" % self.name)
        print("DIR:")
        for dir,mode in self.privilege.items():
            print("%s %s" % (dir,mode))

    def write_priv_to_file(self,filename):
        svn_logger.debug("write(%s) to file(%s)" % (self.name,filename))
        try:
            fh = open(filename,"a")
            for dir,mode in self.privilege.items():
                fh.write("[%s]" % dir)
                fh.write("%s = %s " % (self.name,mode) )
        except IOError:
            svn_logger.error("can not open (%s) !" % filename)
        finally:
            fh.close()
