import json
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import torndb
import time
from tornado.options import define,options
define("port",default=8000,help="tornado will run on the given port",type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')
	
class DbInsert(tornado.web.RequestHandler):
	def post(self):
		object1=self.get_argument('object')
		type1=self.get_argument('type')
		db.execute("Insert into Obj_Table (`J_Obj`,`Type`,`Timestamp`) Values (%s,%s,%s)",object1,type1,time.time() )
		json_data=json.loads(object1)
		row=db.query("select * from Obj_Table Order by id desc")
		new_id=row[0].Id
		self.write(str(row[0].Id)+"<br>")
		#self.write(json_data['name'])
		for k,v in json_data.items():
			db.execute("Insert into KeyValueTable Values(%s,%s,%s)",new_id,k,v )
		
class DbQuery(tornado.web.RequestHandler):
	def post(self):
		id1=self.get_argument('Id1')
		id1='('+id1+')'
		for row in db.query("Select * from Obj_Table where Id In "+id1):
			self.write ("{\"Id\":"+str(row.Id) +",\"Obj\":"+ str(row.J_Obj)+",\"Type\":\""+str(row.Type)+"\",\"Timestamp\":\""+str(row.Timestamp)+"\"}<br>")
class DbSearch(tornado.web.RequestHandler):
	def post(self):
		key1=self.get_argument('key1')
		value1=self.get_argument('value1')
		parameter1=self.get_argument('parameter1')
		gle1=self.get_argument('gle1')
		pValue1=self.get_argument('parameterValue1')
		limit1=self.get_argument('limit1','1000')
		a=list()
		for row in db.query("Select * from KeyValueTable where `Key` ='" +str(key1)+"' and `Value`='"+str(value1)+"' Limit "+limit1):
			self.write (str(row.Id)+"<br>")
			a.append(str(row.Id))
		a=tuple(a)
		#self.write(str(a))
		#self.write(parameter1)
		#self.write(pValue1)
		#self.write(gle1)
		self.write("<br> Select * from Obj_Table where Id IN "+str(a)+" and `"+str(parameter1)+"`" +gle1+" \""+str(pValue1)+"\"<br>")
		for row in db.query("Select * from Obj_Table where Id IN "+str(a)+" and `"+str(parameter1)+"`" +gle1+ "\""+str(pValue1)+"\"" ):
			self.write ("{\"Id\":"+str(row.Id) +",\"Obj\":"+ str(row.J_Obj)+",\"Type\":\""+str(row.Type)+"\",\"Timestamp\":\""+str(row.Timestamp)+"\"}"+"<br>")
class DbRemove (tornado.web.RequestHandler):
	def post(self):
		removeId1=self.get_argument('removeId1')
		self.write(removeId1)
		removeId1='('+removeId1+')'
		db.execute("DELETE FROM Obj_Table WHERE Id IN "+removeId1)
		db.execute("DELETE FROM KeyValueTable WHERE Id IN "+removeId1)
if __name__ == "__main__":
	tornado.options.parse_command_line()
	db = torndb.Connection("localhost", "tordata",user="root",password="ksh")
	app=tornado.web.Application(
		handlers=[(r"/",IndexHandler),(r"/insert",DbInsert),(r"/query",DbQuery),(r"/search",DbSearch),(r"/remove",DbRemove)],
		template_path=os.path.join(os.path.dirname(__file__),"templates"),
		debug=True
		)
	http_server=tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
	