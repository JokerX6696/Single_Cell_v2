#!/data/software/miniconda/envs/snakemake/bin/python
import yaml
import os, sys
import single_cell_auto
##  根据需求生成对应的脚本
# 获取命令行参数
args = sys.argv[1:]
# config='D:/desk/github/Single_Cell_v2/test.yaml'
config = args[0]
config_path = os.path.dirname(config)  # 生成文件与 config 文件同目录
# 读取 YAML 文件
def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
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
### run 

if p.diff_anno.run:
    single_cell_auto.diff_anno_run(
        input_rds = p.diff_anno.input_rds,
        cell_types = p.diff_anno.cell_types,
        analysis_type = p.diff_anno.analysis_type,
        treat = p.diff_anno.treat,
        control = p.diff_anno.control,
        fc = p.diff_anno.fc,
        p = p.diff_anno.p,
        vs_type = p.diff_anno.vs_type,
        anno = p.diff_anno.anno,
        out = config_path  
    )
        
    