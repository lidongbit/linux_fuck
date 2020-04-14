# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:49:14 2020

@author: 62807
@function: increase tab_num automatically
"""

import re,sys,operator
from sys import argv


list_tmp= []
def get_tab_num(tab):
    new = []
    new.append(re.findall(r'\D+',tab)[0]) #非数字
    new.append(re.findall(r"\d+",tab)[0])
    return new

argc = int(len(argv))
if argc<3:
	print('Usage: python 0-%s 1-file_name 2-tab_name [3-begin_num]!'%argv[0])
	sys.exit()
	
fold = open('%s'%argv[1], 'r')
fnew = open('config_new.ini','w')


list_tmp = get_tab_num(argv[2])
numb = int(list_tmp[1])
print(numb)

flag = 0
for line in fold:
    if line.find(list_tmp[0]) != -1:
        if get_tab_num(line)[1] == list_tmp[1]:
            print("first find !")
            flag = 1
        if flag == 1:
            string = re.sub(r'\d+', str(numb), line)
            numb += 1
            fnew.write(string)
            continue
    fnew.write(line)

fold.close()
fnew.close()
    
