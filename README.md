# Helix

Middleware for secure IoT provisioning, access and control.

powered by: [Fiware](https://www.fiware.org/)

## Installing

#### Pre-requisites: 

  System with **python**, **lxc**, **pip**, **python-setuptools** and **python-lxc** installed

  - In debian-based linux distros:

  `sudo apt-get install -y python lxc python-pip python-setuptools python-lxc`

#### Install python requirements

  `pip install -r requirements.txt`

<br>

## Running on Development or Testing environments

  - Start the WebServer

    - syntax:
      ```
      python run.py
      ```
<br>

## Running on Production environments

  - Set Environment variables:

    - syntax:
      ```
      export FLASK_CONFIG=production
      export FLASK_APP=run.py
      ```

  - Database Configuration

    - Set the MySQL environment variable

      - syntax:
        ```
        export MYSQL_HOST=<MySQL Host, default=localhost>
        export MYSQL_USER=<MySQL User, default=admin>
        ```

      - example:
        ```
        export MYSQL_HOST=not_localhost
        export MYSQL_USER=not_admin
        ```

    - Set the MySQL password inside the `helix/secrets/` directory in a `mysql_password.txt`, as specified below:

      |File | Data |
      |-|-|
      |**mysql_password.txt**| The password for the MySQL database |


    - Start the Database Migrations directory and populate the MySQL database

      ```
      flask db init
      flask db migrate
      flask db upgrade
      ```

  - Start the WebServer with

    - Inside the root directory `helix/` run:
    
      ```
      flask run
      ```

## TO-DO

- On Setup, fetch the LWM2M IPSO Registry https://github.com/IPSO-Alliance/pub/blob/master/reg/README.md then populate the Attribute model with all the registries in the database, also remember to remove the attribute template/view, leave only the assign form and models.
