#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 导入模块
import support
from CallData import postman_map

# 现在可以调用模块里包含的函数了
support.print_func("Runoob")
print postman_map.postman_node_map

content = dir(support)
print content;