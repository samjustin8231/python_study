#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime, date


print "hello world!",
print "sam"
print "%s %d" % ('Zara', 21)

##
for i in range(2, 5):
    print i
else:
    pass

##
bb = "my name is sam.";
print bb.title();

##
L = [5, 3, 6, 3, 2]
print max(L)

##
a = """
    <HTML><HEAD><TITLE>
    Friends CGI Demo</TITLE></HEAD>
    <BODY><H3>ERROR</H3>
    <B>%s</B><P>
    <FORM><INPUT TYPE=button VALUE=Back
    ONCLICK="window.history.back()"></FORM>
    </BODY></HTML>
"""
print a



dayOfWeek = datetime.now().weekday()
print(dayOfWeek)

dayOfWeek = datetime.today().weekday()
print(dayOfWeek)

