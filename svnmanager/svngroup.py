
# -*- coding:UTF-8 -*-
from svnid import *
from svnlog import svn_logger

class SvnGroup:
    """
    svn组模块

    成员变量：
        name
        idlist  列表 ， 每个元素是一个SvnId对象
        privilege 字典  目录权限
    方法：
        增加id
        减少id
        增加权限
        删除权限
        获得权限对象
        打印成员和权限
    备注：
        SvnGroup对象并不操作SvnId的privilege变量。
        两种权限区分开来
    """
    def __init__(self,name,idlist=None,privilege=None):
        svn_logger.debug("Group(%s) created" %  name)
        self.name      = name
        self.idlist = []
        self.privilege = {}
        if idlist:
            self.idlist    = idlist
        if privilege:
            self.privilege = privilege

    def add_id(self, id):
        svn_logger.debug("Group(%s) add id (%s)" % (self.name,id.name))
        if not self.has_id(id):
            self.idlist.append(id)

    def del_id(self, id):
        svn_logger.debug("Group(%s) del id (%s)" % (self.name,id.name))
        if  self.has_id(id):
            self.idlist.remove(id)

    def add_privilege(self,dir,mode='rw'):
        svn_logger.debug("Group(%s) add priv (%s) mode (%s)" % (self.name,dir,mode))
        self.privilege[dir] = mode


    def del_privilege(self,dir):
        svn_logger.debug("Group(%s) del priv (%s) " % (self.name,dir))
        if dir in self.privilege :
            del self.privilege[dir]
        else:
            svn_logger.warn("Group(%s) do not have privilege dir(%s)" % (self.name,dir))

    def get_privilege(self,dir):
        svn_logger.debug("Group(%s) get priv (%s) " % (self.name,dir))
        return self.privilege


    def display(self):
        svn_logger.debug("Group(%s) display  " % self.name)
        print("Group: %s" % self.name)
        print("ID:")
        for id in self.idlist:
            print(" "  +  id.name )
        print("DIR:")
        for dir,mode in self.privilege.items():
            print("%-3s %s" % (mode,dir))

    def write_priv_to_file(self,filename):
        svn_logger.debug("Group(%s) write to file(%s)  " % (self.name,filename))
        try:
            fh = open(filename,"a")
            for dir,mode in self.privilege.iteritems:
                fh.write("[%s]" % dir)
                fh.write("@%s = %s " % (self.name,mode))
        except IOError:
            print("can not open (%s) !" % filename)
        finally:
            fh.close()

    def get_idlist_as_string(self):
        svn_logger.debug("Group(%s) get idlist  as str()  " % self.name)
        id_name_list = []
        for id in self.idlist:
           # print(id.name)
            id_name_list.append(id.name)
        string = ",".join(id_name_list)
        return string

    def get_id_name_list(self):
        svn_logger.debug("Group(%s) get idlist  as  list()  " % self.name)
        id_name_list=[]
        for id in self.idlist:
            id_name_list.append(id.name)
        return id_name_list

    def has_id(self,id):
        if id.name in self.get_id_name_list():
            svn_logger.debug("Group(%s) contain id(%s)  " % (self.name,id.name))
            return True
        else:
            svn_logger.debug("Group(%s) do  not contain id(%s)  " % (self.name,id.name))
            return False
