
# -*- coding: UTF-8 -*-

import svnmanager.svnsftp as svnsftp
import svnmanager.svnmaster as svn

"""
可以先从服务器，通过sftp下载权限文件到指定目录下
配置文件为/etc/svn.ini
[svn_server]
hostname = 10.0.100.110
port = 22
username = root
password = 111111
passwdfile = /sdb/svnlib/test/passwd
authfile = /sdb/svnlib/test/authz
[local]
passwdfile = /tmp/passwd
authfile   = /tmp/authz
"""
svnsftp.getall()

#初始化管理员
me = svn.SvnMaster(name="admin",passwd="admin")

# 有两种svn权限导入方式
# 1. 参数指定文件路径
me.read(passwdfile="./file/passwd",authfile="./file/authz")

me.clear()

# 2. ini 指定文件路径
# /etc/svn.ini中
# [local]
# passwdfile = /root/file/passwd
# authfile   = /root/file/authz
#
me.read()

# 对普通用户有以下五种操作
# create  :创建
# destroy :删除
# add     :增加目录权限
# del     :删除目录权限
# change  :修改用户密码
me.display_id_priv("yangkun")
request={ 'type':'id','op':'destroy', 'group_name':None, 'id_name':"yangkun", 'dir':'/root', 'mode':'rw', 'passwd':'111111', }
me.permit_request(request)
request={ 'type':'id','op':'create', 'group_name':None, 'id_name':"yangkun", 'dir':'/root', 'mode':'rw', 'passwd':'111111', }
me.permit_request(request)
request={ 'type':'id','op':'add', 'group_name':None, 'id_name':"yangkun", 'dir':'/root', 'mode':'rw', 'passwd':'111111', }
me.permit_request(request)
request={ 'type':'id','op':'del', 'group_name':None, 'id_name':"yangkun", 'dir':'/root', 'mode':'rw', 'passwd':'111111', }
me.permit_request(request)

for i in range(10):
    id_name = "test" + str(i)
    request={ 'type':'id','op':'create', 'group_name':None, 'id_name':id_name, 'dir':'', 'mode':'', 'passwd':'111111', }
    me.permit_request(request)
request={ 'type':'id','op':'change', 'group_name':None, 'id_name':"yangkun", 'dir':'', 'mode':'', 'passwd':'123456', }
me.permit_request(request)
me.display_id_priv("yangkun")

# 对用户组有以下六种操作
# create  :创建
# destroy :删除
# add     :增加目录权限
# del     :删除目录权限
# add_id  :修改用户密码
# del_id  :修改用户密码
group_name="Host_Group"
request={ 'type':'group','op':'destroy', 'group_name':"Host_Group",  'id_name':"", 'dir':'', 'mode':'', 'passwd':'', }
me.permit_request(request)
me.display_group_priv(group_name)

request={ 'type':'group','op':'create',  'group_name':"Host_Group",  'id_name':"", 'dir':'', 'mode':'', 'passwd':'', }
me.permit_request(request)
me.display_group_priv(group_name)

for i in range(10):
    id_name = "test" + str(i)
    request={ 'type':'group','op':'add_id',  'group_name':"Host_Group",  'id_name':id_name, 'dir':'', 'mode':'', 'passwd':'', }
    me.permit_request(request)
me.display_group_priv(group_name)

for i in range(9,5,-1):
    id_name = "test" + str(i)
    request={ 'type':'group','op':'del_id',  'group_name':"Host_Group",  'id_name':id_name, 'dir':'', 'mode':'', 'passwd':'', }
    me.permit_request(request)
me.display_group_priv(group_name)

for i in range(10):
    dir_name = "/dir" + str(i)
    request={ 'type':'group','op':'add', 'group_name':"Host_Group", 'id_name':"", 'dir':dir_name, 'mode':'rw', 'passwd':'', }
    me.permit_request(request)
me.display_group_priv(group_name)

for i in range(9,5,-1):
    dir_name = "/dir" + str(i)
    request={ 'type':'group','op':'del', 'group_name':"Host_Group", 'id_name':"", 'dir':dir_name, 'mode':'rw', 'passwd':'', }

    me.permit_request(request)
me.display_group_priv(group_name)


# 有两种方法，将svn 权限导出 到文件
# 1. 参数指定文件路径
me.write(passwdfile="./passwd",authfile="./authz")

# 2. ini 指定文件路径
# /etc/svn.ini中
# [local]
# passwdfile = /root/file/passwd
# authfile   = /root/file/authz
#
#me.write()

# 将本地保存的passwd和authz 通过sftp发送服务器
#svnsftp.sendall()



