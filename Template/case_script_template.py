# coding:utf-8
# @Author: wang_cong
import json
import os
import allure
import pytest
from Check.analysis_extractor_info import analysis_extractor_info
from Check.check_api_result import check_api_result
from Check.check_sql_result import check_sql_result
from Check.replace_params import replace_params
from Check.send_api_request import send_api_request
from Check.send_sql_request import send_sql_request
from Utils.operation_json import save_json_data
from Utils.operation_sql import get_sql_data
from Utils.operation_yml import get_yaml_data, save_ruamel_data
# from Utils.operation_log import initLogger
# 
# logger = initLogger(__file__)

# 项目名称，注意：拼接请求地址时，若需要项目名称，则project的值不能为""
project = "template"
# 数据库配置信息
db_env_path = "template"
db_env_file_name = "db_env"
db_env_data = get_yaml_data(db_env_path, db_env_file_name)
# 运行配置信息
run_config_path = "template"
run_config_file_name = "RunConfig"
run_config_data = get_yaml_data(run_config_path, run_config_file_name)
# 运行环境
run_env = run_config_data["env"]
# 接口请求地址，是否需要携带项目名称
need_project_name = run_config_data["need_project_name"]
# 服务配置信息，注意：接口测试与具体使用哪个服务无关，因此，直接默认使用第一个服务配置信息
service_env_path = "template"
service_env_file_name = "service_env"
service_env_data = get_yaml_data(service_env_path, service_env_file_name)
service_info = service_env_data[run_env]
service_data = service_info[0]
host = service_data["host"]
port = service_data["port"]
# 用例信息
case_path = "template"
case_file_name = "template"
case_dict = get_yaml_data(case_path, case_file_name)
# 具体的用例通用相关信息
interface_protocol = case_dict["case_common_info"]["interface_protocol"]
interface_name = case_dict["case_common_info"]["interface_name"]
interface_address = case_dict["case_common_info"]["interface_address"]
interface_method = case_dict["case_common_info"]["interface_method"]
interface_headers = case_dict["case_common_info"]["interface_headers"]
interface_parameters_type = case_dict["case_common_info"]["interface_parameters_type"]
need_file = case_dict["case_common_info"]["need_file"]
interface_deprecated = case_dict['case_common_info']['deprecated']
need_cookie = case_dict['case_common_info']["need_cookie"]
belong_module = case_dict['case_common_info']["belong_module"]
# 需要判断是否携带请求头
if need_cookie:
    interface_headers = interface_headers
else:
    interface_headers = {}
print("判断是否需要携带请求头后，得到的interface_headers是：{}".format(interface_headers))
# 具体的用例数据信息，得到的是一个list数据，并且每个yml文件中，只有一条用例
case_data_info = case_dict["case_list"]
# 依赖信息
depent_path = "template"
depent_file_name = "depent_data"
all_depent_data = get_yaml_data(depent_path, depent_file_name)
# 完整的接口请求地址
if need_project_name:
    base_url = interface_protocol + "://" + host + ":" + str(port) + "/" + project
else:
    base_url = interface_protocol + "://" + host + ":" + str(port)
# 当前用例的编号
file_number = str(os.path.basename(__file__).split("_")[-1].split(".")[0])
# 用例运行所需要的的SQL配置信息
sql_path = "template"
init_sql_file_name = "test_init_sql_" + file_number
clear_sql_file_name = "test_clear_sql_" + file_number


# allure装饰器，用法举例
@allure.epic("项目名称：{}".format(project))
@allure.feature("模块名称：{}".format(belong_module))
@allure.suite("测试套件名称：{}".format(belong_module))
class TestApiCycleInfoQueryList:

    def setup_method(self):
        with allure.step("第一步：初始化用例所需的数据环境"):
            print("执行SQL文件，初始化用例所需的数据环境")
            # 准备获取SQL信息，然后执行SQL，初始化环境。注意：SQL类型可以是insert、update、delete，也可以是select
            # 注意：若SQL类型是insert、update、delete，说明是要为接口执行准备一些初始化数据等信息
            # 注意：若SQL类型是select，说明查询出来的结果，要当做依赖字段信息
            # 注意：SQL文件中的第一行，必须写上# 数据库类型
            all_sql_list = get_sql_data(sql_path, init_sql_file_name)
            # 本条用例的初始化依赖字段信息，假设为depent_data字段，
            dict_sql_depent = {

            }
            dict_api_depent = {

            }
            # 目前这种格式，还缺少依赖字段的级别，testcase、testsuite、global
            self.depent_data = {
                "/api/info/save": {
                    "interface_depent_data": [
                        dict_api_depent
                    ],
                    "sql_depent_data": [
                        dict_sql_depent
                    ]
                }
            }
            # 因为前四行是注意事项，所以长度设置的是4
            if len(all_sql_list) != 4:
                # 数据库类型
                database_type = all_sql_list[4].split(" ")[-1].replace("\n","")
                print("有初始化用例环境所需要运行的SQL")
                for i in range(5, len(all_sql_list)):
                    print("当前正在获取第{}个需要初始化环境的SQL".format(i))
                    sql_content = all_sql_list[i].split("\n")[0]
                    print("第{}个SQL={}".format(i - 4, sql_content))
                    if sql_content != "":
                        # 对SQL语句进行切片，获取SQL语句类型
                        sql_type = sql_content.split(" ")[0]
                        print("第{}个SQL的类型是：{}".format(i - 4, sql_type))
                        # 执行SQL查询，得到查询结果
                        sql_acture_result = send_sql_request(run_env, db_env_data, database_type, sql_type, sql_content)
                        print("执行第{}个SQL，得到的结果是：{}".format(i - 4, sql_acture_result))
                        if sql_type.lower() == "select":
                            field_list = sql_content.split(" from")[0].split("select ")[-1].split(",")
                            for field in field_list:
                                # 去除空格
                                if " " in field:
                                    old_field = field
                                    new_field = field.replace(" ", "")
                                    field_list.remove(old_field)
                                    field_list.append(new_field)
                                if field == "*":
                                    print("取所有字段，无意义，不加入依赖字段信息")
                                    break
                            print("执行第{}个SQL，得到的结果，其对应的字段列表是：{}".format(i - 4, field_list))
                        if sql_type.lower() == "select":
                            # 当查询出来的结果不为空时，将SQL执行结果，放置在依赖字段信息
                            if len(sql_acture_result) == 1:
                                # 将tuple类型的结果进行转换，变成list
                                list_result = list(sql_acture_result)
                                # 遍历每个结果
                                for j in range(len(list_result)):
                                    print("正在遍历第{}个查询结果值".format(j + 1))
                                    print("第{}个查询结果值为：{}".format(j + 1, list_result[j]))
                                    # 遍历查询结果值，将每个值对应到字段名称上
                                    for n in range(len(list_result[j])):
                                        value = list_result[j][n]
                                        # 将这个值，赋值给字段，并且赋值给依赖信息
                                        key = field_list[n]
                                        if key in list(dict_sql_depent.keys()):
                                            print("{}字段已存在依赖信息里，不能继续将它加入到依赖信息".format(key))
                                        else:
                                            dict_sql_depent[key] = value
                            else:
                                print("第{}个初始化select类型的SQL，查询出来的结果要么为空，要么有多条结果，本套代码仅支持一条查询结果，所以，无法将结果写入依赖信息".format(i - 4))
                        else:
                            print("第{}个SQL不是查询语句，无需加入依赖信息".format(i - 4))
                            print("\n")
                            continue
                    else:
                        print("第{}个SQL为空，跳出，继续遍历下一个SQL语句".format(i - 4, sql_content))
                        print("\n")
                        continue
                    print("\n")
            else:
                print("没有初始化用例环境所需要运行的SQL")

    def teardown_method(self):
        with allure.step("第十二步：清除用例执行后的数据环境"):
            print("执行SQL文件，清除用例执行后的数据环境")
            all_sql_list = get_sql_data(sql_path, clear_sql_file_name)
            # 因为前四行是注意事项，所以长度设置的是4
            if len(all_sql_list) != 4:
                # 数据库类型
                database_type = all_sql_list[4].split(" ")[-1].replace("\n","")
                print("有清除用例环境所需要运行的SQL")
                for i in range(5, len(all_sql_list)):
                    print("当前正在获取第{}个需要清除环境的SQL".format(i))
                    sql_content = all_sql_list[i].split("\n")[0]
                    print("第{}个SQL={}".format(i - 4, sql_content))
                    if sql_content != "":
                        # 对SQL语句进行切片，获取SQL语句类型
                        sql_type = sql_content.split(" ")[0]
                        print("第{}个SQL的类型是：{}".format(i - 4, sql_type))
                        if sql_type.lower() != "select":
                            # 执行SQL
                            send_sql_request(run_env, db_env_data, database_type, sql_type, sql_content)
                        else:
                            print("清除用例环境的SQL语句类型，不能是select ！")
                    else:
                        print("第{}个SQL为空，跳出，继续遍历下一个SQL语句".format(i - 4, sql_content))
                        print("\n")
                        continue
                    print("\n")
            else:
                print("没有清除用例环境所需要运行的SQL")

    # allure装饰器，用法举例
    # @allure.story("这里要准备写:被测功能的用户场景（若无，请注释掉此行）：" + belong_module)
    # @allure.title("这里要准备写:用例标题（若无，请注释掉此行）：" + case_data_info[0]["case_name"])
    @allure.title("用例标题：" + case_data_info[0]["case_name"])
    # @allure.testcase("这里要准备写:测试用例的链接地址（若无，请注释掉此行）")
    # @allure.issue("这里要准备写:bug地址（若无，请注释掉此行）")
    @allure.severity("用例等级：" + case_data_info[0]["case_level"])
    # pytest装饰器，用法举例
    # 假设：第一条用例的is_run=False,说明不执行，直接跳过
    @pytest.mark.skipif(condition=case_data_info[0]["is_run"] is False, reason="该条用例的is_run=False,说明不执行，直接跳过")
    @pytest.mark.run(case_data_info[0]["run_order"])
    @pytest.mark.parametrize("every_case_data", case_data_info)
    def test_template(self, every_case_data):

        with allure.step("第二步：发起HTTP请求"):
            # 需要对URL，进行替换处理，如果URL中，含有${}，代表其依赖了其他的参数字段
            url = replace_params(base_url + interface_address, self.depent_data)
            print("替换后的url是：{}".format(url))
            parameters = every_case_data["case_step"]["interface_parameters"]
            # 需要对请求参数，进行替换处理，如果URL中，含有${}，代表其依赖了其他的参数字段
            interface_parameters = replace_params(parameters, self.depent_data)
            print("替换后的parameters是：{}".format(interface_parameters))
            print("当前接口：{} 的请求参数是：{}".format(interface_address, parameters))
            print("当前接口：{} 的请求参数的数据类型是：{}".format(interface_address, type(parameters)))
            # 判断是否需要上传文件
            if need_file:
                print("当前接口：{} 需要上传文件".format(interface_address))
                # 发起接口请求
                file_name = interface_parameters["file"]
                print("当前接口：{} 上传的文件是：{} ".format(interface_address, str(file_name)))
                api_acture_result = send_api_request(interface_address, interface_parameters_type, interface_method, interface_parameters, url, interface_headers, file_name)
            else:
                print("当前接口：{} 不需要上传文件".format(interface_address))
                # 执行接口，得到接口返回值
                api_acture_result = send_api_request(interface_address, interface_parameters_type, interface_method, interface_parameters, url, interface_headers)
            allure.attach(name="接口实际返回值", body=str(api_acture_result))
            print("当前接口：{} 的接口实际返回值是：{}".format(interface_address, api_acture_result))

        with allure.step("第三步：将接口执行结果写入文件"):
            save_json_data(case_path, json_file_name, api_acture_result)

        # 注意，强制要求，既要校验接口，也要校验SQL，只有两者全部校验通过，用例才算真的通过
        with allure.step("第四步：进行接口校验"):
            api_check_info = every_case_data["case_step"]["interface_check"]
            print("当前接口：{} 的接口校验信息是：{}".format(interface_address, api_check_info))
            if api_check_info is not None:
                # 进行接口校验
                api_check_res = check_api_result(api_check_info, api_acture_result)
                # 判断接口校验是否通过
                if api_check_res:
                    allure.attach(name="接口校验结果", body="PASS")
                    print("当前接口：{} 的接口校验通过！".format(interface_address))
                    pytest.assume(api_check_res is True)
                else:
                    allure.attach(name="接口校验结果", body="FAIL")
                    print("当前接口：{} 的接口校验失败！".format(interface_address))
                    pytest.assume(api_check_res is True)
            else:
                allure.attach(name="接口校验信息", body="空")
                print("当前接口：{} 的接口校验信息为空！无法进行校验！请检查！".format(interface_address))
                pytest.assume(api_check_info is not None)

        with allure.step("第五步：发起SQL请求"):
            # 获取发起查询前的各项信息
            sql_info = every_case_data["case_step"]["sql_check"]
            print("当前接口：{} 的SQL请求信息是：{}".format(interface_address, sql_info))
            if sql_info is not None:
                database_type = sql_info["database_type"]
                sql_type = sql_info["sql_type"]
                sql_content = sql_info["sql_content"]
                # 需要对SQL语句，进行替换处理，如果SQL语句中，含有${}，代表其依赖了其他的参数字段
                sql_content = replace_params(sql_content, self.depent_data)
                print("替换后的sql是：{}".format(sql_content))
                sql_acture_result = send_sql_request(run_env, db_env_data, database_type, sql_type, sql_content)
                allure.attach(name="SQL实际返回值", body=str(sql_acture_result))
                print("当前接口：{} 的SQL实际返回值是：{}".format(interface_address, sql_acture_result))
            else:
                allure.attach(name="SQL校验信息", body="空")
                print("当前接口：{} 的SQL校验信息为空！无法进行校验！请检查！".format(interface_address))
                pytest.assume(sql_info is not None)

        with allure.step("第六步：进行SQL校验"):
            sql_check_info = every_case_data["case_step"]["sql_check"]["sql_check"]
            print("当前接口：{} 的SQL校验信息是：{}".format(interface_address, sql_check_info))
            # 准备进行校验
            if sql_check_info is not None:
                # 进行SQL校验
                sql_check_res = check_sql_result(sql_check_info, sql_acture_result)
                # 判断SQL校验是否通过
                if sql_check_res:
                    allure.attach(name="SQL校验结果", body="PASS")
                    print("当前接口：{} 的SQL校验通过！".format(interface_address))
                    pytest.assume(sql_check_res is True)
                else:
                    allure.attach(name="SQL校验结果", body="FAIL")
                    print("当前接口：{} 的SQL校验失败！".format(interface_address))
                    pytest.assume(sql_check_res is True)
            else:
                allure.attach(name="SQL校验信息", body="空")
                print("当前接口：{} 的SQL校验信息为空！无法进行校验！请检查！".format(interface_address))
                pytest.assume(sql_check_info is not None)

        with allure.step("第七步：判断用例执行结果是通过还是失败"):
            if api_check_res and sql_check_res:
                allure.attach(name="用例执行结果", body="PASS")
                print("当前接口：{} 接口校验和SQL校验都通过！".format(interface_address))
                # 说明用例通过，将结果设置为PASS
                case_res = True
                pytest.assume(case_res is True)

                with allure.step("第八步：获取当前接口被其他接口依赖的字段信息"):
                    # 只有校验通过，才允许获取依赖信息
                    api_depent_data = {

                    }
                    sql_depent_data = {

                    }
                    with allure.step("第九步：从接口返回值中，获取被其他接口依赖的字段信息"):
                        # 从接口中，获取依赖信息
                        api_extractor_info = every_case_data["case_step"]["interface_extractor"]
                        # 分析依赖信息
                        api_depent_data = analysis_extractor_info(api_extractor_info, api_acture_result, api_depent_data)
                        allure.attach(name="从接口返回值中，得到的依赖信息", body=json.dumps(api_depent_data))

                    with allure.step("第十步：从SQL查询结果中，获取被其他接口依赖的字段信息"):
                        # 从SQL中，获取依赖信息
                        sql_extractor_info = every_case_data["case_step"]["sql_extractor"]
                        # 分析依赖信息
                        sql_depent_data = analysis_extractor_info(sql_extractor_info, sql_acture_result, sql_depent_data)
                        allure.attach(name="从SQL查询结果中，得到的依赖信息", body=json.dumps(sql_depent_data))

                    with allure.step("第十一步：将从接口和SQL中获取到的依赖信息，写入depent_data.yml文件"):
                        # 设置依赖信息为字段depent_data，其格式如下：
                        depent_data = {
                            interface_address: {
                                "interface_depent_data": [
                                    api_depent_data
                                ],
                                "sql_depent_data": [
                                    sql_depent_data
                                ]
                            }
                        }
                        allure.attach(name="最终得到的依赖信息", body=json.dumps(depent_data))
                        save_ruamel_data(depent_path, depent_file_name, depent_data)

            else:
                allure.attach(name="用例执行结果", body="FAIL")
                print("当前接口：{} 接口校验和SQL校验，至少有一个未通过！".format(interface_address))
                # 说明用例失败，将结果设置为FAIL
                case_res = False
                pytest.assume(case_res is True)
