
## Requirements before Helix Sandbox installation

- You can use any local hypervisor like Virtual Box, VMware and KVM or if you need a global internet access we suggest any Cloud Service Provicer (CSP) like AWS, Azure or Google. 
- Minimum server configuration: 1 vCPU, 1GB RAM and 16GB HDD or SSD.
- You can install any Linux distribution, but Ubuntu Server 18.04 LTS has been validated exhaustively for us. 
- You will need to open the ports in the Firewall if you decide to use CSP:
```
22/TCP - SSH 
5000/TCP - Web Interface
1026/TCP - Orion Contex Broker (HTTP or HTTPs)
27017/TCP - MongoDB "Historical Data Access"
5683/UDP - CoAP
5684/UDP - CoAP with DTLS
```
- You must update and upgrade the server using sudo apt command:

```
sudo apt update
sudo apt upgrade
```
- Install <b>Docker</b>: https://docs.docker.com/install/linux/docker-ce/ubuntu/
- Install <b>docker-compose</b>: https://docs.docker.com/compose/install/#install-compose
- Download the template images to prevent first-time delays deploying containers.

```
sudo docker pull mongo:3.4
sudo docker pull fiware/orion:1.10.0
sudo docker pull fiware/cygnus-ngsi:1.9.0
sudo docker pull m4n3dw0lf/dtls-lightweightm2m-iotagent
```
- If you want to use TLS/DTLS in the Orion and IoT Agents, you need to create a `/run/secrets` directory inside your host and populate with the certificate and key, you can generate a self-signed key-pair using the following command:
```
sudo mkdir -p /opt/secrets
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /opt/secrets/ssl_key -out /opt/secrets/ssl_crt
```

