#!/usr/bin/env python
#coding: utf-8
from MongoDB_control import MongoDB_orm_base, ObjectID

class Blog(MongoDB_orm_base):
	def __init__(self, mongo_control):
		MongoDB_orm_base.__init__(self, mongo_control)
		self.colName = 'blog'

	async def get_all_blogs(self):
		blogs_list = await self.db.get_document_list('', 'date', '-', 20, 0, self.colName)
		return blogs_list

	# not _id
	async def get_by_id(self, id):
		condition = {'id':int(id)}
		blog = await self.db.get_document_one(condition, self.colName)
		return blog

	async def update(self, id, blog):
		condition = {'id':int(id)}
		blog = {'$set':blog}
		await self.db.update(condition, blog, self.colName)

	async def insert(self, blog):
		await self.db.insert(blog, self.colName)

	async def delete(self, id):
		condition = {'id':int(id)}
		await self.db.delete(condition, self.colName)

	async def get_new_id(self):
		blog = await self.db.get_document_list('', 'id', '-', 1, 0, self.colName)
		if len(blog) == 0:
			return 1
		return blog[0]['id'] + 1
