# !/usr/bin/python
#  -*- coding: utf-8 -*-
import sys
import re

sys.path.append('/home/sghipr/PycharmProjects/MarkText/handler')
sys.path.append('/home/sghipr/PycharmProjects/MarkText/readText')
sys.path.append('/home/sghipr/PycharmProjects/MarkText/rule')

from handler import Handler
from rule import Rule
from readText import util


class Parser(object):
    def __init__(self, handler):
        self.rules = []
        self.filters = []
        self.handler = handler

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        # print name
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)

        self.filters.append(filter)

    def parser(self, file):
        self.handler.start('document')
        for block in util.blocks(file):
            # print 'current block',block
            for filterV in self.filters:
                block = filterV(block, self.handler)
                # print 'after filter',block
            for rule in self.rules:
                if rule.condition(block):
                    flag = rule.action(block, self.handler)
                    if flag:
                        break

        self.handler.end('document')


class basicParser(Parser):
    def __init__(self, handler):
        super(basicParser, self).__init__(handler)
        self.addRule(Rule.ListRule())
        self.addRule(Rule.ListItemRule())
        self.addRule(Rule.TitleRule())
        self.addRule(Rule.HeadRule())
        self.addRule(Rule.ParagraphRule())

        self.addFilter(r'\*(.+?)\*', 'emphasize')
        self.addFilter(r'(http://[\.a-zA-Z]+)', 'url')
        self.addFilter(r'([a-zA-Z]+@[\.a-zA-Z]+)', 'mail')

    def transfer(self, sourcefile, destfile):
        """
        数据流重定向.
        :param sourcefile:
        :param destfile:
        :return:
        """
        old_stdin = sys.stdin
        sys.stdin = open(sourcefile, 'r')
        old_stdout = sys.stdout
        sys.stdout = open(destfile, 'w')
        self.parser(sys.stdin)
        # sys.stdout.close()
        sys.stdin = old_stdin
        sys.stdout = old_stdout


def test(sourcefile, destfile):
    basicParserTest = basicParser(Handler.HTMLHandler())
    basicParserTest.transfer(sourcefile, destfile)
