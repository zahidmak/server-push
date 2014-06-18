from tornado import httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

clients = []
userid = 0
class WSHandler(tornado.websocket.WebSocketHandler):
    
    #Called when attempt is made for connection from client
    def open(self):
        obj = SessionManagement()
        obj.createsession(self)#storing web socket object for further communication with client
     
    #Called when client sends message  
    def on_message(self, message):
        print 'message received %s' % userid
 
    #Called when user refreshes or closes the page
    def on_close(self):
        obj = SessionManagement()
        obj.deletesession(self)#deleting web socket object
        print clients


class SessionManagement():
    #Create session and stores into array
    def createsession(self, obj):
        userid = obj.get_argument("userid")
        componentid = obj.get_argument("compid")
        clients.append({"wsobj":obj, "userid":userid, "compid":componentid})
        
    #Delete session from array when client refreshes the page or closes the page    
    def deletesession(self, obj):
        for temp in clients:
            if (obj==temp['wsobj']):
                clients.remove(temp)
        
            
class PushToUser(tornado.web.RequestHandler):
    def get(self):
        userid = self.get_argument('userid')
        compid = self.get_argument('compid')
        message = self.get_argument('message')
        for temp in clients:
            if (temp['userid'] == userid and temp['compid'] == compid):
                temp['wsobj'].write_message(message) 
                
class PushToAll(tornado.web.RequestHandler):
    def get(self):
        message=self.get_argument('message')
        for temp in clients:
            temp['wsobj'].write_message(message)
                 
application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/push', PushToUser), #Ex. /push?userid=123&compid=123&message=hello
    (r'/pushtoall', PushToAll), #Ex. /pushtoall?message="hello"
])
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
