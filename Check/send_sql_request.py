# coding:utf-8
# @Author: wang_cong
from Utils.OperationMysql import OperationMysql
from Utils.operation_log import initLogger

logger = initLogger(__file__)


def send_sql_request(run_env, db_env_data, database_type, sql_type, sql_content):
    """
    连接数据库，执行SQL语句，得到查询结果
    :param run_env: 运行环境
    :param db_env_data: db_env.yml文件中的数据库配置信息
    :param database_type: 数据库类型
    :param sql_type: SQL语句类型，"select", "insert", "update", "delete"
    :param sql_content: SQL语句内容
    :return: 若是查询语句，则返回查询结果；否则，不返回任何内容
    """
    try:
        print(run_env)
        print(db_env_data)
        print("database_type,", database_type)
        print(sql_type)
        print(sql_content)
        db_data = db_env_data[run_env]
        # 开始匹配数据库配置信息
        for db_data in db_data:
            if db_data["database_type"].lower() == database_type.lower() == "mysql":
                print("这是mysql数据库")
                database_host = db_data["mysql_ip"]
                database_port = int(db_data["mysql_port"])
                database_user = db_data["mysql_user"]
                database_password = db_data["mysql_password"]
                database_name = db_data["mysql_db_name"]
                op_mysql = OperationMysql(database_host, database_port, database_user, database_password, database_name)
                # 根据SQL语句类型，执行SQL
                if sql_type.lower() == "select":
                    logger.debug("表示要执行的SQL是select类型的")
                    sql_res = op_mysql.select_all_res(sql_content)
                    return sql_res
                elif sql_type.lower() in ["insert", "update", "delete"]:
                    logger.debug("表示要执行的SQL是'insert', 'update', 'delete'类型的")
                    op_mysql.insert_update_delete_sql(sql_content)
                else:
                    logger.error("当前SQL语句的类型是：{} ， 本套代码暂不支持！".format(sql_type))
            elif db_data["database_type"] == database_type.lower() == "mongodb":
                logger.info("这是mongodb数据库")
                # 还缺少这部分的代码
                logger.error("当前的数据库类型是：{} ，本套代码暂不支持！".format(database_type))
            else:
                logger.error("当前的数据库类型是：{} ，本套代码暂不支持！".format(database_type))
    except Exception as e:
        logger.error("发起SQL请求失败！报错信息是：{}".format(e))
