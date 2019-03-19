#Dummy references
stage = ['ImageQuality','ToBizman','QA']
requestID = ['kii983','dd911','lk978']

#Using client adapter
#Appname and client host
client_adapter = AppLog('test',"http://localhost:8000")

#Constructing single data case
t = time.time()
data = {'stage':'ImageQuality', 'jobID':'abcde','requestID':'12345','timeBefore': t}
client_adapter.Write("Junchen's",data)

#Constructing continuous data cases
while True:
    #Notes the time right before server
    t = time.time()
    time.sleep(random.randint(0,5))
    #Simulate server processing time
    time.sleep(random.randint(0,5))
    #Constructing data
    data = {'stage':stage[random.randint(0,2)], 'jobID': 'bba9498', 'requestID':requestID[random.randint(0,2)], 'timeBefore':t}
    #Send to server
    client_adapter.Write("Junchen's",data)