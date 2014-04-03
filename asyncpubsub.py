import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4
import json
import os
import torndb
import time
import redis
import logging
from sets import Set
class RenderFirebase(tornado.web.RequestHandler):
	def get(self):
		self.render('firebase.js')	
class SubscribeCart(object):
	
	callbacks = {}
	subscribers = {}
	timestamp=0
	Limit=20
	timestampnew=0
	
	def register(self,callback,subscribeChannel1):
		#debug here, the callbacks shouldn't be repeated
		subscribeChannel1=str(subscribeChannel1)
		self.callbacks.setdefault(subscribeChannel1,[]).append(callback)
		logging.info(self.callbacks)

	def addSubscription(self,subscribeChannel1,session):
		session=str(session)
		subscribeChannel1=str(subscribeChannel1)
		if subscribeChannel1 in self.subscribers:
			if session in self.subscribers[subscribeChannel1]:
				return

		self.subscribers.setdefault(subscribeChannel1,[]).append(str(session))
		logging.info(self.subscribers)
   
	def publishMessage(self, publishChannel1,publishObject1):
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		r.zadd(publishChannel1,time.time(),publishObject1)
		self.notifyCallbacks(str(publishChannel1))

	def notifyCallbacks(self,publishChannel1):
		if publishChannel1 in self.callbacks:
			logging.info("in if of notifyCallbacks")
			for c in self.callbacks[publishChannel1]:
				self.callbackHelper(c,publishChannel1)
			self.callbacks[publishChannel1]=[]

	def callbackHelper(self, callback,publishChannel1):
		logging.info("in callbackHelper")
		callback(self.getMessage(publishChannel1))

	def getMessage(self,Channel1):
		logging.info("in getMessage")
		str1=''
		# self.Channel1=Channel1
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		logging.info("outside check loop")
		# while self.timestampnew<=self.timestamp:
		# 	logging.info("new time " + str(timestampnew) + " old time "+ str(timestamp))

		# 	row=r.zrevrange(subscribeChannel1,0,0,withscores=True) 
		# 	if str(row)!='[]':
		# 		self.timestampnew=str(row[0][1])
		# 		time.sleep(2)
		# 	else:l
		# 		self.write('nothing in channel')
		# 		time.sleep(2)
		# loopfunc(subscribeChannel1,timestamp)
		row=r.zrevrange(Channel1,0,-1,withscores=True)
		for p in row:
			p="\"Obj\":"+str(p[0])+",\"Timestamp\":"+str(p[1])
			p='{'+p+'},'
			str1=str1+p
		str1=str1.strip(',')
		str1='['+str1+']'
		return str1
# class DetailHandler (tornado.web.RequestHandler):
# 	def get(self):
# 		session = uuid4()
# 		self.render("index.html", session=session)


class SubscriptionHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post (self):
		subscribeChannel1=self.get_argument('subscribeChannel1')
		session=self.get_argument('session')
		if not session:
			self.set_status(400)
			return
		else:
			self.application.subscribeCart.addSubscription(subscribeChannel1,session)
			self.application.subscribeCart.register(self.on_message,subscribeChannel1)
			
	def on_message(self,message):
		logging.info("on message invoked.. is something changed?")
		logging.info("new message: "+message)
		
		self.write(message)
		self.finish()


class PublishHandler(tornado.web.RequestHandler):
	def post(self):
		publishChannel1=self.get_argument('publishChannel1')
		publishObject1=self.get_argument('publishObject1')
		self.application.subscribeCart.publishMessage(publishChannel1,publishObject1)

# class Application(tornado.web.Application):
# 	def __init__(self):
# 		self.subscribeCart=SubscribeCart()
# 		logging.info("a new subsc object formed")
# 		handlers = [
# 		(r'/',DetailHandler),
# 		(r'/subscribe',SubscriptionHandler),
# 		(r'/publish',PublishHandler),
# 		(r"/firebase.js",RenderFirebase)
# 		] 

# 		settings =  {
# 		'template_path':'templates',
# 		'static_path':'static',
# 		'debug':True
# 		}

# 		tornado.web.Application.__init__(self,handlers,**settings)


# if __name__=='__main__':
# 	tornado.options.parse_command_line	()
# 	app=Application()
# 	server=tornado.httpserver.HTTPServer(app)
# 	server.listen(8002)
# 	tornado.ioloop.IOLoop.instance().start()
