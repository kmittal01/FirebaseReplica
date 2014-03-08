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
define("port",default=8000,help="tornado will run on the given port",type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')
class RenderFirebase(tornado.web.RequestHandler):
	def get(self):
		self.render('firebase.js')	
class DbInsert(tornado.web.RequestHandler):
	def post(self):
		object1=self.get_argument('object')
		type1=self.get_argument('type')
		db.execute("Insert into Obj_Table (`J_Obj`,`Type`,`Timestamp`) Values (%s,%s,%s)",object1,type1,time.time() )
		json_data=json.loads(object1)
		row=db.query("select * from Obj_Table Order by id desc")
		new_id=row[0].Id
		self.write(str(row[0].Id))
		indexkeys=list()
		noIndex=True
		for row in db.query("Select * from IndexTable Where Type=\""+type1+"\""):
			indexkeys.append(str(row.Index))
			noIndex=False
		if noIndex:
			for k,v in json_data.items():
				db.execute("Insert into KeyValueTable Values(%s,%s,%s)",new_id,k,v )
		else: 
			for k,v in json_data.items():
				if (indexkeys.count(k)!=0):
					db.execute("Insert into KeyValueTable Values(%s,%s,%s)",new_id,k,v )
class DbQuery(tornado.web.RequestHandler):
	def post(self):
		a=''
		id1=self.get_argument('Id1')
		id1='('+id1+')'
		for row in db.query("Select * from Obj_Table where Id In "+id1):
			a=a+("{\"Id\":"+str(row.Id) +",\"Obj\":"+ str(row.J_Obj)+",\"Type\":\""+str(row.Type)+"\",\"Timestamp\":\""+str(row.Timestamp)+"\"},")
		a=a.strip(',')
		a='['+a+']'
		self.write((a))
class DbSearch(tornado.web.RequestHandler):
	def post(self):
		key1=self.get_argument('key1')
		value1=self.get_argument('value1')
		parameter1=self.get_argument('parameter1')
		gle1=self.get_argument('gle1')
		gle2=self.get_argument('gle2')
		pValue1=self.get_argument('parameterValue1')
		limit1=self.get_argument('limit1')
		if limit1=='*':
			limit1='30'
		a=list()
		for row in db.query("Select * from KeyValueTable where `Key` ='" +str(key1)+"' and `Value` "+gle2+" '"+str(value1)+"' Limit "+limit1):
			a.append(str(row.Id))
		a=tuple(a)
		a=str(a)
		#self.write(a)
		if(a=='()'):
			str1="[{\"Id\":null,\"Obj\":null,\"Type\":null,\"Timestamp\":null}]"
			self.write(str1)
		else:
			if bool(a.strip(',)')):
				a=a.strip(',)')
				a=a+')'
			str1=''
			for row in db.query("Select * from Obj_Table where Id IN "+str(a)+" and `"+str(parameter1)+"`" +gle1+ "\""+str(pValue1)+"\"" ):
					str1=str1+ ("{\"Id\":"+str(row.Id) +",\"Obj\":"+ str(row.J_Obj)+",\"Type\":\""+str(row.Type)+"\",\"Timestamp\":\""+str(row.Timestamp)+"\"},")
			if(str1!=''):
				str1=str1.strip(',')
				str1='['+str1+']'
				self.write(str1)
			else:
				str1=str1+ ("{\"Id\":null,\"Obj\":null,\"Type\":null,\"Timestamp\":null}")
class DbRemove (tornado.web.RequestHandler):
	def post(self):
		removeId1=self.get_argument('removeId1')
		self.write(removeId1)
		removeId1='('+removeId1+')'
		db.execute("DELETE FROM Obj_Table WHERE Id IN "+removeId1)
		db.execute("DELETE FROM KeyValueTable WHERE Id IN "+removeId1)
class DbIndex (tornado.web.RequestHandler):
	def post(self):
		type1=self.get_argument('type1')
		index1=self.get_argument('index1')
		db.execute("Insert into IndexTable Values (\""+type1+"\",\""+index1+"\")")
		self.write(index1+" indexed for "+type1)
		#self.render('index.html')
class RedisPublish(tornado.web.RequestHandler):
	def post(self):
		publishObject1=self.get_argument('publishObject1')
		publishChannel1=self.get_argument('publishChannel1')
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		r.zadd(publishChannel1,time.time(),publishObject1)
		self.write("published")
		logging.info("published")
class RedisSubscribe(tornado.web.RequestHandler):
	def post(self):	
		logging.info("inside subscribe")
		subscribeChannel1=self.get_argument('subscribeChannel1')
		subscribeLimit1=self.get_argument('subscribeLimit1')
		timestamp=self.get_argument('timestamp')
		str1=''
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		timestampnew=0
		logging.info("outside check loop")
		while timestampnew<=timestamp:
			logging.info("inside check loop")
			logging.info("new time " + str(timestampnew) + " old time "+ str(timestamp))

			row=r.zrevrange(subscribeChannel1,0,0,withscores=True) 
			if str(row)!='[]':
				timestampnew=str(row[0][1])
				time.sleep(2)
			else:
				self.write('nothing in channel')
				time.sleep(2)
		# loopfunc(subscribeChannel1,timestamp)
		row=r.zrevrange(subscribeChannel1,0,-1,withscores=True)
		for p in row:
			p="\"Obj\":"+str(p[0])+",\"Timestamp\":"+str(p[1])
			p='{'+p+'},'
			str1=str1+p
		str1=str1.strip(',')
		str1='['+str1+']'
		self.write(str1)
if __name__ == "__main__":
	tornado.options.parse_command_line()
	db = torndb.Connection("localhost", "tordata",user="root",password="ksh")
	app=tornado.web.Application(
		handlers=[(r"/",IndexHandler),(r"/insert",DbInsert),(r"/query",DbQuery),
		(r"/search",DbSearch),(r"/remove",DbRemove),(r"/indexKey",DbIndex),
		(r"/publish",RedisPublish),(r"/subscribe",RedisSubscribe),(r"/firebase.js",RenderFirebase)],
		template_path=os.path.join(os.path.dirname(__file__),"templates"),
		static_path=os.path.join(os.path.dirname(__file__), "static"),
		debug=True
		)
	http_server=tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
	