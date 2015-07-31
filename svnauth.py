
# -*- coding:UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from svngroup import *
from svnid import *
from svnlog import svn_logger
import re


class SvnAuth(object):
    """SVN权限管理器

    成员变量：
        grouplist 组字典 键为组名 => group 对象
        idlist    ID字典     ID名 =>  ID 对象
    方法：
        权限初始化
        读auth文件
        读passwd文件

        创建组
        组增加成员
        组删除成员
        组增加权限
        组删除权限
        删除组

        增加ID
        删除ID
        ID增加权限
        ID删除权限
        ID修改密码

        写auth文件
        写passwd文件

        查询某个组的权限
        查询某个ID的权限
        查询某个目录的权限

        打印某个组的权限
        打印某个ID的权限

    """

    _instance=None
    def __new__(cls,*args,**kwargs):
        if not cls._instance:
           svn_logger.debug("SvnAuth function __new__ once")
           #cls._instance = super(SvnAuth, cls).__new__(cls, *args, **kwargs)
           cls._instance = super(SvnAuth, cls).__new__(cls)
        return cls._instance

    def __init__(self,passwdfile=None,authfile=None):
        self.x = 1
        self.id_dict={}
        self.group_dict = {}
        svn_logger.info("create svnauth")
        if passwdfile:
            self.read_passwdfile(passwdfile)
        if  authfile:
            self.read_authfile(authfile)

    def refresh(self,passwdfile=None,authfile=None):
        self.id_dict={}
        self.group_dict = {}
        svn_logger.info("refresh svnauth from file(%s),(%s)" % (passwdfile,authfile))
        if passwdfile:
            self.read_passwdfile(passwdfile)
        else:
            svn_logger.debug("passwdfile is None ")
        if authfile:
            self.read_authfile(authfile)
        else:
            svn_logger.debug("authfile is None ")


    def read_passwdfile(self,passwdfile):
        svn_logger.info("read passwd from file(%s)" % passwdfile)
        try:
            passfh = open(passwdfile,"r")
            re1 = r"^(\w+)\s*=\s*(\w+)"
            pattern = re.compile(re1)

            for line in passfh:
                match = pattern.match(line)
                if match:
                    name   = match.group(1)
                    passwd = match.group(2)
                    self.id_add(name,passwd)
                else:
                    svn_logger.debug("line(%s) did not match id=passwd  ;ignore this line" %  line )
        except IOError:
            svn_logger.error("The file(%s) do not exist" % passwdfile)
            exit()
        finally:
            passfh.close()


    def read_authfile(self,authfile):
        svn_logger.info("read line from file")
        try:
            authfh = open(authfile,'r')#,encoding='utf-8')

            group_flag_re=r"\[groups\]"
            pattern_group_flag=re.compile(group_flag_re)
            #组名 和成员列表
            group_userlist_re=r"^(\w+)\s*=\s*(.*)$"
            pattern_userlist=re.compile(group_userlist_re)
            #权限路径
            path_re = r"^\[(\w+:)?(/\S*)\]"
            pattern_path=re.compile(path_re)
            #成员名称和权限
            user_priv_re=r"^(\w+)\s*=\s*(\w+)"
            pattern_user_priv=re.compile(user_priv_re)
            #组名称和权限
            group_priv_re=r"^@(\w+)\s*=\s*(\w+)"
            pattern_group_priv=re.compile(group_priv_re)

            tmp_status = 0
            tmp_dir    = ''
            # 状态0  为初始状态
            # 状态1   遇到[group]标志之后
            # 状态2   遇到[/dir] 目录之后 ，并记录目录名称
            for line in authfh:
                if tmp_status == 0:
                    match = pattern_group_flag.match(line)
                    if match:
                        tmp_status = 1
                        svn_logger.debug("match group flag")
                elif tmp_status == 1:
                    match = pattern_userlist.match(line)
                    if match:
                        #匹配到
                        svn_logger.debug("match userlist in group")

                        group_name = match.group(1)
                        self.group_create(group_name)
                        userlist_string = match.group(2)
                        userlist_string = userlist_string.replace(' ','')
                        userlist = userlist_string.split(',')
                        svn_logger.debug("group(%s) will add userlist(%s)" % (group_name,userlist))
                        for id_name in userlist:
                            if id_name == "":
                                continue
                            self.group_add_id(group_name,id_name)

                    elif pattern_path.match(line):
                        #匹配到目录

                        match = pattern_path.match(line)
                        if  match.group(1):
                            tmp_dir =  match.group(1) + match.group(2)
                        else:
                            tmp_dir = match.group(2)
                        svn_logger.debug("match diretory（%s）" % tmp_dir)
                        tmp_status = 2
                    else:
                        pass
                elif tmp_status == 2:
                    if pattern_group_priv.match(line):
                        svn_logger.debug("match group priv")
                        match = pattern_group_priv.match(line)
                        group_name = match.group(1)
                        mode = match.group(2)
                        self.group_add_priv(group_name,tmp_dir,mode)
                    elif pattern_user_priv.match(line):
                        svn_logger.debug("match user priv")
                        match = pattern_user_priv.match(line)
                        name = match.group(1)
                        mode = match.group(2)
                       # print("(%s) add (%s)" % (name,tmp_dir))
                        self.id_add_priv(name,tmp_dir,mode)
                       # print("(%s) add (%s)" % (name,tmp_dir))
                    elif pattern_path.match(line):
                        #匹配到目录
                        match = pattern_path.match(line)
                        if  match.group(1):
                            tmp_dir =  match.group(1) + match.group(2)
                        else:
                            tmp_dir = match.group(2)
                        svn_logger.debug("match diretory（%s）" % tmp_dir)
                    else:
                        pass
        except IOError:
            svn_logger.error("The file(%s) do not exist" % authfile)
            exit()

        authfh.close()
        return


    #组字典操作
    def group_create(self,name):
        if name not in self.group_dict.keys():
            self.group_dict[name] = SvnGroup(name)
            svn_logger.info("create group(%s)",name)
        else:
            svn_logger.warn("Group %s  exist , don't create again" % name)

    def group_destroy(self,name):
        svn_logger.info("destory group(%s)",name)
        del self.group_dict[name]

    def group_add_id(self,group_name,id_name):
        if group_name not  in self.group_dict.keys():
            svn_logger.warn("Group (%s) not exist" % group_name)
            return
        if id_name not  in self.id_dict.keys():
            svn_logger.warn("Id (%s) not exist" % id_name)
            return
        svn_logger.info("Group(%s) add Id(%s)" % (group_name,id_name))
        self.group_dict[group_name].add_id(self.id_dict[id_name])

    def group_del_id(self,group_name,id_name):
        if group_name not  in self.group_dict.keys():
            svn_logger.warn("Group (%s) not exist" % group_name)
            return
        if id_name not  in self.id_dict.keys():
            svn_logger.warn("Id (%s) not exist" % id_name)
            return
        svn_logger.info("Group(%s) del Id(%s)" % (group_name,id_name))
        self.group_dict[group_name].del_id(self.id_dict[id_name])

    def group_add_priv(self,name,dir,mode="rw"):
        if name  in self.group_dict.keys():
            svn_logger.info("Group(%s) add mode(%s) priv  on dir (%s) " % (name,mode,dir))
            self.group_dict[name].add_privilege(dir,mode)
        else:
            svn_logger.warn("Group %s not exist，can not add priv" % name)
            return False

    def group_del_priv(self,name,dir):
        if name  in self.group_dict.keys():
            svn_logger.info("Group(%s) del  priv  on dir (%s) " % (name,dir))
            self.group_dict[name].del_privilege(dir)
        else:
            svn_logger.warn("Group %s not exist，can not del priv" % name)
            return False

    #id列表操作
    def id_add(self,name,passwd):
        if  name not in  self.id_dict.keys():
            svn_logger.info("Id(%s) add in  idlist of svnauth " % (name))
            self.id_dict[name] =SvnId(name,passwd)
        else:
            svn_logger.warn("Id %s have been exist " % name)

    def id_del(self,name):
        svn_logger.info("Id(%s) deleted in idlist of svnauth" % name)
        for group_name in self.group_dict.keys():
            self.group_dict[group_name].del_id(self.id_dict[name])
        del self.id_dict[name]

    def id_add_priv(self,name,dir,mode="rw"):
        if name in self.id_dict.keys():
            svn_logger.info("Id(%s) add priv(%s) mode(%s)" % (name,dir,mode))
            self.id_dict[name].add_privilege(dir,mode)
        else:
            svn_logger.warn("ID %s not exist,can not add priv" % name)

    def id_del_priv(self,name,dir):
        svn_logger.info("ID(%s) will be deleted priv(%s)" % (name,dir))
        if name in self.id_dict.keys():
            self.id_dict[name].del_privilege(dir)
        else:
            print("ID %s not exist,can not add priv" % name)

    def id_set_pass(self,name,passwd):
        svn_logger.info("Id(%s) will be changed password" % passwd)
        self.id_dict[name].set_pass(passwd)

    def write_passwdfile(self,passwdfile):
        svn_logger.info("write svnauth into passwd file(%s)" % passwdfile)
        try:
            passfh = open(passwdfile,'w')
            passfh.write("[users]\n")
            for id_name in sorted(self.id_dict.keys()):
                id = self.id_dict[id_name]
                passfh.write("%s = %s\n" % (id.name, id.passwd))
            passfh.close()
        except IOError:
            svn_logger.error("can not open (%s)" % passwdfile)
        finally:
            passfh.close()

    def write_authfile(self,authfile):
        svn_logger.info("write svnauth into authfile file(%s)" % authfile)
        try:
            authfh = open(authfile,"w")
               #print group and user list
            authfh.write("[group]\n")
            for group_name in sorted(self.group_dict.keys()):
                group = self.group_dict[group_name]
                userlist = group.get_idlist_as_string()
                authfh.write("%-20s = %s\n" % (group_name,userlist) )
            authfh.write("\n")
            authfh.write ("##########group privilege start #############\n")
            for group_name in sorted(self.group_dict.keys()):
                group = self.group_dict[group_name]
                for dir,mode in group.privilege.items():
                    authfh.write("[%s]\n" % dir )
                    authfh.write("@%s = %s\n" %(group_name,mode))
                authfh.write("\n")

            authfh.write ("##########group privilege  end #############\n")
            authfh.write("\n")
            authfh.write ("##########user privilege  start #############\n")
            for id_name,id in self.id_dict.items():
                #authfh.write ("##########%s #############\n" % id_name)
                for dir,mode in id.privilege.items():
                    authfh.write("[%s]\n" % dir)
                    authfh.write("%s = %s\n" %(id_name,mode))
                if id.privilege.keys():
                    authfh.write("\n")
            authfh.write ("##########user privilege  end #############\n")
        except IOError:
            svn_logger("can not open (%s)" % authfile)
        finally:
            authfh.close()

    def get_id_priv(self,name):
        priv_dict={}
        if name  in sorted(self.id_dict.keys()):
            svn_logger.info("Id(%s) get priv " % name )
            priv_dict = self.id_dict[name].get_privilege()
            for group in self.group_dict.values():
                if group.has_id(self.id_dict[name]):
                    svn_logger.debug("group(%s) contain priv  for id(%s)" %( group.name, name) )
                    priv_dict.update(group.privilege)
            return priv_dict
        else:
            svn_logger.warn("Id %s not exist" % name)
            return None

    def get_group_priv(self,name):
        if name  in self.group_dict.keys():
            svn_logger.info("Group(%s) get priv " % name )
            return self.group_dict[name]
        else:
            svn_logger.warn("Group %s not exist" % name)
            return None

    def get_dir_priv(self,dir):
        pass

    def display_id_priv(self,name):
        print ("#####################################")
        priv_dict = self.get_id_priv(name)
        if priv_dict is None:
            return
        print("ID: %s" % name)
        print("DIR:")
        for dir,mode in priv_dict.items():
            print("%-3s %s" % (mode,dir))
        print ("#####################################\n")

    def display_group_priv(self,group_name):
        print ("#####################################\n")
        group = self.get_group_priv(group_name)
        if group is None:
            return
        group.display()
        print ("#####################################\n")

