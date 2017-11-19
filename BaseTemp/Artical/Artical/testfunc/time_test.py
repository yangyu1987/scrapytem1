#! -*- coding:utf-8 -*-
import time
import random

# print('random'+':{0}'.format(random.random()))
# print('randomint'+':{0}'.format(random.randint(1,8)))
# print(random.randrange(10,20,5))
# # print(random.)
# print (random.choice("学习Python"))
# print (random.choice(["JGood", "is", "a", "handsome", "boy"]))
# print (random.choice(("Tuple", "List", "Dict")))

# while True:
#     random.seed
#     time.sleep(random.random())
#     print(random.random())

def foo(a,b,*c):
    print(a)
    print(b)
    print(c)

foo(1,2,3,4,5)