
# -*- coding:UTF-8 -*-

import svnauth

from svnlog import svn_logger

class SvnMaster():
    """Svn管理员
    描述
       可以审批普通用户的权限，可以读取和操作所有的权限
    成员变量
       name
       passwd
       auth
    方法
       初始化

       从文件导入权限

       增组
       删组
       组加ID
       组减ID
       组加权限
       组减权限

       增ID
       删ID
       ID加权限
       ID减权限
       ID改密码

       查ID权限
       查组权限

       查看申请清单
       批准申请

       修改自己的密码

    """
    def __init__(self,name="admin",passwd="admin",passwdfile=None,authfile=None):
        self.name = name
        self.passwd = passwd
        self.auth = svnauth.SvnAuth(passwdfile,authfile)

    def import_auth(self,passwdfile,authfile):
        self.auth.refresh(passwdfile,authfile)

    def group_create(self,name):
        self.auth.group_create(name)

    def group_destroy(self,name):
        self.auth.group_destroy()

    def group_add_id(self,group_name,id_name):
        self.auth.group_add_id(group_name,id_name)

    def group_del_id(self,group_name,id_name):
        self.auth.group_del_id(group_name,id_name)

    def group_add_priv(self,name,dir,mode="rw"):
        self.auth.group_add_priv(name,dir,mode)

    def group_del_priv(self,name,dir):
        self.auth.group_del_priv(name,dir)

    def id_add(self,name,passwd):
        self.auth.id_add(name,passwd)

    def id_del(self,name):
        self.auth.id_del(name)

    def id_add_priv(self,name,dir,mode="rw"):
        self.auth.id_add_priv(name,dir,mode)

    def id_del_priv(self,name,dir):
        self.auth.id_del_priv(name,dir)

    def id_set_pass(self,name,passwd):
        self.auth.set_pass(name,passwd)

    def get_id_priv(self,name):
        return self.get_id_priv(name)

    def get_group_priv(self,name):
        return self.get_group_priv(name)

    def get_request_list(self):
        pass
    def permit_request(self,request):
        """
        参数
            请求  类型字典
            TYPE
            OP
            NAME
            DIR
            MODE
        """
        mtype = request["type"]
        name = request['name']
        op   = request['op']
        dir  = request['dir']
        mode = request['mode']
        if cmp(mtype,'group') == 0:
            if cmp(op,'add') == 0:
                self.group_add_priv(name,dir,mode)
            elif cmp(op,'del') == 0:
                self.group_del_priv(name,dir)
            else:
                pass
        elif cmp(mtype,'id') == 0:
            if cmp(op,'add') == 0:
                self.id_add_priv(name,dir,mode)
            elif cmp(op,'del') == 0:
                self.id_del_priv(name,dir)
            else:
                pass
        else:
            pass


