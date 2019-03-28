from flask import Flask, jsonify, render_template, request, reqparse
from prometheus_client import Gauge, start_http_server, make_wsgi_app
from werkzeug.wsgi import DispatcherMiddleware
import adapter
from wtforms import Form, TextAreaField, validators

app = Flask(__name__)

''' 
Opening 3 endpoints --> / , /write, /metrics
/ checks for up
/write receives post requests
/metrics get scraped by Prometheus
'''
@app.route('/')
def index():
    return 'Running...'

@app.route('/write', methods=['POST'])
def addMetrics():
    if request.method == 'POST':
        data = request.get_json()
        adapter.write(data)
        return 'Finished addMetrics'

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80)



# class ReviewForm(Form):
#     filename = TextAreaField('',[validators.DataRequired(), validators.length(min = 5)])
#     metricname = TextAreaField('',[validators.DataRequired(), validators.length(min = 5)])
#     period = TextAreaField('')

# @app.route('/toCSV')
# def toCSV():
#     form = ReviewForm(request.form)
#     return render_template('index.html', form = form)



# @app.route('/todb', methods=['POST'])
# def todb():
#     if request.method == 'POST':
#         data = request.form.to_dict()
        
#         metricname = request.form['metricname']
#         filename = request.form['filename']
#         period = request.form['period']
#         # #data = request.get_json()
#         output.outToCsv(filename, metricname, prometheus_host, period)
#         return "Finished todb"
    
