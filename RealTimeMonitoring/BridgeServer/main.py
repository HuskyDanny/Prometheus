from flask import Flask, jsonify, render_template, request
from prometheus_client import Gauge, start_http_server, make_wsgi_app
from werkzeug.wsgi import DispatcherMiddleware
from adapter import adapter
from output import output
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

@app.route('/write', methods=['POST', 'GET'])
def addMetrics():
    if request.method == 'POST':
        data = request.get_json()
        adapter.write(data)
        return 'Finished addMetrics'
    else:
        return "Accessing metrics..." + adapter.showMetrics().decode("utf-8")

@app.route('/todb', methods=['POST'])
def todb():
    if request.method == 'POST':
        data = request.form.to_dict()
        
        metricname = request.form['metricname']
        filename = request.form['filename']
        period = request.form['period']
        # #data = request.get_json()
        output.outToCsv(filename, metricname, prometheus_host, period)
        return "Finished todb"

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80)
    
