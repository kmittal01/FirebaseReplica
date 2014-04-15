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
		session = uuid4()
		self.render("index_n.html", session=session)

class RenderFirebase(tornado.web.RequestHandler):
	def get(self):
		self.render('firebase.js')
class RenderJquery(tornado.web.RequestHandler):
	def get(self):
		self.render('jquery.js')