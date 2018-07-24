
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField, SelectField, TextAreaField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Agent, Device, Service, Attribute

class BrokerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ip = StringField('IP Address')
    port = StringField('Port')
    tls = BooleanField('TLS')
    description = StringField('Description')
    submit = SubmitField('Submit')

class AgentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type',choices=[("lwm2m","LWM2M"), ("mqtt","MQTT")])
    port = StringField('Port')
    encryption = BooleanField('TLS/DTLS')
    description = StringField('Description')
    submit = SubmitField('Submit')

class ServiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeviceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    ip = StringField('IP Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AttributeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Data Type',choices=[("integer","Integer"), ("float","Float"), ("string","String"), ("boolean","Boolean") ])
    mapping = StringField('Mapping', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')

class DeviceAssignForm(FlaskForm):
    attribute = QuerySelectField(query_factory=lambda: Attribute.query.all(),
                                    get_label="name")
    submit = SubmitField('Submit')

class ServiceAssignForm(FlaskForm):
    device = QuerySelectField(query_factory=lambda: Device.query.all(),
                                    get_label="name")
    submit = SubmitField('Submit')

class AgentAssignForm(FlaskForm):
    service = QuerySelectField(query_factory=lambda: Service.query.all(),
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
