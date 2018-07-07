from __future__ import print_function
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sys, uuid, base64
import docker
from time import sleep
client = docker.from_env()
from app import db, login_manager
from simple_aes_cipher import AESCipher, generate_secret_key
from os import environ,urandom
from getpass import getpass

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
  db.Column('attribute_id',db.Integer,
             db.ForeignKey('attribute.id')),
  db.Column('device_id',db.Integer,
            db.ForeignKey('device.id'))
)

service_association = db.Table('service_association',
  db.Column('device_id',db.Integer,
             db.ForeignKey('device.id')),
  db.Column('service_id',db.Integer,
             db.ForeignKey('service.id'))
)

agent_association = db.Table('agent_association',
  db.Column('service_id',db.Integer,
            db.ForeignKey('service.id')),
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
    mapping = db.Column(db.String(60))
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    device = db.relationship('Device', secondary="device_association",
      lazy='dynamic'
    )

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    ip = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    attributes = db.relationship('Attribute',secondary="device_association",
      lazy='dynamic'
    )
    services = db.relationship('Service',secondary="service_association",
      lazy='dynamic'
    )
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

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    type = db.Column(db.String(200))
    readonly = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(200))
    devices = db.relationship('Device', secondary="service_association",
      lazy='dynamic'
    )
    agents = db.relationship('Agent', secondary="agent_association",
      lazy='dynamic'
    )
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

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))
    type = db.Column(db.String(50), default="lwm2m")
    port = db.Column(db.String(5), default="5684")
    encryption = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=False)
    config = db.Column(db.Text)
    services = db.relationship('Service', secondary="agent_association",
      lazy='dynamic'
    )

    def refresh_status(self):
        if client.containers.get(self.name).status == "running":
          self.status = True
        else:
          self.status = False
        return

    def start(self):
        client.containers.get(self.name).start()
        if client.containers.get(self.name).status == "running":
          self.status = True
        else:  
          self.status = False
        return

    def stop(self):
        client.containers.get(self.name).stop()
        if client.containers.get(self.name).status == "stopped":
            self.status = False
        else:
            self.status = True
        return

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

class Broker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description=db.Column(db.String(200))
    ip = db.Column(db.String(60))
    port = db.Column(db.String(5), default="1026")
    tls = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=False)
    config = db.Column(db.Text)
    agents = db.relationship('Agent', secondary="broker_association",
      lazy='dynamic'
    )

    def refresh_status(self):
        if client.containers.get(self.name).status == "running":
          self.status = True
        else:
          self.status = False
        return

    def start(self):
        client.containers.get(self.name).start()
        if client.containers.get(self.name).status == "running":
          self.status = True
          return True
        else:  
          self.status = False
          return False

    def stop(self):
        client.containers.get(self.name).stop()
        if client.containers.get(self.name).status == "exited":
            self.status = False
            return True
        else:
            self.status = True
            return False

    def grant_agent(self,endp):
        agent = Agent.query.filter_by(name=endp.name).first()
        if agent and agent in self.agents:
          return
        if not agent:
          return
        self.agents.append(agent)
    def revoke_agent(self,endp):
        agent = Service.query.filter_by(name=endp.name).first()
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

