import csv
import requests
import sys
import json


def loadingLabel(response):
    labelnames = []
    if not response:
        print("No response available")
    else:
        labelnames.append(list(response[0]['metric'].keys()))
        if '__name__' in labelnames:
            labelnames.remove('__name__') 
        print(labelnames) 
        labelnames = sorted(labelnames[0])
    return labelnames
    

def getResponse(metricName, host, period=''):
    metricName += '{0}'
    query_Type = metricName.format(period)
    print(metricName)
    try:
        response = requests.get('{0}/api/v1/query'.format(host),params={'query': query_Type})
        response = response.json()['data']['result']
        return response
    except:
        print("request not successful, either host or metricName is wrong")
    

def outToCsv(filename, metricName, host, period=''):
    # data = json.loads(data)
    # filename = data['filename']
    # metricName = data['metricName']

    if period:
        response = getResponse(metricName, host)
    else:
        response = getResponse(metricName, host, period)
    labelnames = loadingLabel(response)

    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'value'] + labelnames)
        for result in response:
            l = [result['metric'].get('__name__', '')] + [result['value'][1]]
            for label in labelnames:
                l.append(result['metric'].get(label, ''))
            writer.writerow(l)



