import json
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import torndb
from tornado.options import define,options
define("port",default=8000,help="tornado will run on the given port",type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')
	
class DbInsert(tornado.web.RequestHandler):
	def post(self):
		object1=self.get_argument('object')
		type1=self.get_argument('type')
		db.execute("Insert into Obj_Table (`J_Obj`,`Type`) Values (%s,%s)",object1,type1 )
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
		for row in db.query("Select * from Obj_Table where Id = "+id1):
			self.write ("{\"Id\":"+str(row.Id) +",\"Obj\":"+ str(row.J_Obj)+",\"Type\":\""+str(row.Type)+"\",\"Timestamp\":\""+str(row.Timestamp)+"\"}")
class DbSearch(tornado.web.RequestHandler):
	def post(self):
		key1=self.get_argument('key1')
		value1=self.get_argument('value1')
		for row in db.query("Select * from KeyValueTable where `Key` ='" +str(key1)+"' and `Value`='"+str(value1)+"'"):
			self.write (str(row.Id)+"<br>")
if __name__ == "__main__":
	tornado.options.parse_command_line()
	db = torndb.Connection("localhost", "tordata",user="root",password="ksh")
	app=tornado.web.Application(
		handlers=[(r"/",IndexHandler),(r"/insert",DbInsert),(r"/query",DbQuery),(r"/search",DbSearch)],
		template_path=os.path.join(os.path.dirname(__file__),"templates"),
		debug=True
		)
	http_server=tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
	