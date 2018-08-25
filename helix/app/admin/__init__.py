from flask import Blueprint

import threading

__author__ = "m4n3dw0lf"

admin = Blueprint('admin', __name__)

from . import views

from ..models import Agent,Broker



#agent_observer_daemon = threading.Thread(target=agent_watcher)
#broker_observer_daemon = threading.Thread(target=broker_watcher)


