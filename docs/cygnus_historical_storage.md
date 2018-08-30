## FIWARE Cygnus - Example of historical storage using MongoDB.

#### Creating a pressure sensor in the Orion Context Broker

```
curl -X POST \
-H "fiware-service:pressure_control" \
-H "fiware-servicepath:/pressure_control" \
-H "Content-Type:application/json" \
http://<HELIX_IP>:1026/v1/updateContext \
-d '{
"contextElements": [
            {
                "type": "iotdevice",
                "isPattern": "false",
                "id": "nodemcu",
                "attributes": [
                    {
                        "name": "pressure",
                        "type": "integer",
                        "value": "0"
                    }
                ]
            }
        ],
        "updateAction": "APPEND"
}
'
```
#### Creating a subscription in Orion Contex Broker

```
curl -iX POST \
  'http://<HELIX_IP>:1026/v2/subscriptions' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: pressure_control' \
  -H 'fiware-servicepath: /pressure_control' \
  -d '{
  "description": "Notify Cygnus of all context changes",
  "subject": {
    "entities": [
      {
        "idPattern": ".*"
      }
    ]
  },
  "notification": {
    "http": {
      "url": "http://172.17.0.1:5050/notify"
    },
    "attrsFormat": "legacy"
  },
  "throttling": 5
}'
```

#### Updating pressure sensor data

```
curl -iX POST \
  'http://<HELIX_IP>:1026/v1/updateContext' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: pressure_control' \
  -H 'fiware-servicepath: /pressure_control' \
  -d '{
"contextElements": [
  {
    "type": "iotdevice",
    "isPattern": "false",
    "id": "nodemcu",
    "attributes": [
       {
         "name": "pressure",
         "type": "integer",
         "value": "100"
       }
     ]
   }
 ],
"updateAction": "UPDATE"
}'
```

#### Viewing historical data in MongoDB.

```
docker exec -it <your_broker>_mongodb mongo
> show dbs
admin                0.000GB
local                0.000GB
orion                0.000GB
orion-pressure_control  0.000GB
sth_pressure_control    0.000GB
```
The `sth_pressure_control` will hold collections with the historical data record got from the device.

You can use MongoDB Compass to view historical data https://www.mongodb.com/products/compass

