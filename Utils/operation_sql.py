# coding:utf-8
# @Author: wang_cong
import os
from Utils.operation_log import initLogger

logger = initLogger(__file__)


def get_sql_data(sql_path, sql_file_name):
    """
    读取sql文件，返回一个dict类型的数据
    :param sql_path: sql文件所在路径，不含最后一个"/"符号
    :param sql_file_name: sql文件名称，不含".sql"后缀名
    :return: 返回dict类型的数据
    """
    sql_file = sql_path + "/" + sql_file_name + ".sql"
    if not os.path.exists(sql_file):
        logger.error("{}.sql文件，不存在！".format(sql_file_name))
    with open(sql_file, "r", encoding="utf-8") as f:
        list_sql_data = f.readlines()
    return list_sql_data
