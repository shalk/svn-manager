
# -*- coding:UTF-8 -*-
from svnlog import svn_logger
import svnconfig
import paramiko



def get(hostname=None,port=22,username='root',password='111111',config_dict=None,remote_file=None,local_file=None):
    """
    从服务器上下载文件
    支持参数，支持字典
    """
    if hostname is None:
        hostname = config_dict['hostname']
        port     = config_dict['port']
        username = config_dict['username']
        password = config_dict['password']

    try:
        svn_logger.debug("connect to %s:%s " % (hostname,port))
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)

        sftp =paramiko.SFTPClient.from_transport(t)

        sftp.get(remote_file,local_file)
        svn_logger.debug("get file from  remote(%s) to local (%s) " % (remote_file,local_file))
        t.close();
    except Exception, e:
        svn_logger.error("connect to %s:%s failed " % (hostname,port))
        import traceback
        traceback.print_exc()
        try:
            t.close()
        except:
            pass

def send(hostname=None,port=22,username='root',password='111111',config_dict=None,local_file=None,remote_file=None):
    """
    上传文件到服务器
    """
    if hostname is None:
        hostname = config_dict['hostname']
        port     = config_dict['port']
        username = config_dict['username']
        password = config_dict['password']

    try:
        svn_logger.debug("connect to %s:%s " % (hostname,port))
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)

        sftp =paramiko.SFTPClient.from_transport(t)

        sftp.put(local_file,remote_file)
        svn_logger.debug("send file from  local(%s) to remote(%s) " % (local_file,remote_file))
        t.close();
    except Exception, e:
        svn_logger.error("connect to %s:%s failed " % (hostname,port))
        import traceback
        traceback.print_exc()
        try:
            t.close()
        except:
            pass

def get_auth():
    config_dict = svnconfig.read_config_to_dict()

    get(config_dict=config_dict,remote_file=config_dict['authfile'],local_file=config_dict['local_authfile'])

def get_passwd():
    config_dict = svnconfig.read_config_to_dict()

    get(config_dict=config_dict,remote_file=config_dict['passwdfile'],local_file=config_dict['local_passwdfile'])

def send_auth():
    config_dict = svnconfig.read_config_to_dict()

    send(config_dict=config_dict,remote_file=config_dict['authfile'],local_file=config_dict['local_authfile'])


def send_passwd():
    config_dict = svnconfig.read_config_to_dict()

    send(config_dict=config_dict,remote_file=config_dict['passwdfile'],local_file=config_dict['local_passwdfile'])

def getall():
    config_dict = svnconfig.read_config_to_dict()


    get(config_dict=config_dict,remote_file=config_dict['authfile'],local_file=config_dict['local_authfile'])
    get(config_dict=config_dict,remote_file=config_dict['passwdfile'],local_file=config_dict['local_passwdfile'])

def sendall():
    config_dict = svnconfig.read_config_to_dict()


    send(config_dict=config_dict,remote_file=config_dict['authfile'],local_file=config_dict['local_authfile'])
    send(config_dict=config_dict,remote_file=config_dict['passwdfile'],local_file=config_dict['local_passwdfile'])

