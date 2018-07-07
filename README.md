# Helix
![](img/helix_banner.png)

## About

Middleware for secure IoT provisioning, access and control.

powered by: [Fiware](https://www.fiware.org/)

## Installing

```
git clone https://github.com/m4n3dw0lf/helix-sandbox
cd compose
echo "change_to_your_encryption_key" > secrets/aes_key.txt
sudo docker-compose up -d
```

- Access: http://localhost:5000

- Setup the **admin** account


## TO-DO

- On Setup, fetch the LWM2M IPSO Registry https://github.com/IPSO-Alliance/pub/blob/master/reg/README.md then populate the Attribute model with all the registries in the database, also remember to remove the attribute template/view, leave only the assign form and models.
