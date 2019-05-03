## Creating an entity on Helix Sandbox by Android
```
import json
import requests
url = 'http://<ip_helix>:1026/v2/entities'
head = {"Content-Type": "application/json"}
d= '{ "id": "urn:ngsi-ld:iot:001", "type" : "iot_device", "level" : { "value" : "0", "type" : "integer" }}'
response = requests.post(url, data = d, headers = head)
print (response)
