# coding:utf-8
# @Author: wang_cong
# @File: StartRun.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 19:12


import os
import time
from Utils.create_case_script import create_case_script
from Utils.get_project_config import get_project_config_info
from Utils.operation_yml import get_yaml_data


# 第八步：获取当前日期，作为接口版本号
new = time.strftime("%Y-%m-%d", time.localtime())
# new = "2021-08-04"

# 第一步：获取项目配置信息的存放根路径
project_yaml_path = "."
project_yaml_file_name = "project_path"
gen_path = get_yaml_data(project_yaml_path, project_yaml_file_name)["project_path"]
project_path = gen_path + "/ProjectManage/"
project_config_path = project_path + "01.ProjectConfig"
if not os.path.exists(project_config_path):
    os.makedirs(project_config_path)
# 第二步：获取项目配置信息
project, protocol, swagger_url = get_project_config_info(project_path)
# 第三步：创建接口信息json文件的存放根目录
interfaces_gen_path = project_path + "02.InterfaceData" + "/" + project
if not os.path.exists(interfaces_gen_path):
    os.makedirs(interfaces_gen_path)
#
new_interface_path = interfaces_gen_path + "/" + new
if not os.path.exists(new_interface_path):
    os.makedirs(new_interface_path)
# 第四步：创建接口信息模板yml文件存放根目录
api_template_gen_path = project_path + "03.InterfaceTemplate" + "/" + project
if not os.path.exists(api_template_gen_path):
    os.makedirs(api_template_gen_path)
#
new_api_path = api_template_gen_path + "/" + new
if not os.path.exists(new_api_path):
    os.makedirs(new_api_path)
# 第五步：创建测试用例模板yml文件存放根目录
case_template_gen_path = project_path + "05.CaseTemplate" + "/" + project
if not os.path.exists(case_template_gen_path):
    os.makedirs(case_template_gen_path)
#
new_case_path = case_template_gen_path + "/" + new
if not os.path.exists(new_case_path):
    os.mkdir(new_case_path)
# 第七步：创建所有的用例数据yml文件的存放根目录
all_cases_gen_path = project_path + "06.UnitTest/01.UnitCases" + "/" + project
if not os.path.exists(all_cases_gen_path):
    os.makedirs(all_cases_gen_path)
#
cases_path = all_cases_gen_path + "/" + new
if not os.path.exists(cases_path):
    os.mkdir(cases_path)
# 创建单元测试用例的脚本文件存放根目录
script_gen_path = project_path + "06.UnitTest/02.UnitCasesScripts" + "/" + project
if not os.path.exists(script_gen_path):
    os.makedirs(script_gen_path)
# 当前版本的单元测试的脚本文件目录
script_path = script_gen_path + "/" + new
if not os.path.exists(script_path):
    os.mkdir(script_path)
# 创建单元测试用例的运行配置文件存放根目录
run_config_gen_path = project_path + "06.UnitTest/03.UnitTestRunConfig" + "/" + project
if not os.path.exists(run_config_gen_path):
    os.makedirs(run_config_gen_path)
# 当前版本的单元测试的运行配置文件目录
run_config_path = run_config_gen_path + "/" + new
if not os.path.exists(run_config_path):
    os.mkdir(run_config_path)
# 创建单元测试用例的测试数据，如：各种文件，存放根目录
data_gen_path = project_path + "06.UnitTest/04.UnitTestData" + "/" + project
if not os.path.exists(data_gen_path):
    os.makedirs(data_gen_path)
# 当前版本的单元测试的测试数据，如：各种文件，目录
data_path = data_gen_path + "/" + new
if not os.path.exists(data_path):
    os.mkdir(data_path)
# 创建单元测试用例的报告存放根目录
report_gen_path = project_path + "06.UnitTest/05.UnitTestReport" + "/" + project
if not os.path.exists(report_gen_path):
    os.makedirs(report_gen_path)
# 当前版本的单元测试报告目录
report_path = report_gen_path + "/" + new
if not os.path.exists(report_path):
    os.mkdir(report_path)
# 创建单元测试用例的日志存放根目录
log_gen_path = project_path + "06.UnitTest/06.UnitTestLog" + "/" + project
if not os.path.exists(log_gen_path):
    os.makedirs(log_gen_path)
# 当前版本的单元测试日志目录
log_path = log_gen_path + "/" + new
if not os.path.exists(log_path):
    os.mkdir(log_path)
# 创建xml_report_path目录
xml_report_path = report_path + "/xml"
if not os.path.exists(xml_report_path):
    os.makedirs(xml_report_path)
# 创建detail_report_path目录
detail_report_path = report_path + "/detail_report"
if not os.path.exists(detail_report_path):
    os.makedirs(detail_report_path)
# 创建summary_report_path目录
summary_report_path = report_path + "/summary_report_path/summary_report.html"
# 创建测试报告的运行环境配置目录
environment_properties_path = xml_report_path
if not os.path.exists(environment_properties_path):
    os.makedirs(environment_properties_path)
# 创建单元测试用例的环境配置文件存放根目录
env_config_gen_path = project_path + "06.UnitTest/07.UnitTestEnvConfig" + "/" + project
if not os.path.exists(env_config_gen_path):
    os.makedirs(env_config_gen_path)
# 当前版本的单元测试的数据库环境配置文件目录
db_env_path = env_config_gen_path + "/" + new
if not os.path.exists(db_env_path):
    os.mkdir(db_env_path)
# 当前版本的单元测试的服务环境配置文件目录
service_env_path = env_config_gen_path + "/" + new
if not os.path.exists(service_env_path):
    os.mkdir(service_env_path)
# 创建单元测试用例的依赖配置文件存放根目录
depent_gen_path = project_path + "06.UnitTest/08.UnitTestDepentData" + "/" + project
if not os.path.exists(depent_gen_path):
    os.makedirs(depent_gen_path)
# 当前版本的单元测试的依赖配置文件目录
depent_path = depent_gen_path + "/" + new
if not os.path.exists(depent_path):
    os.mkdir(depent_path)

# 生成测试用例脚本py文件
create_case_script(cases_path, new, script_path, project, db_env_path, run_config_path, service_env_path, depent_path, data_path)
