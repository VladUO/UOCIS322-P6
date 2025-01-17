from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/listAll',  methods = ["POST"])
def listAll():
    # getting format and k values out
    format = request.form.get("format")
    k = request.form.get("k")
    
    # app.logger.debug(format); 
    # app.logger.debug(k); 

    # formatting and sending a request to the api.py using requests
    r = requests.get('http://restapi:5000/listAll' + "/" + format + "?top=" + k)
    return r.text

@app.route("/listOpenOnly",  methods = ["POST"])
def listOpenOnly():
    # getting format and k values out
    format = request.form.get("format")
    k = request.form.get("k")

    # app.logger.debug(format); 
    # app.logger.debug(k);

    # formatting and sending a request to the api.py using requests
    r = requests.get('http://restapi:5000/listOpenOnly' + "/" + format + "?top=" + k)
    return r.text

@app.route("/listCloseOnly",  methods = ["POST"])
def listCloseOnly():
    # getting format and k values out
    format = request.form.get("format")
    k = request.form.get("k")

    # app.logger.debug(format); 
    # app.logger.debug(k);

    # formatting and sending a request to the api.py using requests
    r = requests.get('http://restapi:5000/listCloseOnly' + "/" + format + "?top=" + k)    
    return r.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
