
# -*- coding:UTF-8 -*-
import logging

def svn_log():
    #logger_name="svn_mgr_main"
    logger_filename="/var/log/svn.log"

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
   # formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(filename)s[line:%(lineno)d]: %(message)s',
   #                               "%Y-%m-%d %H:%M:%S")
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - [%(module)s  %(funcName)s() line:%(lineno)d ]: %(message)s',
                                  "%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(logger_filename,encoding = "UTF-8")
    #设置文件写入的级别
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    #设置显示的级别
    ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

svn_logger=svn_log()
