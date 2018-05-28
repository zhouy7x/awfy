#!/usr/bin/python 
import urllib

f = urllib.urlopen("http://www.baidu.com")
print f.read()


