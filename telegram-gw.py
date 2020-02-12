from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.httputil import HTTPHeaders
from tornado.escape import json_encode, json_decode
import tornado.web
from os import environ, getenv

template = "{} -> {}: {}"

bot_id  = environ["BOT_ID"]
url     = "https://api.telegram.org/bot{}/sendMessage".format(bot_id)

bind_addr = getenv("BIND_ADDR") or "127.0.0.1"
bind_port = getenv("BIND_PORT") or 8888

body = {
   "chat_id":    "", 
   "parse_mode": "markdown",
   "text":       ""
}

statusmap = { 
   "firing":   "PROBLEM", 
   "resolved": "OK"
} 

headers = HTTPHeaders(
   {"Content-Type": "application/json"})


client = AsyncHTTPClient()


class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("ok")

class MainHandler(tornado.web.RequestHandler):
    def get(self, matched_part=None):
        if matched_part is None:
            self.write("error")
        else:
            self.write(matched_part)

    def post(self, matched_part=None):
        if matched_part is None:
            self.write("no user id provided")
            return

        body["chat_id"] = matched_part

        data = json_decode(self.request.body)
        
        for alert in data["alerts"]:
           try:
               body["text"] = template.format(alert["labels"]["hostname"], statusmap[alert["status"]], alert["annotations"]["summary"])
               request = HTTPRequest(url, headers=headers, method="POST", body=json_encode(body))
               r = client.fetch(request)
           except Exception as e:
               print(e)
               self.write("error")
           else:
               self.write("sent")


def telegram():
    return tornado.web.Application([
        (r"/", DefaultHandler),
        ("^\/user\/(.+)/$", MainHandler),
    ])

if __name__ == "__main__":
    app = telegram()
    app.listen(bind_port, address=bind_addr)
    tornado.ioloop.IOLoop.current().start()
