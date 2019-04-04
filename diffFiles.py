#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
   Create a file named 'result.html' which is as a result after two files diffing
   Usage:
       ./diffFiles.py file1 file2
"""
import difflib,sys

try:
    file1=sys.argv[1]
    file2=sys.argv[2]
except Exception as e:
    print('Error:%s' %str(e))
    print('Usage: ./diffFiles.py file1 file2')
    sys.exit()

def readfile(filename):
    try:
        openfile = open(filename,'r')
        text=openfile.read().splitlines()
        openfile.close()
        return text
    except IOError as error:
        print('Read file Error:%s' %str(error))
        sys.exit()

if file1 == "" or file2 == "":
    print('Usage: ./diffFiles.py file1 file2')
    sys.exit()

file1_line = readfile(file1)
file2_line = readfile(file2)
d=difflib.HtmlDiff()
with open('result.html','w') as f:
    f.write(d.make_file(file1_line,file2_line))
