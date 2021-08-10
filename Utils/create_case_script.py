# coding:utf-8
# @Author: wang_cong
import os
from Utils.operation_dir import create_every_path_dirs
from Utils.operation_log import initLogger

logger = initLogger(__file__)


def create_case_script(unit_case_path, new, unit_script_path, project, db_env_path, run_config_path, service_env_path, depent_path, data_path):
    """

    :param unit_case_path:
    :param new:
    :param unit_script_path:
    :param project:
    :param db_env_path:
    :param run_config_path:
    :param service_env_path:
    :param depent_path:
    :param data_path:
    :return:
    """
    # 注意：根据测试用例yaml文件的存放目录，判断有几个yaml文件，即表示有几个测试用例，便需要创建几个py文件

    # template文件的路径
    root_path = os.path.dirname(os.path.dirname(__file__))
    template_py_file_path = root_path + '/Template/case_script_template.py'
    with open(template_py_file_path, 'r', encoding='utf-8') as tem_file:
        template_py_file_content = tem_file.readlines()
    for root, dirs, files in os.walk(unit_case_path):
        for dir in dirs:
            dd = os.path.join(root, dir)
            ll = os.listdir(dd)
            for data in ll:
                if data.endswith(".yml"):
                    yml_file_name = data.split(".yml")[0]
                    ff = dd.split(new)[-1].replace("\\", "/")
                    create_every_path_dirs(unit_script_path, ff)
                    # 构造py文件名称
                    ss = ff.replace("\\", "/").split("/")[1:]
                    py_file_name = ""
                    for name in ss[:-1]:
                        py_file_name = py_file_name + "_" + name
                    py_file_name = "test" + py_file_name + "_" + yml_file_name + ".py"
                    # 完整的py文件路径名称
                    py_file_path = unit_script_path + ff
                    py_file = py_file_path.replace("\\", "/") + "/" + py_file_name
                    interface_module_name = ff.split('/')[1:]
                    module_name = ''
                    for module in interface_module_name:
                        module_name = module_name + module[:1].upper() + module[1:]
                    case_path = unit_case_path + ff
                    sql_path = data_path + ff
                    # 准备生成测试用例脚本py文件
                    with open(py_file, 'w', encoding='utf-8') as py_f:
                        for line in template_py_file_content:
                            if 'project = "template"' in line:
                                line = line.replace('template', project)
                                py_f.write(line)
                            elif 'db_env_path = "template"' in line:
                                line = line.replace('template', db_env_path.replace("\\", "/"))
                                py_f.write(line)
                            elif 'run_config_path = "template"' in line:
                                line = line.replace('template', run_config_path.replace("\\", "/"))
                                py_f.write(line)
                            elif 'service_env_path = "template"' in line:
                                line = line.replace('template', service_env_path.replace("\\", "/"))
                                py_f.write(line)
                            elif 'case_path = "template"' in line:
                                line = line.replace("template", case_path.replace("\\", "/"))
                                py_f.write(line)
                            elif 'case_file_name = "template"' in line:
                                line = line.replace('template', yml_file_name)
                                py_f.write(line)
                            elif 'depent_path = "template"' in line:
                                line = line.replace('template', depent_path.replace("\\", "/"))
                                py_f.write(line)
                            elif 'sql_path = "template"' in line:
                                line = line.replace('template', sql_path.replace("\\", "/"))
                                py_f.write(line)
                            elif 'class TestTemplate' in line:
                                line = line.replace('Template', module_name.replace('-', ''))
                                py_f.write(line)
                            elif 'def test_template' in line:
                                line = line.replace('test_template', py_file_name.split(".py")[0])
                                py_f.write(line)
                            else:
                                py_f.write(line)

                    # 准备生成__init__文件
                    # py_init_file = py_file_path.replace("\\", "/") + "/" + "__init__.py"
                    # if not os.path.exists(py_init_file):
                    #     with open(py_init_file, 'w', encoding='utf-8') as py_init_f:
                    #         py_init_f.write("")

                    # 准备生成conftest.py文件
                    # py_conf_file = py_file_path.replace("\\", "/") + "/" + "conftest.py"
                    # if not os.path.exists(py_conf_file):
                    #     with open(py_conf_file, 'w', encoding='utf-8') as py_conf_f:
                    #         py_conf_f.write("")




