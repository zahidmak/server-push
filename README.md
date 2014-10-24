server-push
===========
There has always been problem for pushing data from server side to client side. Here is the solution using HTML 5 web sockets and python.
This is plug and play kind of websocket server which can push data to the client side(vice-versa).
Prerequisite: python tornado webserver. Install using following command in the cmd prompt
pip install tornado OR easy_install tornado

For detail see server-push.pdf

Uses
1. Pushing data from server side
2. Getting data from client side
3. Making chat application

<p>
    <strong>server-push</strong>
</p>
<p>
    There has always been problem for pushing data from server side to client side. Here is the solution using web sockets and tornado webserver(python).
</p>
<p>
    This is plug and play kind of websocket server which can push data to the client side and vice-versa.
</p>
<p>
    <strong>Prerequisite</strong>
    : tornado webserver. Install using following command in the cmd line
</p>
<div>
    <p>
        <code>pip install tornado</code>
        OR <code>easy_install tornado</code>
    </p>
</div>
<p>
    <strong><u>Step 1</u></strong>
    <u>: Run server.py on server(Now server is ready for conversation using websockets) using following cmd</u>
</p>
<div>
    <p>
        <em>python server.py</em>
    </p>
</div>
<p>
    <strong><u>Step 2</u></strong>
    <u>: Copy and paste the below code on client’s HTML page</u>
</p>
<div>
    <p>
        &lt;script&gt;
    </p>
    <p>
        $(document).ready(function () {
    </p>
    <p>
        var ws;
    </p>
    <p>
        var host = '192.168.1.1'; //server IP
    </p>
    <p>
        var port = '8888'; //server port
    </p>
    <p>
        var uri = 'ws'; //websocket uri
    </p>
    <p>
        ws = new WebSocket("ws://" + host + ":" + port + uri); //create web socket object
    </p>
    <p>
        //Called when connection is established with server
    </p>
    <p>
        ws.onopen = function (evt) {
    </p>
    <p>
        alert("Connection open");
    </p>
    <p>
        };
    </p>
    <p>
        //Called when message is sent from server
    </p>
    <p>
        ws.onmessage = function (evt) {
    </p>
    <p>
        alert("message received: " + evt.data)
    </p>
    <p>
        };
    </p>
    <p>
        //Called when connection is closed from server
    </p>
    <p>
        ws.onclose = function (evt) {
    </p>
    <p>
        alert("Connection close");
    </p>
    <p>
        };
    </p>
    <p>
        });
    </p>
    <p>
        &lt;/script&gt;
    </p>
</div>
<p>
    <strong><u>Step 3</u></strong>
    <u>: Understanding server side code(server.py)</u>
</p>
<div>
    <p>
        from tornado import httpserver
    </p>
    <p>
        import tornado.websocket
    </p>
    <p>
        import tornado.ioloop
    </p>
    <p>
        import tornado.web
    </p>
    <p>
        clients = []
    </p>
    <p>
        userid = 0
    </p>
    <p>
        class WSHandler(tornado.websocket.WebSocketHandler):
    </p>
    <p>
        #Called when attempt is made for connection from client
    </p>
    <p>
        def open(self):
    </p>
    <p>
        obj = SessionManagement()
    </p>
    <p>
        obj.createsession(self)#storing web socket object for further communication with client
    </p>
    <p>
        #Called when client sends message
    </p>
    <p>
        def on_message(self, message):
    </p>
    <p>
        print 'message received %s' % userid
    </p>
    <p>
        #Called when user refreshes or closes the page
    </p>
    <p>
        def on_close(self):
    </p>
    <p>
        obj = SessionManagement()
    </p>
    <p>
        obj.deletesession(self)#deleting web socket object
    </p>
    <p>
        print 'connection closed'
    </p>
    <p>
        class SessionManagement():
    </p>
    <p>
        #Create session and stores into array
    </p>
    <p>
        def createsession(self, obj):
    </p>
    <p>
        userid = obj.get_argument("userid")
    </p>
    <p>
        componentid = obj.get_argument("compid")
    </p>
    <p>
        clients.append({"wsobj":obj, "userid":userid, "compid":componentid})
    </p>
    <p>
        for w in clients:
    </p>
    <p>
        print w
    </p>
    <p>
        #Delete session from array when client refreshes the page or closes the page
    </p>
    <p>
        def deletesession(self, obj):
    </p>
    <p>
        for temp in clients:
    </p>
    <p>
        if cmp(obj, temp['wsobj']):
    </p>
    <p>
        clients.remove(temp)
    </p>
    <p>
        for w in clients:
    </p>
    <p>
        print w
    </p>
    <p>
        class PushToUser(tornado.web.RequestHandler):
    </p>
    <p>
        def get(self):
    </p>
    <p>
        userid = self.get_argument('userid')
    </p>
    <p>
        compid = self.get_argument('compid')
    </p>
    <p>
        message = self.get_argument('message')
    </p>
    <p>
        for temp in clients:
    </p>
    <p>
        if (temp['userid'] == userid and temp['compid'] == compid):
    </p>
    <p>
        temp['wsobj'].write_message(message)
    </p>
    <p>
        class PushToAll(tornado.web.RequestHandler):
    </p>
    <p>
        def get(self):
    </p>
    <p>
        message=self.get_argument('message')
    </p>
    <p>
        for temp in clients:
    </p>
    <p>
        temp['wsobj'].write_message(message)
    </p>
    <p>
        application = tornado.web.Application([
    </p>
    <p>
        (r'/ws', WSHandler),
    </p>
    <p>
        (r'/push', PushToUser), #Ex. /push?userid=123&amp;compid=123&amp;message=hello
    </p>
    <p>
        (r'/pushtoall', PushToAll), #Ex. /pushtoall?message="hello"
    </p>
    <p>
        ])
    </p>
    <p>
        if __name__ == "__main__":
    </p>
    <p>
        http_server = tornado.httpserver.HTTPServer(application)
    </p>
    <p>
        http_server.listen(8888)
    </p>
    <p>
        tornado.ioloop.IOLoop.instance().start()
    </p>
</div>
<p>
    <u>Step 4: Sending message to client using REST</u>
</p>
<p>
    - Push message to specific user
</p>
<p>
    <img src="file:///C:\Users\Zahid\AppData\Local\Temp\msohtmlclip1\01\clip_image002.jpg" height="397" width="813"/>
</p>
<p>
    - Push message to all users
</p>
<p>
    <img src="file:///C:\Users\Zahid\AppData\Local\Temp\msohtmlclip1\01\clip_image004.jpg" height="434" width="841"/>
</p>
<p>
    Done!!!!!
</p>
