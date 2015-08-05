
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

       从文件导入,并初始化
       从内存写入文件

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

       打印ID权限
       打印组权限

       查看申请清单
       批准申请

       修改自己的密码

    """
    def __init__(self,name="admin",passwd="admin",passwdfile=None,authfile=None):
        self.name       = name
        self.passwd     = passwd
        self.authfile   = authfile
        self.passwdfile = passwdfile
        self.auth       = svnauth.SvnAuth(passwdfile,authfile)

    def read_ini(self):
        import svnconfig
        config_dict     =   svnconfig.read_config_to_dict()
        self.authfile   =   config_dict['local_authfile']
        self.passwdfile =   config_dict['local_passwdfile']

    def read(self,passwdfile=None,authfile=None):
        """
            从文件读取权限，参数为空
            则读取ini 文件指定的passwdfile,authfile文件

        """

        if passwdfile is None or authfile is None:
            self.read_ini()
        else:
            self.passwdfile = passwdfile
            self.authfile   = authfile

        self.auth.refresh(self.passwdfile,self.authfile)

    def write(self,passwdfile=None,authfile=None):

        if passwdfile is None or authfile is None:
            self.read_ini()
        else:
            self.passwdfile = passwdfile
            self.authfile   = authfile

        self.auth.write_passwdfile(self.passwdfile)
        self.auth.write_authfile(self.authfile)

    def clear(self):
        self.auth.refresh()

    def backup():
        pass

    def group_create(self,name):
        self.auth.group_create(name)

    def group_destroy(self,name):
        self.auth.group_destroy(name)

    def group_add_id(self,group_name,id_name):
        self.auth.group_add_id(group_name,id_name)

    def group_del_id(self,group_name,id_name):
        self.auth.group_del_id(group_name,id_name)

    def group_add_priv(self,name,dir,mode="rw"):
        self.auth.group_add_priv(name,dir,mode)

    def group_del_priv(self,name,dir):
        self.auth.group_del_priv(name,dir)

    def id_add(self,name,passwd=None):
        passwd=name
        self.auth.id_add(name,passwd)

    def id_del(self,name):
        self.auth.id_del(name)

    def id_add_priv(self,name,dir,mode="rw"):
        self.auth.id_add_priv(name,dir,mode)

    def id_del_priv(self,name,dir):
        self.auth.id_del_priv(name,dir)

    def id_set_pass(self,name,passwd):
        self.auth.id_set_pass(name,passwd)

    def get_id_priv(self,name):
        return self.get_id_priv(name)

    def get_group_priv(self,name):
        return self.get_group_priv(name)

    def display_group_priv(self,name):
        self.auth.display_group_priv(name)

    def display_id_priv(self,name):
        self.auth.display_id_priv(name)

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
        mtype      = request["type"]
        group_name = request['group_name']
        id_name    = request['id_name']
        op         = request['op']
        dir        = request['dir']
        mode       = request['mode']
        passwd     = request['passwd']

        if cmp(mtype,'group') == 0:
            if cmp(op,'add') == 0:
                self.group_add_priv(group_name,dir,mode)
            elif cmp(op,'del') == 0:
                self.group_del_priv(group_name,dir)
            elif cmp(op,'add_id') == 0:
                self.group_add_id(group_name,id_name)
            elif cmp(op,'del_id') == 0:
                self.group_del_id(group_name,id_name)
            elif cmp(op,'create') == 0:
                self.group_create(group_name)
            elif cmp(op,'destroy') == 0:
                self.group_destroy(group_name)
            else:
                svn_logger.warn("op(%s) 不存在" % op)
                pass
        elif cmp(mtype,'id') == 0:
            if cmp(op,'add') == 0:
                self.id_add_priv(id_name,dir,mode)
            elif cmp(op,'del') == 0:
                self.id_del_priv(id_name,dir)
            elif cmp(op,'create') == 0:
                self.id_add(id_name)
            elif cmp(op,'destory') == 0:
                self.id_del(id_name)
            elif cmp(op,'change') == 0:
                self.id_set_pass(id_name,passwd)
            else:
                svn_logger.warn("op(%s) 不存在" % op)
                pass
        else:
            svn_logger.warn("type(%s) 不存在" % type)
            pass


