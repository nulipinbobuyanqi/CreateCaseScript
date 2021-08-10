# coding:utf-8
# @Author: wang_cong
import jsonpath
from Utils.operation_log import initLogger

logger = initLogger(__file__)


def analysis_extractor_info(extractor_info, acture_result, depent_data):
    """

    :param extractor_info: 接口依赖信息
    :param acture_result: 依赖接口的实际返回值
    :param depent_data: 依赖信息，dict类型
    :return: 返回依赖数据
    """
    try:
        # 判断得到的结果是否为None
        if extractor_info is None:
            logger.info("没有被其他接口依赖的字段")
            return depent_data
        else:
            logger.info("有被其他接口依赖的字段，接下来，获取这些依赖信息")
            # 依赖信息一定是list，遍历每个依赖信息
            for m in range(len(extractor_info)):
                logger.info("当前正在获取第{}个依赖信息".format(m + 1))
                every_extractor = extractor_info[m]
                logger.info("当前正在获取第{}个依赖信息，其值是：{}".format(m + 1, every_extractor))
                # 根据依赖信息是否存在extract_type字段，来判断是获取接口依赖字段还是获取SQL依赖字段
                if "extract_type" in list(every_extractor.keys()):
                    logger.info("这是从接口中，获取依赖信息")
                    # 获取依赖数据的各项信息
                    parameter_name = every_extractor["parameter_name"]
                    extract_type = every_extractor["extract_type"]
                    extract_path = every_extractor["extract_path"]
                    parameter_level = every_extractor["parameter_level"]
                    # 根据被依赖字段的获取方式来进行分析判断
                    if extract_type.lower() == "response_content":
                        if extract_path.startswith("$"):
                            # 根据待依赖的字段的jsonpath，找到其数据
                            extract_info = jsonpath.jsonpath(acture_result, extract_path)
                            # 进行判断
                            if not extract_info:
                                raise Exception("通过依赖字段的jsonpath={} ，在实际结果中，找不到对应内容！".format(extract_path))
                            else:
                                # 判断是否为None或者空
                                if extract_info == "None" or extract_info == "" or extract_info is None:
                                    return depent_data
                                else:
                                    # 遍历list里面的每个值，得到依赖数据
                                    depent_value = extract_info[0]
                                    # 将这个字段和字段的值传给depent_data
                                    if parameter_name in list(depent_data.keys()):
                                        logger.info("{}字段已存在接口依赖信息里，无法将其加入".format(parameter_name))
                                    else:
                                        depent_data[parameter_name] = depent_value
                        else:
                            raise Exception("当前的提取路径是：{} ，不正确，无法进行接口校验！提取路径必须以$符号开头且符合jsonpath语法要求".format(extract_path))
                    elif extract_type.lower() == "response_code":
                        if extract_path is None:
                            logger.info("暂时缺少提取方式是response_code的接口校验代码")
                            raise Exception("暂时缺少提取方式是response_code的接口校验代码")
                        else:
                            raise Exception("当提取方式是response_code时，提取路径必须是None . 但当前的提取路径不是None ,而是：{}".format(extract_path))
                    elif extract_type.lower() == "cookie":
                        logger.info("暂时缺少提取方式是cookie的接口校验代码")
                        raise Exception("暂时缺少提取方式是cookie的接口校验代码")
                    elif extract_type.lower() == "interface_headers":
                        logger.info("暂时缺少提取方式是interface_headers的接口校验代码")
                        raise Exception("暂时缺少提取方式是interface_headers的接口校验代码")
                else:
                    logger.info("这是从SQL中，获取依赖信息")
                    # 获取依赖数据的各项信息
                    parameter_name = every_extractor["parameter_name"]
                    extract_path = every_extractor["extract_path"]
                    parameter_level = every_extractor["parameter_level"]
                    hang_count = len(acture_result)
                    logger.info("当前SQL查询结果的总行数为：{}".format(hang_count))
                    split_path = extract_path.split(".")
                    if extract_path.startswith("$"):
                        # 根据待依赖的字段的路径，找到其数据
                        if len(split_path) == 3:
                            hang = int(split_path[1])
                            lie = int(split_path[2])
                            lie_count = len(acture_result[hang - 1])
                            logger.info("当前SQL查询结果，每条数据的总列数是：{}".format(lie_count))
                            logger.info("取SQL查询结果的第{}行第{}列的数据，进行使用".format(hang, lie))
                            # 判断行号是否有效
                            if hang <= hang_count:
                                # 判断列号是否有效
                                if lie <= lie_count:
                                    # 获取提取到的实际结果
                                    acture_result = acture_result[hang - 1][lie - 1]
                                    # 将结果赋值给depent_data
                                    if parameter_name in list(depent_data.keys()):
                                        logger.info("{}字段已存在SQL依赖信息里，无法将其加入".format(parameter_name))
                                    else:
                                        depent_data[parameter_name] = acture_result
                                else:
                                    raise Exception("当前输入的列号是：{} ，大于等于总列数：{} ，列号无效，请检查后重新输入！".format(lie, lie_count))
                            else:
                                raise Exception("当前输入的行号是：{} ，大于等于总行数：{} ，行号无效，请检查后重新输入！".format(hang, hang_count))
                        else:
                            raise Exception("当前的提取路径是：{} ，不正确，无法进行SQL校验！提取路径必须以$符号开头且必须是$.X.Y的格式！".format(extract_path))

            # 应该返回什么呢？

            return depent_data
    except Exception as e:
        logger.info("分析接口依赖信息，获取依赖数据失败！报错信息是：{}".format(e))
