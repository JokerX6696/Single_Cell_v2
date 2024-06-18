#!D:/Application/python/python.exe
# -*- coding: utf-8 -*-
import yaml
import os, sys
import single_cell_auto  # 尝试更加模块化
##  根据需求生成对应的脚本
# 获取命令行参数
args = sys.argv[1:]
# config='D:/desk/github/Single_Cell_v2/test.yaml'
config = args[0]
config_path = os.path.dirname(os.path.abspath(config))  # 生成文件与 config 文件同目录
# 读取 YAML 文件
def read_yaml_file(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

###  定义类 将 yaml 递归创建至 类中
class Project:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                setattr(self, key, Project(**value))
            else:
                setattr(self, key, value)
### yaml 转化为类属性
yaml_data = read_yaml_file(config)
# 创建类的实例，并将字典中的键值对应于类的属性
p = Project(**yaml_data)
p.out = config_path
### run
# 差异 富集
if p.diff_anno.run:
    single_cell_auto.diff_anno_run(obj=p)
# cellchat
if p.cellchat.run:
    single_cell_auto.cellchat_run(obj=p)
# GSVA
if p.gsva.run:
    single_cell_auto.gsva_run(obj=p)
# 修改细胞类型
if p.modified_cell_type.run:
    single_cell_auto.modified_cell_type_run(obj=p)
# monocle
if p.monocle2.run:
    single_cell_auto.monocle2_run(obj=p)
# scvelo
if p.scvelo_py.run:
    single_cell_auto.scvelo_py_run(obj=p)
# sub_clusters
if p.sub_clusters.run:
    single_cell_auto.sub_clusters_run(obj=p)
# SCENIC
if p.scenic.run:
    single_cell_auto.scenic_run(obj=p)
# inferCNV
if p.inferCNV.run:
    single_cell_auto.inferCNV_run(obj=p)  

