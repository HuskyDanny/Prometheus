
from prometheus_client import Gauge, Counter, Histogram, start_http_server, REGISTRY
from datetime import datetime
import json
import time
from flask import request

DATE_FMT = "%Y-%m-%d %H:%M:%S"
labels = ['A_Stage','B_JobID','C_RequestID']

QA_Request_Counts = Counter('QA_Request', 'Requests#')
Bizman_Request_Counts = Counter('Bizman_Request','Requests#')

QA_Request_Latency = Histogram('QA_Request_Latency', 'Latency')
Bizman_Request_Latency = Histogram('Bizman_Request_Latency', 'Latency')

reference = {'QA':[QA_Request_Counts,QA_Request_Latency], 
            'Bizman':[Bizman_Request_Counts, Bizman_Request_Latency]}
#Converting data to prometheus format
def write(data):
    
    if not data:
        print("Data passed in is null")
    else:
        for envelope in data:

            data = envelope['data']

            #Get stage and timebefore
            stage = data['stage']
            latency = data['latency']
            
            reference[stage][0].inc()
            reference[stage][1].observe(latency)
                
def clearAll():
    for name in list(REGISTRY._names_to_collectors.keys()):
        try:
            REGISTRY.unregister(REGISTRY._names_to_collectors[name])
        except:
            print("{0} has already been deleted".format(name))
            pass
