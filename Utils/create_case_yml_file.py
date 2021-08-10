# coding:utf-8
# @Author: wang_cong
# @File: create_case_yml_file.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 10:48
import re
from Template.case_template import case_template
from Utils.analysis_json_data import get_every_path_summary, get_every_path_method, get_every_path_parameter_type, \
    get_every_path_params, get_every_path_header, get_every_path_deprecated, get_every_path_tags
from Utils.operation_yml import save_ruamel_data
from Utils.operation_log import initLogger

logger = initLogger(__file__)


# 生成yml文件，填入接口信息
def create_case_yml_file(all_paths, case_base_path, definition_list, all_definitions, headers=None):
    all_yml_file_path_list = []
    for path in all_paths:
        # 接口协议interface_protocol
        case_template["case_common_info"]['interface_protocol'] = "interface_protocol"
        # 接口名称interface_name
        case_template["case_common_info"]['interface_name'] = get_every_path_summary(all_paths, path)
        # 所属模块belong_module
        case_template["case_common_info"]['belong_module'] = get_every_path_tags(all_paths, path)
        # 接口地址interface_address
        case_template["case_common_info"]['interface_address'] = path
        # 请求方法interface_method
        case_template["case_common_info"]['interface_method'] = get_every_path_method(all_paths, path)
        # 请求参数类型interface_parameters_type
        case_template["case_common_info"]['interface_parameters_type'] = get_every_path_parameter_type(all_paths, path)
        # 请求参数interface_parameters
        case_template["case_list"][0]["case_step"]['interface_parameters'] = get_every_path_params(all_paths, path, definition_list, all_definitions)
        # 请求头interface_headers
        case_template["case_common_info"]['interface_headers'] = get_every_path_header(all_paths, path, definition_list, all_definitions)
        # 将传入的headers与从swagger上抓取的headers进行合并
        case_template["case_common_info"]['interface_headers'] = headers
        # 接口是否已弃用
        case_template["case_common_info"]['deprecated'] = get_every_path_deprecated(all_paths, path)

        # 用例其他信息均设置一个默认值，要么为空，要么有个值
        # 用例名称case_name，取自接口名称
        case_template["case_list"][0]["case_name"] = case_template["case_common_info"]['interface_name']
        # 用例级别case_level，设置normal为默认值
        case_template["case_list"][0]["case_level"] = "normal"
        # 用例所属版本case_version，设置为空
        case_template["case_list"][0]["case_version"] = None

        # 接口校验提取方式extract_type，设置response_content为默认值
        case_template["case_list"][0]["case_step"]["interface_check"][0]["extract_type"] = "response_content"
        # 接口校验不需要比较的字段not_compare，设置为空
        case_template["case_list"][0]["case_step"]["interface_check"][0]["not_compare"] = None
        # 接口校验提取路径extract_path，设置为空
        case_template["case_list"][0]["case_step"]["interface_check"][0]["extract_path"] = None
        # 接口校验操作器operator，设置==为默认值
        case_template["case_list"][0]["case_step"]["interface_check"][0]["operator"] = "=="
        # 接口校验预期结果expected_value，设置为空
        case_template["case_list"][0]["case_step"]["interface_check"][0]["expected_value"] = None
        # 接口依赖参数名parameter_name，设置为空
        case_template["case_list"][0]["case_step"]["interface_extractor"][0]["parameter_name"] = None
        # 接口依赖提取方式extract_type，设置为response_content
        case_template["case_list"][0]["case_step"]["interface_extractor"][0]["extract_type"] = "response_content"
        # 接口依赖提取路径extract_path，设置为空
        case_template["case_list"][0]["case_step"]["interface_extractor"][0]["extract_path"] = None
        # 接口依赖参数级别parameter_level，设置testcase为默认值
        case_template["case_list"][0]["case_step"]["interface_extractor"][0]["parameter_level"] = "testcase"

        # SQL校验数据库类型database_type，设置mysql为默认值
        case_template["case_list"][0]["case_step"]["sql_check"]["database_type"] = "mysql"
        # SQL校验SQL语句类型sql_type，设置select为默认值
        case_template["case_list"][0]["case_step"]["sql_check"]["sql_type"] = "select"
        # SQL校验SQL语句内容sql_content，设置为空
        case_template["case_list"][0]["case_step"]["sql_check"]["sql_content"] = None
        # SQL校验提取路径extract_path，设置为空
        case_template["case_list"][0]["case_step"]["sql_check"]["sql_check"][0]["extract_path"] = None
        # SQL校验操作器operator，设置==为默认值
        case_template["case_list"][0]["case_step"]["sql_check"]["sql_check"][0]["operator"] = "=="
        # SQL校验预期结果expected_value，设置为空
        case_template["case_list"][0]["case_step"]["sql_check"]["sql_check"][0]["expected_value"] = None
        # SQL依赖参数名parameter_name，设置为空
        case_template["case_list"][0]["case_step"]["sql_extractor"][0]["parameter_name"] = None
        # SQL依赖提取路径extract_path，设置为空
        case_template["case_list"][0]["case_step"]["sql_extractor"][0]["extract_path"] = None
        # SQL依赖参数级别parameter_level，设置testcase为默认值
        case_template["case_list"][0]["case_step"]["sql_extractor"][0]["parameter_level"] = "testcase"

        # 最后，生成每个用例模板信息yml文件
        # print("去除"+"{}"+"符号前，接口路径path={}".format(path))
        path = re.sub(r"{.*}", "", path, count=0, flags=0)
        # print("去除"+"{}"+"符号后，接口路径path={}".format(path))
        case_yml_path = case_base_path + path
        all_yml_file_path_list.append(case_yml_path.replace("\\", "/"))
        if path.split("/")[-1] != "":
            yaml_file_name = path.split("/")[-1] + "_1"
        else:
            yaml_file_name = path.split("/")[-2] + "_1"
        yaml_data = case_template
        save_ruamel_data(case_yml_path, yaml_file_name, yaml_data)
    # logger.debug(all_yml_file_path_list)
    return all_yml_file_path_list
