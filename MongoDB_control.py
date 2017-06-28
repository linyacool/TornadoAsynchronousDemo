#!/usr/bin/env python
#coding: utf-8
import pymongo
import motor
import bson

def ObjectID(id):
	return bson.objectid.ObjectId(id)

class MongoDB_orm_base(object):
	def __init__(self, mongo_control):
		self.db = mongo_control


class Control(object):
	def __init__(self, mongoClient):
		self.db = mongoClient

	# def ObjectId(id):
 #        return bson.objectid.ObjectId(id)
    
    # get one document
	async def get_document_one(self, condition, colName):
		document = await self.db[colName].find_one(condition)
		return document
        
    # get document List by condition, sortby, sort, limit, skip
	async def get_document_list(self, condition, sortby, sort, limit, skip, colName):
		sortlist = {
			'+':pymongo.ASCENDING ,
			'-':pymongo.DESCENDING
		}
		if condition == '':
			cursor = self.db[colName].find()
		else:
			cursor = self.db[colName].find(condition)
		cursor.sort(sortby, sortlist[sort]).limit(limit).skip(skip)
		documentlist = []
		async for document in cursor:
			documentlist.append(document)
		return documentlist
        
    # update document
	async def update(self, condition, document, colName):
		await self.db[colName].update(condition,document)
    
    # insert doucumnet
	async def insert(self, document, colName):
		result = await self.db[colName].insert(document)
		return result
    
    # delete document
	async def delete(self, condition, colName):
		await self.db[colName].delete_many(condition)