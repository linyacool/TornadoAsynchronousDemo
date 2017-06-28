#!/usr/bin/env python
#coding: utf-8
import os.path

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import MongoDB_ORM
import motor

define("port", default=80, help="run on the given port", type=int)

mongo_client = motor.MotorClient()

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/edit/([0-9Xx\-]+)", EditHandler),
			(r"/add", EditHandler),
			(r"/delete/([0-9Xx\-]+)", DelHandler),
			(r"/blog/([0-9Xx\-]+)", BlogHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
			db = MongoDB_ORM.MongoDB_ORM(mongo_client.demo2),
			)
		self.db = MongoDB_ORM.MongoDB_ORM(mongo_client.demo2)
		tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.settings['db']

class MainHandler(BaseHandler):
	async def get(self):
		import time
		blogs = await self.db.blog.get_all_blogs()
		self.render(
			"index.html",
			blogs = blogs,
			time = time,
		)
class EditHandler(BaseHandler):
	async def get(self, id=None):
		blog = dict()
		if id:
			blog = await self.db.blog.get_by_id(id)
		self.render("edit.html", blog = blog)

	async def post(self, id=None):
		import time
		blog = dict()
		if id:
			blog = await self.db.blog.get_by_id(id)
			# if '_id' not in blog:
			# 	self.redirect("/")
			# 	return
			blog.pop('_id')
		blog['title'] = self.get_argument("title", None)
		blog['content'] = self.get_argument("content", None)
		blog['date'] = int(time.time())
		if id:
			await self.db.blog.update(id, blog)
		else:
			blog['id'] = await self.db.blog.get_new_id()
			await self.db.blog.insert(blog)
		self.redirect("/")

class DelHandler(BaseHandler):
	async def get(self, id=None):
		if id:
			blog = await self.db.blog.delete(id)
		self.redirect("/")

class BlogHandler(BaseHandler):
	async def get(self, id=None):
		import time
		if id:
			blog = await self.db.blog.get_by_id(id)
			self.render("blog.html",
				page_title = "我的博客",
				blog = blog,
				time = time,
				)
		else:
			self.redirect("/")

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()
