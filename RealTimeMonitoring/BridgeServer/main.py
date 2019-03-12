from flask import Flask, jsonify, render_template, request
from prometheus_client import Gauge, start_http_server
from adapter import write, monitor
from output import outToCsv
from wtforms import Form, TextAreaField, validators


class ReviewForm(Form):
    filename = TextAreaField('',[validators.DataRequired(), validators.length(min = 5)])
    metricname = TextAreaField('',[validators.DataRequired(), validators.length(min = 5)])
    period = TextAreaField('')

prometheus_host = 'http://prometheus:9090'
http_port = 8000

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello'

@app.route('/toCSV')
def toCSV():
    form = ReviewForm(request.form)
    return render_template('index.html', form = form)



#start http server for data scraping
monitor(8000)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
