
from prometheus_client import Gauge, start_http_server, REGISTRY
from datetime import datetime
import json
import time
from flask import request

DATE_FMT = "%Y-%m-%d %H:%M:%S"
labels = ['A_Stage','B_JobID','C_RequestID','D_StartTime','E_EndTime']

All_timestamps = Gauge('All_timestamps', 'timestamps',labels)

def checkData(dimensions, data):
    for dimension in dimensions:
        try:
            dummy = data[dimension]
            if not dummy:
                print("{0} missing data".format(dimension))
        except:
            print("Should write as {0}".format(dimension))

#Converting data to prometheus format
def write(data):
    
    if not data:
        print("Data passed in is null")
    else:
        #dimensions = ['stage','jobID','requestID','timeBefore']
        #self.checkData(dimensions, data)
        # data = json.loads(data)

        #extract the metrics that stores useful infos
        for envelope in data:

            data = envelope['data']

            #Get each column of data 
            stage = data['stage']
            jobID = data['jobID']
            requestID = data['requestID']
            dateBefore_timeStamp = data['timeBefore']

            dateBefore_str = str(datetime.utcfromtimestamp(int(dateBefore_timeStamp)).strftime(DATE_FMT))
            datetimeAfter_str = str(datetime.now().strftime(DATE_FMT))
            datetimeAfter_timeStamp = time.time()
            timeStamp = datetimeAfter_timeStamp - dateBefore_timeStamp
            All_timestamps.labels(stage, jobID, requestID, dateBefore_str, datetimeAfter_str).set(timeStamp)
            # All_timestamps.labels(stage, jobID, requestID).set(timeStamp)
            print(All_timestamps)


def clearAll():
    for name in list(REGISTRY._names_to_collectors.keys()):
        try:
            REGISTRY.unregister(REGISTRY._names_to_collectors[name])
        except:
            print("{0} has already been deleted".format(name))
            pass
            
def existing():
    return REGISTRY._names_to_collectors

def monitor(port = 8000, address=''):
    start_http_server(port, address)