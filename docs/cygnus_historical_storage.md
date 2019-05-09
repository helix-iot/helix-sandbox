## FIWARE Cygnus - Start historical storage using MongoDB

#### Send a subscription to Orion Context Broker 

```
curl -X POST \
-H "Content-Type:application/json" \
-H "Accept:application/json" \
http://<helix_ip>:1026/v2/subscriptions \
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
}
'
```
#### Viewing historical data from MongoDB

> You can use MongoDB Compass to view historical data. Try https://www.mongodb.com/products/compass

