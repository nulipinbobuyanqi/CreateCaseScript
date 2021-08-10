# coding:utf-8
# @Author: wang_cong
from Check.check_api_result import check_api_result
from Check.check_sql_result import check_sql_result
from Check.replace_params import replace_params
from Check.send_api_request import send_api_request
from Check.send_sql_request import send_sql_request
from Check.analysis_extractor_info import analysis_extractor_info
from Utils.operation_log import initLogger

logger = initLogger(__file__)


def get_depent_data(premise_step_info, base_url, dict_api_depent, dict_sql_depent, depent_data, interface_address, run_env=None, db_env_data=None):
    """
    根据传入的前置条件信息，得到依赖的参数信息，并返回
    :param premise_step_info: 前置条件信息
    :param base_url: 基本的接口请求地址
    :param dict_api_depent: 接口依赖信息，dict类型
    :param dict_sql_depent: SQL依赖信息，dict类型
    :param depent_data: 总的依赖信息，dict类型
    :param interface_address: 接口地址
    :param run_env: 运行环境
    :param db_env_data: 数据库配置信息
    :return: 返回依赖的参数信息
    """
    try:

        # 对前置条件信息，进行判断
        if premise_step_info is None:
            logger.info("无前置依赖信息")
            return depent_data
        else:
            logger.info("有前置依赖信息")
            logger.info("一共有{}个依赖信息".format(len(premise_step_info)))
            # 所有的步骤编号，组成一个列表
            step_number_list = [

            ]
            # 遍历每一个前置依赖信息
            for p in range(len(premise_step_info)):
                logger.info("当前正在遍历第{}个依赖信息".format(p + 1))
                every_premise_info = premise_step_info[p]
                logger.info("第{}个依赖信息是：{}".format(p + 1, every_premise_info))
                # 获取当前这个依赖信息的步骤编号
                step_number = int(every_premise_info["step_number"])
                # 将这个步骤编号，存入步骤编号列表
                if step_number not in step_number_list:
                    step_number_list.append(step_number)
                else:
                    logger.error("步骤编号step_number={}的前置信息，编号和其他步骤的编号，重复了！无法加入到步骤编号列表去，后续执行前置条件".format(step_number))
            # 按照步骤编号，从小到大的排序展示
            step_number_list = sorted(step_number_list)
            # 设置新的前置条件信息为new_premise_step_info
            new_premise_step_info = [

            ]
            # 根据步骤编号顺序，重新组合前置条件信息
            for step_number in step_number_list:
                for every_premise_data in premise_step_info:
                    if every_premise_data["step_number"] == step_number:
                        new_premise_step_info.append(every_premise_data)
            # 接下来，按照步骤编号列表中的步骤顺序，去执行前置条件
            logger.info("重整过前置条件步骤后，最新的前置条件信息是：{}".format(new_premise_step_info))
            # 遍历每一个前置依赖信息
            for n in range(len(new_premise_step_info)):
                logger.info("当前正在遍历第{}个依赖信息".format(n + 1))
                every_premise_info = premise_step_info[n]
                logger.info("第{}个依赖信息是：{}".format(n + 1, every_premise_info))
                step_type = every_premise_info["step_type"]
                # 根据步骤类型，分别获取前置依赖信息
                if step_type is None or step_type == "":
                    logger.error("步骤类型为空，无法获取前置依赖信息！")
                if step_type.lower() not in ["api", "sql"]:
                    logger.error("当前步骤类型是：{} ，本套代码暂不支持，无法获取前置依赖信息！".format(step_type))
                if step_type.lower() == "api":
                    """
                    第一步：获取接口前置信息
                    """
                    logger.info("=====开始从接口中获取前置依赖信息=====")
                    # 获取发起请求前的各项信息
                    api = every_premise_info["api"]
                    interface_address = api["interface_address"]
                    interface_method = api["interface_method"]
                    interface_headers = api["interface_headers"]
                    interface_parameters_type = api["interface_parameters_type"]
                    interface_parameters = api["interface_parameters"]
                    need_cookie = api["need_cookie"]
                    belong_module = api["belong_module"]
                    # 需要判断是否携带请求头
                    if need_cookie:
                        interface_headers = interface_headers
                    else:
                        interface_headers = {}
                    logger.info("判断是否需要携带请求头后，得到的interface_headers是：{}".format(interface_headers))
                    # 需要对URL，进行替换处理，如果URL中，含有${}，代表其依赖了其他的参数字段
                    url = replace_params(base_url + interface_address, depent_data)
                    logger.info("替换后的url是：{}".format(url))
                    # 需要对请求参数，进行替换处理，如果URL中，含有${}，代表其依赖了其他的参数字段
                    interface_parameters = replace_params(interface_parameters, depent_data)
                    logger.info("替换后的parameters是：{}".format(interface_parameters))
                    # 判断是否为上传文件接口
                    if api["need_file"]:
                        file_name = api["file"]
                        # 执行前置条件接口，得到前置接口返回值
                        acture_result = send_api_request(interface_address, interface_parameters_type, interface_method, interface_parameters, url, interface_headers, file_name)
                        logger.info("执行前置接口，得到的接口返回值是：{}".format(acture_result))
                    else:
                        # 执行前置条件接口，得到前置接口返回值
                        acture_result = send_api_request(interface_address, interface_parameters_type, interface_method, interface_parameters, url, interface_headers)
                        logger.info("执行前置接口，得到的接口返回值是：{}".format(acture_result))
                    # 执行接口校验，只有校验通过了，才允许去获取依赖信息
                    check_info = api["interface_check"]
                    logger.info("前置接口的校验信息是：{}".format(check_info))
                    # 准备进行校验
                    check_res = check_api_result(check_info, acture_result)
                    if check_res:
                        logger.info("前置接口校验通过！")
                        # 校验通过，准备获取该接口被其他接口所依赖的字段信息
                        api_extractor_info = api["interface_extractor"]
                        # 分析依赖信息，得到准确的一定是一个list
                        dict_api_depent = analysis_extractor_info(api_extractor_info, acture_result, dict_api_depent)
                    else:
                        logger.error("前置接口校验失败！")
                    logger.info("=====结束从接口中获取前置依赖信息=====")
                elif step_type.lower() == "sql":
                    """
                    第一步：获取SQL前置信息
                    """
                    logger.info("=====开始从SQL中获取前置依赖信息=====")
                    # 获取发起查询前的各项信息
                    premise_sql_info = every_premise_info["sql"]
                    database_type = premise_sql_info["database_type"]
                    sql_type = premise_sql_info["sql_type"]
                    sql_content = premise_sql_info["sql_content"]
                    # 需要对SQL语句，进行替换处理，如果SQL语句中，含有${}，代表其依赖了其他的参数字段
                    sql_content = replace_params(sql_content, depent_data)
                    logger.info("替换后的sql是：{}".format(sql_content))
                    # 执行SQL查询，得到查询结果
                    acture_result = send_sql_request(run_env, db_env_data, database_type, sql_type, sql_content)
                    logger.info("执行前置SQL，得到的查询返回值是：{}".format(acture_result))
                    # 执行SQL校验，只有校验通过了，才允许去获取依赖信息
                    check_info = premise_sql_info["sql_check"]
                    logger.info("前置SQL的校验信息是：{}".format(check_info))
                    # 准备进行校验
                    check_res = check_sql_result(check_info, acture_result)
                    if check_res:
                        logger.info("前置SQL校验通过！")
                        # 校验通过，准备获取该SQL中被其他接口所依赖的字段信息
                        sql_extractor_info = premise_sql_info["sql_extractor"]
                        # 分析依赖信息，得到准确的一定是一个list
                        dict_sql_depent = analysis_extractor_info(sql_extractor_info, acture_result, dict_sql_depent)
                    else:
                        logger.error("前置SQL校验失败！")
                    logger.info("=====结束从SQL中获取前置依赖信息=====")
            # 拼接出来总得依赖信息
            depent_data = {
                interface_address: {
                    "interface_depent_data": [
                        dict_api_depent
                    ],
                    "sql_depent_data": [
                        dict_sql_depent
                    ]
                }
            }
            logger.info("依赖信息是：{}".format(depent_data))
            return depent_data
    except Exception as e:
        logger.error("获取依赖信息失败！报错信息是：{}".format(e))

