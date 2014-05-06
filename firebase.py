import json
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import torndb
import time
import redis
from tornado.options import define,options
import logging
from uuid import uuid4
from sets import Set
import asyncpubsub
import config
import database

define("port",default=8002,help="tornado will run on the given port",type=int)

class Application(tornado.web.Application):
	def __init__(self):
		self.subscribeCart=asyncpubsub.SubscribeCart()
		logging.info("a new subsc object formed")
		handlers=[(r"/",config.IndexHandler),(r"/insert",database.DbInsert),
		(r"/query",database.DbQuery),(r"/search",database.DbSearch),(r"/remove",database.DbRemove),(r"/indexKey",database.DbIndex),
		(r"/publish",asyncpubsub.PublishHandler),(r"/removeps",asyncpubsub.RemoveHandler),(r"/removepsbykey",asyncpubsub.RemoveHandlerByKey),
		(r"/subscribe",asyncpubsub.SubscriptionHandler),(r"/unsubscribeChannel",asyncpubsub.UnsubscriptionHandler),
		(r"/firebase.js",config.RenderFirebase),(r"/jquery.js",config.RenderJquery),(r"/initfunc",config.RenderInitFunc),
		(r"/insertTesting",config.RenderInsertTesting),(r"/searchTesting",config.RenderSearchTesting)] 

		settings =  {
		'template_path':'templates',
		'static_path':'static',
		'debug':True
		}

		tornado.web.Application.__init__(self,handlers,**settings)

if __name__=='__main__':
	tornado.options.parse_command_line	()
	db = torndb.Connection("localhost", "tordata",user="root",password="ksh")
	app=Application()
	server=tornado.httpserver.HTTPServer(app)
	server.listen(8002)
	tornado.ioloop.IOLoop.instance().start()

	