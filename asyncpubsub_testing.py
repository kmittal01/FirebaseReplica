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
		subscribeChannel1=str(subscribeChannel1)
		self.callbacks.setdefault(subscribeChannel1,[]).append(callback)

	def addSubscription(self,subscribeChannel1,session):
		session=str(session)
		subscribeChannel1=str(subscribeChannel1)
		if subscribeChannel1 in self.subscribers:
			if session in self.subscribers[subscribeChannel1]:
				return

		self.subscribers.setdefault(subscribeChannel1,[]).append(str(session))

	def removeSubscription(self,unsubscribeChannel,session):
		session=str(session)
		unsubscribeChannel=str(unsubscribeChannel)
		if unsubscribeChannel in self.subscribers:
			if session in self.subscribers[unsubscribeChannel]:
				self.subscribers[unsubscribeChannel].remove(str(session))
			else:
				logging.info("sorry, you are not subscribed to this channel")
		else:
			logging.info("Sorry, no channel like this exists")

   
	def publishMessage(self, publishChannel1,publishObject1):
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		r.zadd(publishChannel1,time.time(),publishObject1)
		self.notifyCallbacks(str(publishChannel1))

	def RemoveMessage(self,channel1,rankStart1,rankEnd1):
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		if r.exists(channel1):
			r.zremrangebyrank(channel1,rankStart1,rankEnd1)
			self.notifyCallbacks(str(channel1))
		else:
			logging.info("the channel doesn't exists")

	def RemoveMessageByKey(self,channel1,key):
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		if r.exists(channel1):
			r.zrem(channel1,key)
			self.notifyCallbacks(str(channel1))
		else:
			logging.info("the channel doesn't exists")


	def notifyCallbacks(self,publishChannel1):
		if publishChannel1 in self.callbacks:
			for c in self.callbacks[publishChannel1]:
				self.callbackHelper(c,publishChannel1)
			self.callbacks[publishChannel1]=[]

	def callbackHelper(self, callback,publishChannel1):
		callback(self.getMessage(publishChannel1))

	def getMessage(self,Channel1):
		str1=''
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		count=r.zcard(str(Channel1))
		row=r.zrevrange(Channel1,0,-1,withscores=True)
		for p in row:
			p="\"Rank\":"+str(int(count)-1)+",\"Obj\":"+str(p[0])+",\"Timestamp\":"+str(p[1])
			p='{'+p+'},'
			str1=str1+p
			count=str(int(count)-1)
		str1=str1.strip(',')
		str1='['+str1+']'
		return str1

class SubscriptionHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post (self):
		subscribeChannel1=self.get_argument('subscribeChannel1')
		session=self.get_argument('session')
		if not session:
			self.set_status(400)
			return
		else:
			start= time.clock()
			for i in range (500):
				session = uuid4()
				self.application.subscribeCart.addSubscription(subscribeChannel1,session)
				self.application.subscribeCart.register(self.on_message,subscribeChannel1)
			end= time.clock()
			timediff= (end-start)
			logging.info("time taken:"+str(timediff))
	def on_message(self,message):
		pass
		logging.info(time.clock())
		# self.write(message)
		# self.finish()


class PublishHandler(tornado.web.RequestHandler):
	def post(self):
		publishChannel1=self.get_argument('publishChannel1')
		publishObject1=self.get_argument('publishObject1')
		self.application.subscribeCart.publishMessage(publishChannel1,publishObject1)

class RemoveHandler(tornado.web.RequestHandler):
	def post(self):
		logging.info("in remove handler")
		channel1=self.get_argument('removeChannel1')
		rankStart1=self.get_argument('rankStart1')
		rankEnd1=self.get_argument('rankEnd1')
		self.application.subscribeCart.RemoveMessage(channel1,rankStart1,rankEnd1)

class RemoveHandlerByKey(tornado.web.RequestHandler):
	def post(self):
		channel1=self.get_argument('removeChannel1')
		key=self.get_argument('key')
		self.application.subscribeCart.RemoveMessageByKey(channel1,key)

class UnsubscriptionHandler(tornado.web.RequestHandler):
	def post(self):
		unsubscribeChannel=self.get_argument('unsubscribeChannel')
		session=self.get_argument('session')
		self.application.subscribeCart.removeSubscription(unsubscribeChannel,session)
		
