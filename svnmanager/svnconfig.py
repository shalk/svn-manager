
# -*- coding:UTF-8 -*-
from svnlog import svn_logger

import ConfigParser
#
#  读写svn ini 文件
#
def read_config_to_dict(ini='/etc/svn.ini'):
    """
    从ini文件里读取svn_server字段
    :param ini:
    :return:svn_sftp_dict
    """
    cf = ConfigParser.ConfigParser()
    svn_sftp_dict={}
    field="svn_server"
    local_field="local"
    try:
        svn_logger.debug("read svn ini file(%s) " % ini )
        cf.read(ini)
        svn_sftp_dict['hostname'] = cf.get(field,'hostname')
        svn_sftp_dict['port'] = cf.getint(field,'port')
        svn_sftp_dict['username'] = cf.get(field,'username')
        svn_sftp_dict['password'] = cf.get(field,'password')
        svn_sftp_dict['passwdfile'] = cf.get(field,'passwdfile')
        svn_sftp_dict['authfile'] = cf.get(field,'authfile')
        svn_sftp_dict['local_passwdfile'] = cf.get(local_field,'passwdfile')
        svn_sftp_dict['local_authfile'] = cf.get(local_field,'authfile')
    except IOError as e:
        svn_logger.error("open svn ini file (%s) failed" % ini)
    return svn_sftp_dict


