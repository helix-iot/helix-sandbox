from flask import Blueprint

__author__ = "m4n3dw0lf"

admin = Blueprint('admin', __name__)

from . import views

from ..models import Attribute

def bootstrap():
  attributes = { 
    "Digital Input State":{
      "id": "5500",
      "op": "R",
      "type":"Boolean"
    },  
    "Digital Input Counter":{
      "id": "5501",
      "op": "R",
      "type":"Integer"
    },  
    "Digital Input Polarity":{
      "id":"5502",
      "op": "R/W",
      "type":"Boolean"
    },  
    "Digital Input Debounce":{
      "id":"5503",
      "op":"R/W",
      "type":"Integer"
    },  
    "Digital Input Edge Selection":{
      "id":"5504",
      "op":"R/W",
      "type":"Integer"
    }   
  }
  try:
    Attribute.query.first()
    return True
  except:
    try:
      for attribute in attributes.keys():
        attr = attributes[attribute]
        db_attr = Attribute(
                     name = attribute,
                     type = attr['type'],
                     mapping = attr['id'],
                     operation = attr['op']
                  )
        db.session.add(db_attr)
      db.session.commit()
      return True
    except Exception as e:
      return False

bootstrap()

