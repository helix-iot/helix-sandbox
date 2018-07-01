from os import environ
import uuid

try:
  SECRET_KEY=open(environ['CSRF_KEY']).readline().replace("\n","")
except:
  try:
    SECRET_KEY=open("./secrets/csrf_key.txt").readline().replace("\n","")
  except:
    SECRET_KEY=str(uuid.uuid1())
try:
  if environ['FLASK_CONFIG'].lower() == "production":
    try:
      mysql_host = environ['MYSQL_HOST']
    except:
      mysql_host = "localhost"
    try:
      mysql_user = environ['MYSQL_USER']
    except:
      mysql_user = "admin"
    try:
      mysql_password = open(environ['MYSQL_PASSWORD']).readline().replace("\n","")
    except:
      mysql_password=open("./secrets/mysql_password.txt").readline().replace("\n","")
    SQLALCHEMY_DATABASE_URI="mysql://{}:{}@{}/helixdb".format(mysql_user,mysql_password,mysql_host)
except KeyError:
  pass


