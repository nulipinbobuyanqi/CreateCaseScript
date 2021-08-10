# coding:utf-8
# @Author: wang_cong
import json
import allure
import requests
from Utils.operation_log import initLogger

logger = initLogger(__file__)


def send_api_request(interface_address, interface_parameters_type, interface_method, interface_parameters, url,
                     interface_headers, file_name=None):
    """
    发起接口请求，并得到接口返回值
    :param interface_address: 接口地址
    :param interface_parameters_type: 接口参数类型
    :param interface_method: 接口请求方法
    :param interface_parameters: 接口请求参数
    :param url: 完整的接口请求地址
    :param interface_headers: 接口请求头
    :param file_name: 完整的文件路径+文件名称+文件格式后缀
    :return: 返回接口返回值
    """
    try:
        """
        第一类：常见的媒体格式类型，如下：

        text/html ： HTML格式
        text/plain ：纯文本格式
        text/xml ： XML格式
        image/gif ：gif图片格式
        image/jpeg ：jpg图片格式
        image/png：png图片格式

        第二类：以application开头的媒体格式类型，如下：

        application/xhtml+xml ：XHTML格式
        application/xml： XML数据格式
        application/atom+xml ：Atom XML聚合格式
        application/json： JSON数据格式
        application/pdf：pdf格式
        application/msword ： Word文档格式
        application/octet-stream ： 二进制流数据（如常见的文件下载）
        application/x-www-form-urlencoded ： <form encType=””>中默认的encType，form表单数据被编码为key/value格式发送到服务器（表单默认的提交数据的格式）

        第三类：另外一种常见的媒体格式是上传文件之时使用的：

        multipart/form-data ： 需要在表单中进行文件上传时，就需要使用该格式
        """
        # 根据Content-Type类型、method类型、parameters类型，来判断，该使用什么方法，执行请求
        if interface_parameters_type == "application/x-www-form-urlencoded":
            if interface_method.lower() == "post":
                if isinstance(interface_parameters, dict):
                    if interface_parameters != {}:
                        with allure.step("含参数的application/x-www-form-urlencoded的POST请求接口"):
                            allure.attach(name="请求接口", body=str(interface_address))
                            allure.attach(name="请求地址", body=url)
                            allure.attach(name="请求头", body=str(interface_headers))
                            allure.attach(name="请求参数", body=str(interface_parameters))
                        res = requests.post(url=url, data=interface_parameters, headers=interface_headers)
                        return res.json()
                    else:
                        logger.error("请求参数为空，无法进行请求！")
                else:
                    logger.error("参数的请求类型不是dict，无法进行请求！")
            else:
                logger.error("请求方法不是post，无法进行请求！")
        elif interface_parameters_type == "multipart/form-data":
            if interface_method.lower() == "post":
                files_data = {
                    "file": open(file_name, "rb")
                }
                with allure.step("需要上传文件的POST请求接口"):
                    allure.attach(name="请求接口", body=str(interface_address))
                    allure.attach(name="请求地址", body=url)
                    allure.attach(name="请求头", body=str(interface_headers))
                    allure.attach(name="请求参数", body=str(interface_parameters))
                    allure.attach(name="文件名称", body=str(file_name))
                res = requests.post(url=url, data=json.dumps(interface_parameters), headers=interface_headers,
                                    files=files_data)
                # res = requests.post(url=url, json=interface_parameters, headers=interface_headers, files=files_data)
                return res.json()
            else:
                logger.error("请求方法不是post，无法进行请求！")

        elif "application/json" in interface_parameters_type:
            if interface_method.lower() == "post":
                if isinstance(interface_parameters, dict):
                    if interface_parameters != {}:
                        with allure.step("含参数的application/json的POST请求接口"):
                            allure.attach(name="请求接口", body=str(interface_address))
                            allure.attach(name="请求地址", body=url)
                            allure.attach(name="请求头", body=str(interface_headers))
                            allure.attach(name="请求参数", body=str(interface_parameters))
                        res = requests.post(url=url, json=interface_parameters, headers=interface_headers)
                        return res.json()
                    else:
                        logger.error("请求参数为空，无法进行请求！")
                else:
                    logger.error("参数的请求类型不是dict，无法进行请求！")
            # 其实method=post，也可以用下面这样的方式进行请求：data=json.dumps(parameters)
            # if interface_method.lower() == "post":
            #     if isinstance(interface_parameters, dict):
            #         if interface_parameters != {}:
            #             res = requests.post(url=url, data=json.dumps(interface_parameters), headers=interface_headers)
            #             return res.json()
            #         else:
            #             logger.error("请求参数为空，无法进行请求！")
            #     else:
            #         logger.error("参数的请求类型不是dict，无法进行请求！")
            elif interface_method.lower() == "get":
                if isinstance(interface_parameters, dict):
                    if interface_parameters != {}:
                        with allure.step("含参数的application/json的GET请求接口"):
                            allure.attach(name="请求接口", body=str(interface_address))
                            allure.attach(name="请求地址", body=url)
                            allure.attach(name="请求头", body=str(interface_headers))
                            allure.attach(name="请求参数", body=str(interface_parameters))
                        res = requests.get(url=url, data=json.dumps(interface_parameters), headers=interface_headers)
                        return res.json()
                    else:
                        with allure.step("不含参数的application/json的GET请求接口"):
                            allure.attach(name="请求接口", body=str(interface_address))
                            allure.attach(name="请求地址", body=url)
                            allure.attach(name="请求头", body=str(interface_headers))
                        res = requests.get(url=url, headers=interface_headers)
                        return res.json()
                else:
                    logger.error("参数的请求类型不是dict，无法进行请求！")
            # 其实method=get，也可以用下面这样的方式进行请求：params=parameters
            # elif interface_method.lower() == "get":
            #     if isinstance(interface_parameters, dict):
            #         if interface_parameters != {}:
            #             res = requests.get(url=url, params=interface_parameters, headers=interface_headers)
            #             return res.json()
            #         else:
            #             res = requests.get(url=url, headers=interface_headers)
            #             return res.json()
            #     else:
            #         logger.error("参数的请求类型不是dict，无法进行请求！")
            else:
                logger.error("请求方法既不是post，也不是get，无法进行请求！")
        else:
            logger.error("当前的请求头Content-Type类型是：{} ，本套代码暂不支持！无法发起请求！".format(interface_parameters_type))
    except Exception as e:
        logger.error("发起接口请求失败！报错信息是：{}".format(e))
