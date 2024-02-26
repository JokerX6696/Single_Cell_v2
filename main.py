#!/data/software/miniconda/envs/snakemake/bin/python
import yaml
import os, sys
import single_cell_auto
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

if p.cellchat.run:
    single_cell_auto.cellchat_run(obj=p)

