from __future__ import print_function, absolute_import, division
from flask import Flask
from flask import request
import json
from FunctionModule import Reply
import aiml
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app, supports_credentials = True)
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

@app.route('/chat/', methods = ['GET'])
def chat():
    #jsondata = request.get_json()
    #data = json.loads(jsondata)
    query=request.args.get('query')
    #stuff happens here that involves data to obtain a result
    response = Reply(kernel.respond(query))
    #result = [CBReply(data[0]['query'])] 
    return json.dumps(response)

''''@app.after_request
def apply_caching(response):
	response.headers["access-control-allow-origin"] = "*"
	response.headers["access-control-allow-credentials"] = "true"
	return response'''

if __name__ == '__main__':
    app.run(debug=True)