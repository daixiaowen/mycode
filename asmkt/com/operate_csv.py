# coding:utf-8

import csv


class Operate_csv(object):
    '''读写csv'''
    def __init__(self, filename, headers_list, row_list):
        self.filename = filename
        self.headers_list = headers_list
        self.row_list = row_list

    def write_headers(self):
        '''
        写入头部信息
        :param args:
        :return:
        '''
        headers = []
        headers.append(self.headers_list)
        return headers

    def write_rows(self):
        row = [[row] for row in self.row_list]
        return row

    def write_csv(self):
        '''
        :param headers:headers是一个列表
        :param rows_list:rows_list是一个二维数组(sign)
        :return: 无返回值
        '''
        with open(self.filename, 'w', newline='')as f:
            '''newline=""为了避免写入有空格'''
            f_csv = csv.writer(f)
            f_csv.writerow(self.write_headers())
            f_csv.writerows(self.write_rows())

    def read_csv(self):
        '''return:返回一个列表'''
        with open(self.filename, 'r') as f:
            f_csv = csv.reader(f)
            L = []  # 定义一个空列表，用来存放从csv文件中获取到的值
            for ase_key in f_csv:
                  L.append(ase_key)
        return L[1:]  # 去掉头字段
