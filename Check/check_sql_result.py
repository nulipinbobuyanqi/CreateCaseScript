# coding:utf-8
# @Author: wang_cong
from Check.sql_compare import sql_compare
from Utils.operation_log import initLogger

logger = initLogger(__file__)


def check_sql_result(check_info, acture_result):
    """
    校验SQL请求，返回校验成功或者失败
    :param check_info: SQL校验信息
    :param acture_result: SQL请求得到的实际返回值
    :return: 返回校验成功或者失败
    """
    try:
        # 因为有多条校验信息，必须每条校验信息，都是PASS ,才能算PASS；有一个不是FAIL,那就FAIL
        # 因此，决定将每条校验结果放入一个list里面
        check_res = []
        # 对校验信息，进行判断
        if check_info is None:
            logger.info("无校验信息")
            flag = True
            check_res.append(flag)
        else:
            logger.info("有校验信息")
            logger.info(check_info)
            # 遍历每一个校验信息
            for n in range(len(check_info)):
                logger.info("当前正在遍历第{}个校验信息".format(n + 1))
                every_check_info = check_info[n]
                logger.info("=====开始SQL校验=====")
                # 获取SQL校验的各项信息
                extract_path = every_check_info["extract_path"]
                if extract_path is None or extract_path == "":
                    logger.error("提取路径为空，无法进行SQL校验！")
                operator = every_check_info["operator"]
                if operator is not None or operator != "":
                    if operator not in ["==", ">", "<", "<=", "!=", "in", "not in", "is None", "is not None"]:
                        logger.error("当前操作器是：{} 不在")
                else:
                    logger.error("操作器为空，无法进行SQL校验！")
                expected_value = every_check_info["expected_value"]
                if expected_value is None or expected_value == "":
                    logger.error("预期结果为空，无法进行SQL校验！")
                if not isinstance(acture_result, tuple):
                    logger.error("SQL实际返回值的数据类型时：{} ，不是tuple，无法进行SQL校验".format(type(acture_result)))
                if acture_result == ():
                    logger.error("SQL实际查询结果为空，无法进行SQL校验！")
                # 根据校验信息的提取方式类型，分别进行判断
                if extract_path.startswith("$"):
                    flag = sql_compare(acture_result, operator, expected_value, extract_path)
                    check_res.append(flag)
                else:
                    logger.error("当前的提取路径是：{} ，不正确，无法进行SQL校验！提取路径必须以$符号开头！".format(extract_path))
        # 接下来分析，校验结果列表中，是否有False
        if len(check_res) == 0:
            logger.info("说明没得到任何校验结果")
            logger.info("=====结束SQL校验=====")
            return False
        else:
            if False in check_res:
                logger.info("=====结束SQL校验=====")
                return False
            else:
                logger.info("=====结束SQL校验=====")
                return True
    except Exception as e:
        logger.error("校验SQL失败！报错信息是：{}".format(e))
