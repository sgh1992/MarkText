# !/usr/bin/python
#  -*- coding: utf-8 -*-

"""
从文件中读取所有的数据.
"""


def lines(files):
    for line in files:
        yield line
    yield '\n'


def blocks(files):
    block = []
    for line in lines(files):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []

