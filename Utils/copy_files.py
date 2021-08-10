# coding:utf-8
# @Author: wang_cong
# @File: copy_files.py
# @Project: AutoCreateCaseTool
# @Time: 2021/6/1 15:03
import os
import shutil


def copy_all_files(source_path, target_path, old_version):

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    if os.path.exists(source_path):
        # root 所指的是当前正在遍历的这个文件夹的本身的地址
        # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
        # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
        for root, dirs, files in os.walk(source_path):
            for file in files:
                src_file = os.path.join(root, file)
                address = src_file.split(old_version)[-1]
                dst_path = target_path + address
                # 判断目录是否在目标目录存在，不存在的话，说明，就被抛弃了，不需要复制过来
                pp = "/".join(str(address).split("\\")[:-1])
                if os.path.exists(target_path + pp):
                    shutil.copy(src_file, dst_path)
