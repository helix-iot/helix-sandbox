# Helix sandbox

## About

Helix Sandbox is an open platform that is fully compatible with FIWARE's Generic Enablers (GE). Its purpose is to simplify the process of installation, configuration and use of the GEs through an easy-to-use graphical interface that enables orchestration of the elements that constitute it. The platform is built on a microservice basis and uses Docker to perform the GE instantiation. Helix Sandbox can be installed on any Cloud platform or virtualization that enables the use of Linux virtual machines. In its internal architecture are present the Orion Context Broker, IoT Agent LWM2M Coap, Cygnus, Helix dashboard and a MongoDB database to provide the temporal storage of the data. It can be used to aid and accelerate the process of constructing PoCs (Proof of Concept) and experimental applications based on FIWARE with the use of few computional resources.

<img align="right" src="docs/img/powered_by_fiware.png">

<br>
<br>

## Helix Sandbox Architecture

<img src="docs/img/helixsandbox.jpg">

<br>

## Documentation

  - Requirements, Installation and Maintenance
    - [Requirements before Helix sandbox installation](docs/requirements.md)
    - [Installation](docs/installation.md)
    - [Updating/Reseting](docs/update_reset.md)

  - Tutorials and How-to's
    - [Accessing Helix Sandbox Web Interface](docs/accessing.md)
    - [Creating an Attribute](docs/create_attribute.md)
    - [Creating a Service](docs/create_service.md)
    - [Creating a Device](docs/create_device.md)
    - [Creating an Agent](docs/create_agent.md)
    - [Creating a Broker](docs/create_broker.md)
    - [Assigning an Attribute to a Service](docs/assign_attribute.md)
    - [Assigning a Service to a Device](docs/assign_service.md)
    - [Assigning an Agent to a Broker](docs/assig_agent.md)
    - [Assigning a Device to an Agent](docs/assign_device.md)
    - [Connecting to the Agent using the device](docs/connecting_device.md)
    - [FIWARE Cygnus - Example of historical storage using MongoDB.](docs/cygnus_historical_storage.md)
    - [Creating a third-party dashboard](docs/creating_dashboard.md)


  > If this is the first time you use Helix Sandbox, we recommend that you proceed in the order above.

<br>

## Documentation and additional resources

#### FIWARE Orion Context Broker
https://fiware-orion.readthedocs.io/en/master/index.html

#### FIWARE Cygnus
https://fiware-cygnus.readthedocs.io/en/latest/

#### IoT Agent CoAP with DTLS - Secure FIWARE
https://github.com/m4n3dw0lf/SecureFiware

#### Postman Collection - Orion Context Broker
https://goo.gl/dPPHQv

#### Sketch Arduino Uno R3 + ESP8266 + LM35 Send data to Orion Context Broker
https://goo.gl/nX8iMG

#### © Helix 2018, All rights reserved.
