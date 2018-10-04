from __future__ import print_function
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sys, uuid, base64
import docker,json,requests
from time import sleep
client = docker.from_env()
from app import db, login_manager
from simple_aes_cipher import AESCipher, generate_secret_key
from os import environ,urandom
from getpass import getpass
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

__author__ = "m4n3dw0lf"

try:
  AES_KEY = open(environ['AES_KEY']).readline().replace("\n","")
except:
  try:
    AES_KEY = getpass("AES Master Key:").rstrip("\n")
  except KeyboardInterrupt:
    sys.exit(0)

secret_key = generate_secret_key(AES_KEY)
cipher = AESCipher(secret_key)
AES_KEY = None
secret_key = None

device_association = db.Table('device_association',
  db.Column('service_id',db.Integer,
             db.ForeignKey('service.id')),
  db.Column('device_id',db.Integer,
            db.ForeignKey('device.id'))
)

service_association = db.Table('service_association',
  db.Column('attribute_id',db.Integer,
             db.ForeignKey('attribute.id')),
  db.Column('service_id',db.Integer,
             db.ForeignKey('service.id'))
)

agent_association = db.Table('agent_association',
  db.Column('device_id',db.Integer,
            db.ForeignKey('device.id')),
  db.Column('agent_id',db.Integer,
             db.ForeignKey('agent.id'))
)

broker_association = db.Table('broker_association',
  db.Column('agent_id',db.Integer,
            db.ForeignKey('agent.id')),
  db.Column('broker_id',db.Integer,
            db.ForeignKey('broker.id'))
)

user_device_association = db.Table('user_device_association',
  db.Column('device_id',db.Integer,
             db.ForeignKey('device.id')),
  db.Column('user_id',db.Integer,
             db.ForeignKey('users.id'))
)

class Attribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200))
    mapping = db.Column(db.String(20), unique=True)
    operation = db.Column(db.String(4))
    mandatory = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    services = db.relationship('Service', secondary="service_association",
      lazy='dynamic'
    )

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    ip = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    services = db.relationship('Service',secondary="device_association",
      lazy='dynamic'
    )
    agents = db.relationship('Agent',secondary="agent_association",
      lazy='dynamic'
    )
    def grant_service(self,endp):
        service = Service.query.filter_by(name=endp.name).first()
        if service and service in self.services:
          return
        if not service:
          return
        self.services.append(service)
    def revoke_service(self,endp):
        service = Service.query.filter_by(name=endp.name).first()
        if not service or not service in self.services:
	  return
        self.services.remove(service)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    mapping = db.Column(db.String(20), unique=True)
    type = db.Column(db.String(200))
    description = db.Column(db.String(200))
    attributes = db.relationship('Attribute', secondary="service_association",
      lazy='dynamic'
    )
    devices = db.relationship('Device', secondary="device_association",
      lazy='dynamic'
    )
    def has_attribute(self,name):
        attribute = Attribute.query.filter_by(name=name).first()
        if not attribute or not attribute in self.attributes:
          return False
        return True
    def grant_attribute(self,endp):                                          
        attribute = Attribute.query.filter_by(name=endp.name).first()
        if attribute and attribute in self.attributes:
          return
        if not attribute:
          return
        self.attributes.append(attribute)
    def revoke_attribute(self,endp):
        attribute = Attribute.query.filter_by(name=endp.name).first()
        if not attribute or not attribute in self.attributes:
          return
        self.attributes.remove(attribute)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))
    type = db.Column(db.String(50), default="lwm2m")
    port = db.Column(db.String(5), default="5684", unique=True)
    encryption = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=False)
    created = db.Column(db.Boolean, default=False)
    broker_ip = db.Column(db.String(50), default="localhost")
    broker_port = db.Column(db.String(8), default="1026")
    broker_name = db.Column(db.String(50))
    broker_context = db.Column(db.String(5), default="http")
    config = db.Column(db.Text)
    devices = db.relationship('Device', secondary="agent_association",
      lazy='dynamic'
    )

    def refresh_status(self):
        try:
            if client.containers.get(self.name).status == "running":
                self.status = True
            else:
                self.status = False
        except:
            self.status = False
        return

    def create(self):
        try:
            if self.id != 1:                                
                raise Exception("Sandbox Limit Reached")
            if self.type == "lwm2m":
                client.containers.create("m4n3dw0lf/dtls-lightweightm2m-iotagent", 
                   name=self.name, 
                   network="host",
                   volumes={
                            '/opt/secrets/ssl_crt': {
                            'bind':'/opt/iota-lwm2m/cert.crt',
                            'mode':'rw'
                           },
                            '/opt/secrets/ssl_key': {
                            'bind':'/opt/iota-lwm2m/cert.key',
                            'mode':'rw'
                           }
                   }
                )
                self.created = True
            else:
                self.created = False
        except:
            self.created = False
        return

    def set_broker(self,broker_ip,broker_name,broker_context,broker_port):
        if self.created == True:
            client.containers.get(self.name).exec_run("sed -i '62,78s/{}/{}/' config-secure.js".format(self.broker_ip,broker_ip))
            if broker_context == "http":
              self.broker_context = "http"
              client.containers.get(self.name).exec_run('sed -i \'64s/https/http/\' config-secure.js')
	    else:
              self.broker_context = "https"
              client.containers.get(self.name).exec_run('sed -i \'64s/http/https/\' config-secure.js')
            log.debug('Broker context: {}'.format(broker_context))
            client.containers.get(self.name).restart()
            self.broker_ip = broker_ip
            self.broker_name = broker_name
	    self.broker_port = broker_port
        return

    def destroy(self):
        try:
          client.containers.get(self.name).stop()
        except:
          pass
        try:
          client.containers.get(self.name).remove()
          self.status = False
          self.created = False
        except:
          self.status = False
          self.created = False
        return

    def start(self):
        try:
            client.containers.get(self.name).start()
        except: 
            pass
        return

    def stop(self):
        try:
            client.containers.get(self.name).stop()
        except:
            pass
        return

    def grant_device(self,endp):
        device = Device.query.filter_by(name=endp.name).first()
        if device and device in self.devices:
          return
        if not device:
          return
        message = {}
        message['services'] = []
        services = device.services
        srvs = []
        message2 = {}
        message2['devices'] = []
        dvcs = []
        for s in services:
          service = {}
          dev = {}
          dev['internal_attributes'] = {}
          attrs = s.attributes
          attributes = []
          lwm2m_attributes = {}
          for a in attrs:
              lwm2m_attributes[a.name] = {
                    "objectType":int(s.mapping),
                    "objectInstance": int(0),
                    "objectResource":int(a.mapping)
              }
              attribute = {}
              attribute['name'] = a.name
              attribute['type'] = a.type
              attributes.append(attribute)
          service['attributes'] = attributes
          dev['attributes'] = attributes
          dev['internal_attributes']['lwm2mResourceMapping'] = lwm2m_attributes
          service['type'] = s.name
          resource = s.name.lower().split() 
          service['resource'] = "/" + "_".join(resource)
          service['apikey'] = "" # Need to change later
          dev['device_id'] = device.name
          dev['entity_type'] = "Device"
          srvs.append(service)
          dvcs.append(dev)
        message2['devices'] = dvcs
        message['services'] = srvs
        print("\n\n"+json.dumps(message)+"\n\n")
        print("\n\n"+json.dumps(message2)+"\n\n")        
        headers = {
          "fiware-service":"{}".format("_".join(resource)),
          "fiware-servicepath":"/{}".format("_".join(resource)),
          "Content-Type":"application/json"
        }
        if self.encryption:
          context = "https"
        else:
          context = "http"
        for x in client.containers.get("helix-sandbox").attrs["NetworkSettings"]["Networks"].keys():
            gateway = client.containers.get("helix-sandbox").attrs["NetworkSettings"]["Networks"][x]["Gateway"]
            try:
              service_registration = requests.post("https://{}:4041/iot/services".format(gateway),
                       headers=headers,
                       json=message,
                       verify=False
                     )
            except Exception as e:
              log.debug("Can't register service: {}".format(e))
              raise e
            print("\n\n"+service_registration.text+"\n\n")
            try:
              device_registration = requests.post('https://{}:4041/iot/devices'.format(gateway),
                       headers=headers,
                       json=message2,
                       verify=False
                    )
            except Exception as e:
              log.debug("Can't register device: {}".format(e))
              raise e
            print("\n\n"+device_registration.text+"\n\n")
            subscription = {
              "description": "Notify Cygnus of all {} context changes".format(self.name),
              "subject": {
               "entities": [
                 {
                   "idPattern": ".*"
                 }
               ]
              },
              "notification": {
                "http": {
                  "url": "http://{}:5050/notify".format(gateway)
                },
              "attrsFormat": "legacy"
              },
                "throttling": 5
            }
            try:
              log.debug('Broker context: {}'.format(self.broker_context))
              cygnus_registration = requests.post('{}://{}:{}/v2/subscriptions'.format(self.broker_context,gateway,self.broker_port),
                      headers=headers,
                      json=subscription,
                      verify=False
                    )
            except Exception as e:
              log.debug("Can't register subscription: {}".format(e))
              log.debug('{}://{}:{}/v2/subscriptions'.format(self.broker_context,gateway,self.broker_port))
              raise e
            print("\n\n"+cygnus_registration.text+"\n\n")
        self.devices.append(device)

    def revoke_device(self,endp):
        device = Device.query.filter_by(name=endp.name).first()
        if not device or not device in self.devices:
          return
        self.devices.remove(device)



class Broker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description=db.Column(db.String(200))
    ip = db.Column(db.String(60))
    port = db.Column(db.String(5), default="1026", unique=True)
    tls = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=False)
    created = db.Column(db.Boolean, default=False)
    config = db.Column(db.Text)
    agents = db.relationship('Agent', secondary="broker_association",
      lazy='dynamic'
    )

    def refresh_status(self):
        try:
            if client.containers.get(self.name).status == "running":
                self.status = True
            else:
                self.status = False
        except:
            self.status = False
        return

    def create(self):
        try:
	     if self.id != 1:
               raise Exception("Sandbox Limit Reached")
             client.containers.create("mongo:3.4",
		command=" --nojournal",
                ports={"27017/tcp":"27017"},
	     	name="{}_mongodb".format(self.name),
	     )
             client.containers.create("fiware/cygnus-ngsi:1.7.1",
	        name="{}_cygnus".format(self.name),
                environment=[
                "CYGNUS_MONGO_HOSTS={}_mongodb:27017".format(self.name),
                "CYGNUS_LOG_LEVEL=DEBUG",
                "CYGNUS_SERVICE_PORT=5050",
                "CYGNUS_API_PORT=5080"
                ],
                ports={"5050/tcp":"5050","5080/tcp":"5080"},
                links=[("{}_mongodb".format(self.name),"{}_mongodb".format(self.name))]
	     )
             if self.tls:
                cmd = " -dbhost {}_mongodb -https -key /etc/orion-ssl/cert.key -cert /etc/orion-ssl/cert.crt".format(self.name)
             else:
                cmd = " -dbhost {}_mongodb".format(self.name)
             client.containers.create("fiware/orion:1.10.0", 
		command=cmd,
                name=self.name,
                ports={"1026/tcp":self.port},
                links=[("{}_mongodb".format(self.name),"{}_mongodb".format(self.name)),
                       ("{}_cygnus".format(self.name),"{}_cygnus".format(self.name))
                      ],
                volumes={
                         '/opt/secrets/ssl_crt': {
                         'bind':'/etc/orion-ssl/cert.crt',
                         'mode':'rw'
                        },  
                         '/opt/secrets/ssl_key': {
                         'bind':'/etc/orion-ssl/cert.key',
                         'mode':'rw'
                        }
                }
             )
             self.created = True
        except:
             self.created = False
        return

    def destroy(self):
        try:
          client.containers.get(self.name).stop()
	  client.containers.get("{}_mongodb".format(self.name)).stop()
	  client.containers.get("{}_cygnus".format(self.name)).stop()
        except:
          pass
        client.containers.get(self.name).remove()
	client.containers.get("{}_mongodb".format(self.name)).remove()
	client.containers.get("{}_cygnus".format(self.name)).remove()
        self.status = False
        self.created = False
        return

    def start(self):
	client.containers.get("{}_mongodb".format(self.name)).start()
	client.containers.get("{}_cygnus".format(self.name)).start()
        client.containers.get(self.name).start()
        return

    def stop(self):
        try:
            client.containers.get(self.name).stop()
	    client.containers.get("{}_mongodb".format(self.name)).stop()
	    client.containers.get("{}_cygnus".format(self.name)).stop()
        except:
            pass
        return

    def grant_agent(self,endp):
        agent = Agent.query.filter_by(name=endp.name).first()
        if agent and agent in self.agents:
          return
        if not agent:
          return
        self.agents.append(agent)

    def revoke_agent(self,endp):
        agent = Agent.query.filter_by(name=endp.name).first()
        if not agent or not agent in self.agents:
          return
        self.agents.remove(agent)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    encrypted_password_hash = db.Column(db.String(2048))
    encrypted_api_key = db.Column(db.String(512))
    devices = db.relationship('Device',secondary="user_device_association",
      lazy='dynamic'
    )
    is_admin = db.Column(db.Boolean, default=False) 
    @property
    def api_key(self):
        return cipher.decrypt(self.encrypted_api_key)
    @api_key.setter
    def api_key(self, token):
        self.encrypted_api_key = cipher.encrypt(token)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')
    @password.setter
    def password(self, password):
        password_hash = generate_password_hash(password)
        encrypted_hash = cipher.encrypt(password_hash)
        self.encrypted_password_hash = encrypted_hash
    def verify_password(self, password):
        decrypted_hash = cipher.decrypt(self.encrypted_password_hash)
        return check_password_hash(decrypted_hash, password)
    def has_device(self,name):
        device = Device.query.filter_by(name=name).first()
        if not device or not device in self.devices:
          return False
        return True
    def grant_device(self,endp):
        device = Device.query.filter_by(name=endp.name).first()
        if device and device in self.devices:
          return
        if not device:
          return
        self.devices.append(device)
    def revoke_device(self,endp):
        device = Device.query.filter_by(name=endp.name).first()
        if not device or not device in self.devices:
          return
        self.devices.remove(device)
    def __repr__(self):
        return '<User: {}>'.format(self.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

