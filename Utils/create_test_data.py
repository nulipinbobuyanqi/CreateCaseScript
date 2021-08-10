# coding:utf-8
# @Author: wang_cong
import os
from Utils.operation_dir import create_every_path_dirs


def create_test_data(unit_case_path, new, data_path):
    """

    :param unit_case_path:
    :param new:
    :param data_path:
    :return:
    """
    # 注意：根据测试用例yaml文件的存放目录，判断有几个yaml文件，即表示有几个测试用例的数据要生成，便需要创建几个数据文件
    # SQL数据文件的命名规则是：test_sql_1.sql
    for root, dirs, files in os.walk(unit_case_path):
        for dir in dirs:
            dd = os.path.join(root, dir)
            ll = os.listdir(dd)
            for data in ll:
                if data.endswith(".yml"):
                    yml_file_name = data.split(".yml")[0]
                    if "_" in yml_file_name:
                        number = yml_file_name.split("_")[-1]
                    else:
                        number = "1"
                    ff = dd.split(new)[-1].replace("\\", "/")
                    create_every_path_dirs(data_path, ff)
                    # 基础的SQL文件路径
                    sql_file_path = data_path + ff
                    # 构造初始化SQL文件名称
                    init_sql_file_name = "test_init_sql_" + number + ".sql"
                    # 完整的初始化SQL文件路径名称
                    init_sql_file = sql_file_path.replace("\\", "/") + "/" + init_sql_file_name
                    # 构造清除SQL文件名称
                    clear_sql_file_name = "test_clear_sql_" + number + ".sql"
                    # 完整的清除SQL文件路径名称
                    clear_sql_file = sql_file_path.replace("\\", "/") + "/" + clear_sql_file_name
                    # 准备生成初始化SQL文件
                    with open(init_sql_file, 'w', encoding='utf-8') as sql_init__f:
                        content = """# 注意：本SQL文件的前四行，请勿删除，否则导致SQL文件执行失败！
# 注意：本套代码，暂时仅支持将每条SQL语句，写在一行里，并以英文分号;相隔开。以及使用enter键换行！
# 注意：请从第五行开始，写SQL语句，本套代码支持："select、insert、update、delete"这四种类型的语句。
# 注意：请将第四行的内容，按照此格式要求书写。#（一个空格）数据库类型名称全称小写，举例：# mysql或者# mongodb 。默认是：# mysql
# mysql
"""
                        sql_init__f.write(content)
                    with open(clear_sql_file, 'w', encoding='utf-8') as sql_clear__f:
                        content = """# 注意：本SQL文件的前四行，请勿删除，否则导致SQL文件执行失败！
# 注意：本套代码，暂时仅支持将每条SQL语句，写在一行里，并以英文分号;相隔开。以及使用enter键换行！
# 注意：请从第五行开始，写SQL语句，本套代码支持："select、insert、update、delete"这四种类型的语句。
# 注意：请将第四行的内容，按照此格式要求书写。#（一个空格）数据库类型名称全称小写，举例：# mysql或者# mongodb 。默认是：# mysql
# mysql
"""
                        sql_clear__f.write(content)
