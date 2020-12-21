#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Time     :2019/8/10
@Name     :ZhangWei
@Contact  :1223242863@qq.com
@File     :regex2list.py
@Software :Pycharm
"""

import re
import itertools


# 遍遍历多个列表元素的所有组合
class Regex2List(object):
    def __init__(self, regex_path, regex_list):
        self.regex_path = regex_path
        self.regex_list = regex_list

    @staticmethod
    def get_list(str_list):
        res, data = [], ['']
        for line in str_list:
            if line == '':
                continue
            else:
                data = itertools.product(data, line.split('|'))
        for result in data:
            res.append(''.join(re.findall(r'[\u4e00-\u9fa5]', str(result))))
        print(res)
        return res

    def run(self):
        res_list = []
        with open(self.regex_path, 'r', encoding='utf-8') as file:
            for line in file:
                print(line)
                data = re.split("|".join(self.regex_list), line[:-1])
                for res in self.get_list(data):
                    res_list.append(res)
        return res_list


if __name__ == "__main__":
    rl = Regex2List(regex_path="regex.txt", regex_list=["\(", "\)", "\+", "\（", "\）"])
    for res in rl.run():
        print(res)