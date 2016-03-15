# !/usr/bin/python
#  -*- coding: utf-8 -*-


class Handler(object):
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, *args)
        if callable(method):
            return method(*args)

    def start(self, name):
        return self.callback("start_", name)

    def end(self, name):
        return self.callback("end_", name)

    def sub(self, name):

        def substitute(match):
            result = self.callback("sub_", name, match)
            if result is None:
                return match.group(0)
            return result

        return substitute

    def feed(self, block):
        print block

class HTMLHandler(Handler):

    def start_paragraph(self):
        print '<p>'

    def end_paragraph(self):
        print '</p>'

    def start_head(self):
        print '<h2>'

    def end_head(self):
        print '</h2>'

    def start_document(self):
        print '<html><head><title>...</title></head><body>'

    def end_document(self):
        print '</body></html>'

    def start_title(self):
        print '<h1>'

    def end_title(self):
        print '</h1>'

    def start_listItem(self):
        print '<ul>'

    def end_listItem(self):
        print '</ul>'

    def start_list(self):
        print '<li>'

    def end_list(self):
        print '</li>'

    def sub_emphasize(self, match):
        return '<em>%s</em>' % (match.group(1))

    def sub_url(self,match):
        return '<a href = %s>%s</a>' % (match.group(1), match.group(1))

    def sub_mail(self,match):
        return '<a href = mailto:%s>%s</a>' % (match.group(1), match.group(1))



