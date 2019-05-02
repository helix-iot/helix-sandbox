## Receiving data from helix by GET method
```
import json
import requests
url = 'http://<ip_helix>:1026/v2/entities/urn:ngsi-ld:iot:001/attrs/level'
response = requests.get(url)
data = response.json()
value = str(data['value'])
valued = int(value)
response = requests.get(url)
print (valued)
