# coding:utf-8
import pymysql
from Utils.operation_log import initLogger

logger = initLogger(__file__)


class OperationMysql:
    def __init__(self, host, port, user, password, database):
        """
        初始化
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        if self.host is None or self.user is None or self.password is None or self.database is None:
            logger.error("数据库连接失败， host , user , password 和 database 的值，存在为空的情况！")
        else:
            # 通过connect()创建连接
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.database)
            # 通过cursor()创建游标对象
            self.cur = self.conn.cursor()

    def __del__(self):
        """
        释放数据库连接并关闭
        :return:
        """
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_one_res(self, sql):
        """
        获取一个查询结果数据
        :param sql:
        :return: 得到一行tuple返回值
        """
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        res = self.cur.fetchone()
        logger.debug("根据SQL={} ，查询到的一个结果是：{}".format(sql, res))
        return res

    def select_all_res(self, sql):
        """
        获取所有查询结果数据
        :param sql:
        :return: 得到多个tuple组合成的tuple组返回值
        """
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        res = self.cur.fetchall()
        logger.debug("根据SQL={} ，查询到的所有结果是：{}".format(sql, res))
        logger.info("执行查询SQL语句，成功！ ")
        return res

    def insert_update_delete_sql(self, sql):
        """
        获取新增、修改和删除的结果数据
        :param sql:
        :return:
        """
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
            logger.info("执行新增、修改或删除的SQL语句，成功！ ")
        except Exception as e:
            print("执行新增、修改或删除的SQL语句，出现错误！ 报错信息为：{} ".format(e))
            # 回滚所有更改
            self.conn.rollback()

    def get_table_struct(self, table_name):
        """
        获取某个表的结构
        :param table_name:
        :return:
        """
        key_list = []
        # 查询表结构的SQL语句，结构为：desc database_name.table_name
        sql = "desc %s.%s ;" % (self.database, table_name)
        result = self.select_all_res(sql)
        for i in result:
            key_list.append(i[0])
        logger.info("表结构得到的列名，组成的list结果为：-------",key_list)
        return key_list
