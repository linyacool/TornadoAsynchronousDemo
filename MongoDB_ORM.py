#!/usr/bin/env python
#coding: utf-8
import MongoDB_control
import blog

class MongoDB_ORM(object):
	def __init__(self, mongodb):
		control = MongoDB_control.Control(mongodb)
		self.blog = blog.Blog(control)