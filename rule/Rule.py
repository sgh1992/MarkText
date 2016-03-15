# !/usr/bin/python
#  -*- coding: utf-8 -*-

class Rule(object):
    """
    是所有规则的超类.
    """

    def condition(self, block):
        """
        :param type:根据对应的类型来判断是否与条件相符.
        :return: 返回匹配结果,匹配则返回True,否则则返回False
        """
        return True

    def action(self, block, handler):
        """

        :param block: 需要处理的文本字符串.
        :param handler: 根据给定的处理器对字符串进行处理.
        :return: 判定当前规则是否应该停止.
        主要针对的是列表规则,当发现当前block是列表之后,但是其后续的block可能也是列表,而列表只是添加一个结尾标志位.
        规则的顺序很重要.
        """
        handler.start(self.type)  # 运用了多态的处理方式,这里的type根据子类而进行具体操作.
        handler.feed(block)
        handler.end(self.type)
        return True


class HeadRule(Rule):
    """
    标题的规则
    1.不能包含換行符
    2.最后一个字符不能是:
    3.整个字符的长度不能超过70.
    """
    type = "head"

    def condition(self, block):
        return '\n' not in block and len(str(block)) <= 70 and not block[-1] == ':'


class TitleRule(Rule):
    type = "title"
    first = True

    def condition(self, block):
        if not self.first:
            return False
        self.first = False
        return HeadRule().condition(block)


class ListItemRule(Rule):
    type = "listItem"

    def condition(self, block):
        if str(block).startswith("-"):
            return True
        return False

    def action(self, block, handler):
        block = block[1:]
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True


class ListRule(Rule):
    type = "list"
    inside = False

    def condition(self, block):
        return True

    def action(self, block, handler):

        if not self.inside and ListItemRule().condition(block):
            self.inside = True
            handler.start(self.type)
        elif self.inside and not ListItemRule().condition(block):
            handler.end(self.type)
            self.inside = False
        return False


class ParagraphRule(Rule):
    type = "paragraph"
    def condition(self, block):
        return True



