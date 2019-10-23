# coding:utf-8


import yaml


class OperateYaml():
    def __init__(self, filename):
        self.filename = filename

    def read_yaml(self):
        '''读取yaml文件'''
        with open(self.filename, "r") as y:
            yaml.warnings({"YAMLLoadWarning": False})
            res = yaml.load(y)
        return res

    def write_yaml(self, dict_list):
        '''写入yaml文件'''
        with open(self.filename, "a", newline="\n") as y:
            yaml.dump(dict_list, y)

o = OperateYaml(r"F:\mycode\asmkt\config\urls.yaml")
