## Connecting to the Agent using the device

Walkthrough client found here: https://github.com/telefonicaid/lwm2m-node-lib

Run the following commands in the client:

```
create /3311/0                                  # Notice: Object ID
connect <HELIX_IP> 5683 rasp1 /light_control    # Notice: Device and Service names
set /3311/0 5850 On                             # Notice: Resource ID
```

### Query the device status on the FIWARE Orion Context Broker

Run the following curl:

```
curl -X POST -k https://<HELIX_IP>:1026/v1/queryContext \
--header "fiware-service:light_control" \
--header "fiware-servicepath:/light_control" \
--header "Content-Type:application/json" \
--header "Accept:application/json" \
-d '{
      "entities": [{
        "id" : "Device:rasp1"
      }]
    }'
```

```
{
 "contextResponse": [
 {
>..."contextElement": {
>..."type": "Device",
>..."isPattern": "false",
>..."id": "Device:rasp1",
>..."attributes": [
>...{
>...>..."name": "On/Off",
>...>..."type": "Boolean",
>...>..."value": "On"
>...}
>...]
>...},
>..."statusCode": {
>... "code": "200",
>... "reasonPhrase": "OK"
   }
  }
 ]
}
```

