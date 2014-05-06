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
import asyncpubsub
import config
from uuid import uuid4
from sets import Set
db = torndb.Connection("localhost", "tordata2",user="root",password="ksh")
class DbInsert(tornado.web.RequestHandler):
	def post(self):
		object1=self.get_argument('object')
		type1=self.get_argument('type')
		app_id=self.get_argument('app_id')
		db.execute("Insert into Obj_Table (`J_Obj`,`Type`,`App_Id`,`Timestamp`) Values (%s,%s,%s,%s)",object1,type1,app_id,time.time() )
		json_data=json.loads(object1)
		row=db.query("select * from Obj_Table Order by id desc")
		new_id=row[0].Id
		self.write(str(row[0].Id))
		indexkeys=list()
		noIndex=True
		for row in db.query("Select * from IndexTable Where Type=\""+type1+"\" and App_Id=\""+app_id+"\""):
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
		app_id=self.get_argument('app_id')
		# logging.info("herere");
		# logging.info(limit1);
		if limit1=='*':
			limit1='30'
		a=list()
		logging.info(limit1)
		# logging.info("Select * from KeyValueTable where `Key` ='" +str(key1)+"' and `Value` "+gle2+" '"+str(value1)+"' Limit "+limit1)
		#limit should be in next query
		for row in db.query("Select * from KeyValueTable where `Key` ='" +str(key1)+"' and `Value` "+gle2+" '"+str(value1)+"'"):
			a.append(str(row.Id))
		a=tuple(a)
		a=str(a)
		
		if(a=='()'):
			str1="[{\"Id\":null,\"Obj\":null,\"Type\":null,\"Timestamp\":null}]"
			self.write(str1)
		else:
			if bool(a.strip(',)')):
				a=a.strip(',)')
				a=a+')'
			str1=''
			for row in db.query("Select * from Obj_Table where Id IN "+str(a)+" and `App_Id` = \""+str(app_id)+"\" and `"+str(parameter1)+"`" +gle1+ "\""+str(pValue1)+"\"" +" Limit "+limit1):
					str1=str1+ ("{\"Id\":"+str(row.Id) +",\"Obj\":"+ str(row.J_Obj)+",\"Type\":\""+str(row.Type)+"\",\"Timestamp\":\""+str(row.Timestamp)+"\"},")
			logging.info("Select * from Obj_Table where Id IN "+str(a)+" and `App_Id` = \""+str(app_id)+"\" and `"+str(parameter1)+"`" +gle1+ "\""+str(pValue1)+"\"" +" Limit "+limit1)
			if(str1!=''):
				str1=str1.strip(',')
				str1='['+str1+']'
				self.write(str1)
				# logging.info(time.clock())
				logging.info(str1)
			else:
				str1=str1+ ("{\"Id\":null,\"Obj\":null,\"Type\":null,\"Timestamp\":null}")
				self.write(str1)
class DbRemove (tornado.web.RequestHandler):
	def post(self):
		removeId1=self.get_argument('removeId1')
		removeId1='('+removeId1+')'
		db.execute("DELETE FROM Obj_Table WHERE Id IN "+removeId1)
		db.execute("DELETE FROM KeyValueTable WHERE Id IN "+removeId1)
		self.write(removeId1)
class DbIndex (tornado.web.RequestHandler):
	def post(self):
		type1=self.get_argument('type1')
		index1=self.get_argument('index1')
		app_id=self.get_argument('app_id')
		db.execute("Insert into IndexTable Values (\""+type1+"\",\""+index1+"\",\""+app_id+"\")")
		self.write(index1+" indexed for "+type1 + " of application "+app_id)

class RenderInitFunc (tornado.web.RequestHandler):
	def post(self):
		session = uuid4()
		self.write(session)
