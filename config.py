import json
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
from uuid import uuid4
class IndexHandler (tornado.web.RequestHandler):
	def get(self):
		self.render("index_n.html")

class RenderFirebase(tornado.web.RequestHandler):
	def get(self):
		self.render('firebase.js')
class RenderJquery(tornado.web.RequestHandler):
	def get(self):
		self.render('jquery.js')

class RenderInsertTesting(tornado.web.RequestHandler):
	def get(self):
		self.render('Insert_testing.html')

class RenderSearchTesting(tornado.web.RequestHandler):
	def get(self):
		self.render('search_testing.html')

class RenderInitFunc (tornado.web.RequestHandler):
	def post(self):
		session = uuid4()
		self.write(str(session))
