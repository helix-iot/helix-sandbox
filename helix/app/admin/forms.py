
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField, SelectField, TextAreaField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Agent, Device, Service, Attribute

__author__ = "m4n3dw0lf"

class BrokerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ip = StringField('IP Address')
    port = StringField('Port')
    tls = BooleanField('TLS')
    description = StringField('Description')
    submit = SubmitField('Submit')

class AgentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type',choices=[("lwm2m","LWM2M")])
    port = StringField('Port')
    encryption = BooleanField('TLS/DTLS')
    description = StringField('Description')
    submit = SubmitField('Submit')

class ServiceForm(FlaskForm):
    mapping = StringField('Object ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')

class DeviceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    ip = StringField('IP Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AttributeForm(FlaskForm):
    mapping = StringField('Resource ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type',choices=[("Integer","Integer"), ("Float","Float"), ("String","String"), ("Boolean","Boolean")],validators=[DataRequired()])
    operation = SelectField('Operation',choices=[("R","R"), ("W","W"), ("RW","RW"), ("E","E")],validators=[DataRequired()])
    mandatory = BooleanField('Mandatory')
    description = StringField('Description')
    submit = SubmitField('Submit')


class ServiceAssignForm(FlaskForm):
    attribute = QuerySelectField(query_factory=lambda: Attribute.query.all(),
                                    get_label="name")
    submit = SubmitField('Submit')

class DeviceAssignForm(FlaskForm):
    service = QuerySelectField(query_factory=lambda: Service.query.all(),
                                    get_label="name")
    submit = SubmitField('Submit')

class AgentAssignForm(FlaskForm):
    device = QuerySelectField(query_factory=lambda: Device.query.all(),
                                    get_label="name")
    submit = SubmitField('Submit')

class BrokerAssignForm(FlaskForm):
    agent = QuerySelectField(query_factory=lambda: Agent.query.all(),
                                get_label="name")
    submit = SubmitField('Submit')

class UserAssignForm(FlaskForm):
    device = QuerySelectField(query_factory=lambda: Device.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')
