# -*- coding:utf-8 -*-
# Author : oldman
# License : (C) Copyright 2015-2017, minivision
import re


def get_num(strs):
    num = re.match('.*?(\d+).*',strs).group(1)
    return num


if __name__ =='__main__':
    pass