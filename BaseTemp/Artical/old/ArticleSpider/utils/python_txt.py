#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/14/17 6:41 AM
# @Author  : Yang

class Sanyuan(object):

    def __init__(self):
        name = 'sanyuan'

    @property
    def name(self):
        pass

# a = 2 if b = 3 else a =5

# a = map(lambda x:x+2,[1,23,4,5])
#
# b = [i+5 for i in a]
# print(b)
#
# def han(a,b):
#
#     def han2(x):
#         y = a * x + b
#         print(y)
#
#     return han2
#
# han1 = han(3,4)
# han1(3)
#
#
# def wrapper(func):
#
#     def func1(a,b):
#         print('-----')
#         func(a,b)
#         print('-----')
#
#     return func1
#
# @wrapper
# def name(a,b):
#     c = a + b
#     print(c)
#
# name(1,2)

class test(object):

    def name(self,name):
        print(name)

    def get_name(self,name):
        print('-------')
        self.name(name)
        print('-----')


yang = test()
yang.get_name('yang')


