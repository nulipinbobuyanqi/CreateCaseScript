# coding:utf-8
# @Author: wang_cong
import re
from Utils.operation_log import initLogger

logger = initLogger(__file__)


def replace_params(before_replace, extract_data):
    """
    将含有${}符号的数据，进行替换，并返回
    :param before_replace: 替换前的数据
    :param extract_data: 被替换的数据，dict类型的数据
    :return: 返回不含${}符号的数据
    """
    logger.debug("替换前的数据为：{}".format(before_replace))
    logger.debug("替换前的数据，其数据类型为：{}".format(type(before_replace)))
    logger.debug("被替换的数据，其值是：{}".format(extract_data))
    if extract_data is None or extract_data == "":
        return before_replace
    else:
        if isinstance(extract_data, dict):
            extract_data_keys_list = extract_data.keys()
            if isinstance(before_replace, str):
                param_rel_key_list = re.findall(r"\${(.*?)}", before_replace)
                for index in range(len(param_rel_key_list)):
                    pattern = re.compile(r'\${' + param_rel_key_list[index] + r'}')
                    key = param_rel_key_list[index]
                    if key in extract_data_keys_list:
                        extract_data_key_value = extract_data[key]
                        if isinstance(extract_data_key_value, list):
                            list_value = []
                            for k in range(len(extract_data_key_value)):
                                param = re.sub(pattern, extract_data_key_value[k], before_replace, count=1)
                                list_value.append(param)
                            before_replace = list_value
                        elif isinstance(extract_data_key_value, str):
                            before_replace = re.sub(pattern, extract_data_key_value, before_replace, count=1)
                    else:
                        logger.error("在extract_data字典里，找不到key={}的关联键，采取返回替换前的参数={}的方式".format(key,before_replace))
                before_replace = before_replace
            elif isinstance(before_replace, list):
                for k, i in enumerate(before_replace):
                    before_replace[k] = replace_params(i, extract_data)
            elif isinstance(before_replace, dict):
                for key in list(before_replace.keys()):
                    logger.debug("key={}".format(key))
                    value = before_replace[key]
                    if isinstance(value, list):
                        for k, i in enumerate(value):
                            before_replace[key][k] = replace_params(i, extract_data)
                    elif isinstance(value, dict):
                        before_replace[key] = replace_params(value, extract_data)
                    elif isinstance(value, str):
                        param_rel_key_list = re.findall(r"\${(.*?)}", value)
                        for index in range(len(param_rel_key_list)):
                            pattern = re.compile(r'\${' + param_rel_key_list[index] + r'}')
                            key1 = param_rel_key_list[index]
                            logger.debug("key1={}".format(key1))
                            if key1 in extract_data_keys_list:
                                extract_data_key_value = extract_data[key1]
                                if isinstance(extract_data_key_value, list):
                                    list_value = []
                                    for k in range(len(extract_data_key_value)):
                                        param = re.sub(pattern, extract_data_key_value[k], value, count=1)
                                        list_value.append(param)
                                    before_replace[key] = list_value
                                elif isinstance(extract_data_key_value, str):
                                    logger.debug("key={}".format(key))
                                    before_replace[key] = re.sub(pattern, extract_data_key_value, value, count=1)
                            else:
                                before_replace[key] = value
                                return None
            logger.debug("对含有${{}}$标识的数据（如：请求参数、请求地址、关联值）, 进行替换后，得到的是：{}".format(before_replace))
            return before_replace
        else:
            logger.error("要被替换的数据，其数据类型是：{} ， 不是dict，无法进行替换！".format(type(extract_data)))
