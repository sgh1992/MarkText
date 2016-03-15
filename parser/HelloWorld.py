# !/usr/bin/python
#  -*- coding: utf-8 -*-
import sys
#sys.path.append('/home/sghipr/PycharmProjects/MarkText/handler')
from handler import Handler
print 'Hello,World!'
handlerTest = Handler.HTMLHandler()
handlerTest.start_document()
def good():
    print 'Good'
