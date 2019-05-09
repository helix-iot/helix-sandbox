## Creating, Sending and Receiving data context from Orion Context Broker
### Requirements

Create and start a Orion Context Broker through the Helix Sandbox Dashboard

### NGSI-LD Standard

Fiware data model recommend that use the ngsi-ld standards to create a entity, for example:

If you have two iot_devices, you can discribe them as follows:

- Arduino 1

    type: "iot_device"

    id: "urn:ngsi-ld:iot:001"

- Arduino 2

    type: "iot_device"

    id: "urn:ngsi-ld:iot:002"

### Creating a context entity
```
import json
import requests
url = 'http://<helix_ip>:1026/v2/entities'
head = {"Content-Type": "application/json"}
d= '{ "id": "urn:ngsi-ld:iot:001", "type" : "iot_device", "level" : { "value" : "0", "type" : "integer" }}'
response = requests.post(url, data = d, headers = head)
print (response)
```
### Sending data to a context entity
```
import json
import requests
head = {"Content-Type": "application/json"}   
d = '{ "level" : { "value" : "0", "type" : "integer" } }'
url = 'http://<helix_ip>:1026/v2/entities/urn:ngsi-ld:iot:001/attrs'
response = requests.post(url, data=d, headers=head)
print (response)
```
### Receiving data from a context entity
```
import json
import requests
url = 'http://<helix_ip>:1026/v2/entities/urn:ngsi-ld:iot:001/attrs/level'
response = requests.get(url)
data = response.json()
value = str(data['value'])
valued = int(value)
print (valued)
