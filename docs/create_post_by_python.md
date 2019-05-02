## sending light data through the POST method done in Python on Adroind

````
import json
import requests
import androidhelper
head = {"Content-Type": "application/json"}   
droid = androidhelper.Android()
droid.startSensingTimed(1, 250)
sensor2 = droid.sensorsGetLight().result
d1 = '{ "level" : { "value" : "'
d2 = str(sensor2)
d3 = '" , "type" : "integer" } }'
dt = d1 + d2 + d3
print (dt)
url = 'http://<ip_helix:1026/v2/entities/urn:ngsi-ld:iot:001/attrs'
response = requests.post(url, data=dadost, headers=head)
print (response)
droid.stopSensing()
