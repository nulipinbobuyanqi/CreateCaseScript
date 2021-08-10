# coding:utf-8
# @Author: wang_cong
from Check.api_compare import api_compare
from Utils.operation_log import initLogger

logger = initLogger(__file__)


def check_api_result(check_info, acture_result):
    """
    校验接口请求，返回校验成功或者失败
    :param check_info: 接口校验信息
    :param acture_result: 接口请求得到的实际返回值
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
            # 遍历每一个校验信息
            for n in range(len(check_info)):
                logger.info("当前正在遍历第{}个校验信息".format(n + 1))
                every_check_info = check_info[n]
                logger.info("=====开始接口校验=====")
                # 获取接口校验的各项信息
                extract_type = every_check_info["extract_type"]
                if extract_type is not None or extract_type != "":
                    if extract_type.lower() not in ["interface_headers", "cookie", "response_code", "response_content"]:
                        logger.error("当前的提取方式是：{} ，本套代码暂不支持！无法进行接口校验！".format(extract_type))
                else:
                    logger.error("提取方式为空，无法进行接口校验！")
                extract_path = every_check_info["extract_path"]
                if extract_path is None or extract_path == "":
                    logger.error("提取路径为空，无法进行接口校验！")
                operator = every_check_info["operator"]
                if operator is not None or operator != "":
                    if operator not in ["==", ">", "<", "<=", "!=", "in", "not in", "is None", "is not None"]:
                        logger.error("当前操作器是：{} 不在".format(operator))
                else:
                    logger.error("操作器为空，无法进行接口校验！")
                expected_value = every_check_info["expected_value"]
                if expected_value is None or expected_value == "":
                    logger.error("预期结果为空，无法进行接口校验！")
                if not isinstance(acture_result, dict):
                    logger.error("接口实际返回值的数据类型时：{} ，不是dict，无法进行接口校验".format(type(acture_result)))
                not_compare = every_check_info["not_compare"]
                # 根据校验信息的提取方式类型，分别进行判断
                if extract_type.lower() == "response_content":
                    if extract_path.startswith("$"):
                        flag = api_compare(acture_result, not_compare, operator, expected_value, extract_path)
                        check_res.append(flag)
                    else:
                        logger.error("当前的提取路径是：{} ，不正确，无法进行接口校验！提取路径必须以$符号开头且符合jsonpath语法要求".format(extract_path))
                elif extract_type.lower() == "response_code":
                    if extract_path is None:
                        logger.info("暂时缺少提取方式是response_code的接口校验代码")
                        logger.error("暂时缺少提取方式是response_code的接口校验代码")
                    else:
                        logger.error("当提取方式是response_code时，提取路径必须是None . 但当前的提取路径不是None ,而是：{}".format(extract_path))
                elif extract_type.lower() == "cookie":
                    logger.info("暂时缺少提取方式是cookie的接口校验代码")
                    logger.error("暂时缺少提取方式是cookie的接口校验代码")
                elif extract_type.lower() == "interface_headers":
                    logger.info("暂时缺少提取方式是interface_headers的接口校验代码")
                    logger.error("暂时缺少提取方式是interface_headers的接口校验代码")
        # 接下来分析，校验结果列表中，是否有False
        if len(check_res) == 0:
            logger.info("说明没得到任何校验结果")
            logger.info("=====结束接口校验=====")
            return False
        else:
            if False in check_res:
                logger.info("=====结束接口校验=====")
                return False
            else:
                logger.info("=====结束接口校验=====")
                return True
    except Exception as e:
        logger.error("校验接口失败！报错信息是：{}".format(e))
