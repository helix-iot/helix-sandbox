from __future__ import print_function
import sys,uuid
from flask import abort, flash, redirect, render_template, url_for, Response, jsonify
from flask_login import current_user, login_required
from . import admin
from forms import AgentForm, AttributeForm, DeviceForm, ServiceForm, UserAssignForm, AgentAssignForm, ServiceAssignForm, DeviceAssignForm, BrokerForm, BrokerAssignForm
from .. import db
from ..models import Attribute, Device, Service, Agent, Broker, User

def check_admin():
    if not current_user.is_admin:
        abort(403) 

@admin.route('/attributes', methods=['GET', 'POST'])
@login_required
def list_attributes():
    check_admin()
    attributes = Attribute.query.all()
    return render_template('admin/attributes/attributes.html',
                           attributes=attributes, title="Attributes")

@admin.route('/attributes/add', methods=['GET', 'POST'])
@login_required
def add_attribute():
    check_admin()
    add_attribute = True
    form = AttributeForm()
    if form.validate_on_submit():
        attribute = Attribute(name=form.name.data,
                              type=form.type.data,
                              mapping = form.mapping.data,
                              description=form.description.data,
                              mandatory=form.mandatory.data,
                              operation=form.operation.data
                              )
        try:
            db.session.add(attribute)
            db.session.commit()
            flash('You have successfully added a new attribute.')
        except:
            flash('Error: attribute name already exists.')
        return redirect(url_for('admin.list_attributes'))
    return render_template('admin/attributes/attribute.html', action="Add",
                           add_attribute=add_attribute, form=form,
                           title="Add Attribute")


@admin.route('/attributes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_attribute(id):
    check_admin()
    add_enpoint = False
    attribute = Attribute.query.get_or_404(id)
    form = AttributeForm(obj=attribute)
    if form.validate_on_submit():
        attribute.name = form.name.data
        attribute.type = form.type.data
        attribute.mapping = form.mapping.data
        attribute.description = form.description.data
        attribute.operation = form.operation.data
        attribute.mandatory = form.mandatory.data
        db.session.commit()
        flash('You have successfully edited the attribute.')

        # redirect to the attributes page
        return redirect(url_for('admin.list_attributes'))

    form.description.data = attribute.description
    form.name.data = attribute.name
    form.operation.data = attribute.operation
    form.mapping.data = attribute.mapping
    form.type.data = attribute.type
    form.mandatory.data = attribute.mandatory
    return render_template('admin/attributes/attribute.html', action="Edit",
                           add_attribute=add_attribute, form=form,
                           attribute=attribute, title="Edit Attribute")

@admin.route('/attributes/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_attribute(id):
    check_admin()
    attribute = Attribute.query.get_or_404(id)
    db.session.delete(attribute)
    db.session.commit()
    flash('You have successfully deleted the attribute.')

    # redirect to the attributes page
    return redirect(url_for('admin.list_attributes'))

    return render_template(title="Delete Attribute")


@admin.route('/devices', methods=['GET', 'POST'])
@login_required
def list_devices():
    check_admin()
    devices = Device.query.all()
    return render_template('admin/devices/devices.html',
                           devices=devices, title="Devices")

@admin.route('/devices/add', methods=['GET', 'POST'])
@login_required
def add_device():
    check_admin()
    add_device = True
    form = DeviceForm()
    if form.validate_on_submit():
        device = Device(name=form.name.data,
                        description=form.description.data,
                        ip=form.ip.data
                       )
        try:
            db.session.add(device)
            db.session.commit()
            flash('You have successfully added a new device.')
        except:
            flash('Error: device name already exists.')
        return redirect(url_for('admin.list_devices'))
    return render_template('admin/devices/device.html', action="Add",
                           add_device=add_device, form=form,
                           title="Add Device")


@admin.route('/devices/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_device(id):
    check_admin()
    add_enpoint = False
    device = Device.query.get_or_404(id)
    form = DeviceForm(obj=device)
    if form.validate_on_submit():
        device.name = form.name.data
        device.description = form.description.data
        device.ip = form.ip.data
        db.session.commit()
        flash('You have successfully edited the device.')

        # redirect to the devices page
        return redirect(url_for('admin.list_devices'))

    form.description.data = device.description
    form.name.data = device.name
    form.mapping.data = device.mapping
    form.ip.data = device.ip
    return render_template('admin/devices/device.html', action="Edit",
                           add_device=add_device, form=form,
                           device=device, title="Edit Device")

@admin.route('/devices/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_device(id):
    check_admin()
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    flash('You have successfully deleted the device.')

    # redirect to the devices page
    return redirect(url_for('admin.list_devices'))



@admin.route('/devices/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_device(id):
    check_admin()
    device = Device.query.get_or_404(id)
    form = DeviceAssignForm(obj=device)
    assign_device = True
    if form.validate_on_submit():
        device.grant_service(form.service.data)
        db.session.add(device)
        db.session.commit()
        flash('You have successfully assigned an device.')
        return redirect(url_for('admin.list_devices'))
    return render_template('admin/devices/device.html',
                           device=device, form=form,
                           assign_device=assign_device,
                           title='Assign Device')

@admin.route('/devices/revoke/<int:id>',methods=['GET','POST'])
@login_required
def revoke_device(id):
    check_admin()
    device = Device.query.get_or_404(id)
    form = DeviceAssignForm(obj=device)
    unassign_device = True
    if form.validate_on_submit():
        device.revoke_service(form.service.data)
        db.session.add(device)
        db.session.commit()
        flash('You have successfully revoked an device.')
        return redirect(url_for('admin.list_devices'))
    return render_template('admin/devices/device.html',
                           device=device, form=form,
                           unassign_device=unassign_device,
                           title='Revoke Device')

@admin.route('/services', methods=['GET','POST'])
@login_required
def list_services():
    check_admin()
    services = Service.query.all()
    return render_template('admin/services/services.html',
                           services=services, title="Services")

@admin.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    check_admin()
    add_service = True
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(name=form.name.data,
                      description=form.description.data,
                      mapping = form.mapping.data,
                     )
        try:
            db.session.add(service)
            db.session.commit()
            flash('You have successfully added a new service.')
        except:
            flash('Error: service name already exists.')
        return redirect(url_for('admin.list_services'))
    return render_template('admin/services/service.html', action="Add",
                            add_service=add_service, form=form,
                            title="Add Service")

@admin.route('/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_service(id):
    check_admin()
    add_enpoint = False
    service = Service.query.get_or_404(id)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.name = form.name.data
        service.description = form.description.data
        service.mapping = form.mapping.data
        db.session.commit()
        flash('You have successfully edited the service.')

        # redirect to the devices page
        return redirect(url_for('admin.list_services'))

    form.description.data = service.description
    form.name.data = service.name
    return render_template('admin/services/service.html', action="Edit",
                           add_service=add_service, form=form,
                           service=service, title="Edit Service")

@admin.route('/services/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_service(id):
    check_admin()
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('You have successfully deleted the service.')

    # redirect to the devices page
    return redirect(url_for('admin.list_services'))

    return render_template(title="Delete Service")


@admin.route('/services/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_service(id):
    check_admin()
    service = Service.query.get_or_404(id)
    form = ServiceAssignForm(obj=service)
    assign_service = True
    if form.validate_on_submit():
        service.grant_attribute(form.attribute.data)
        db.session.add(service)
        db.session.commit()
        flash('You have successfully assigned an device.')
        return redirect(url_for('admin.list_services'))
    return render_template('admin/services/service.html',
                           service=service, form=form,
                           assign_service=assign_service,
                           title='Assign Service')

@admin.route('/services/revoke/<int:id>',methods=['GET','POST'])
@login_required
def revoke_service(id):
    check_admin()
    service = Service.query.get_or_404(id)
    form = ServiceAssignForm(obj=service)
    unassign_service = True
    if form.validate_on_submit():
        service.revoke_attribute(form.attribute.data)
        db.session.add(service)
        db.session.commit()
        flash('You have successfully revoked an device.')
        return redirect(url_for('admin.list_services'))
    return render_template('admin/services/service.html',
                           service=service, form=form,
                           unassign_service=unassign_service,
                           title='Revoke Service')

@admin.route('/agents', methods=['GET', 'POST'])
@login_required
def list_agents():
    check_admin()
    agents = Agent.query.all()
    return render_template('admin/agents/agents.html',
                           agents=agents, title="Agents")

@admin.route('/agents/add', methods=['GET', 'POST'])
@login_required
def add_agent():
    check_admin()
    add_agent = True
    form = AgentForm()
    if form.validate_on_submit():
        agent = Agent(name=form.name.data,
                      type=form.type.data,
                      port=form.port.data,
                      encryption=form.encryption.data,
                      description=form.description.data,
                     )
        try:
            db.session.add(agent)
            db.session.commit()
            flash('You have successfully added a new agent.')
        except:
            flash('Error: agent name or port already in use.')
        return redirect(url_for('admin.list_agents'))
    form.encryption.data = True
    form.port.data = 5684
    return render_template('admin/agents/agent.html', action="Add",
                           add_agent=add_agent, form=form,
                           title="Add Agent")

@admin.route('/agents/status', methods=['GET'])
def refresh_agents():
    check_admin()
    agents = Agent.query.all()
    for agent in agents:
      agent.refresh_status()
    db.session.commit()
    return redirect(url_for('admin.list_agents'))

@admin.route('/agents/create/<int:id>',methods=['GET'])
def create_agent(id):
    check_admin()
    agent = Agent.query.get_or_404(id)
    agent.create()
    db.session.commit()
    if agent.type == "lwm2m" and agent.encryption:
      flash('Create request for container {} submitted successfully.'.format(agent.name))
    else:
      flash('Container type or protocol not supported yet.')
    return redirect(url_for('admin.list_agents'))

@admin.route('/agents/start/<int:id>',methods=['GET'])
def start_agent(id):
    check_admin()
    agent = Agent.query.get_or_404(id)
    agent.start()
    db.session.commit()
    flash('Start request for container {} submitted successfully.'.format(agent.name))
    return redirect(url_for('admin.list_agents'))

@admin.route('/agents/stop/<int:id>',methods=['GET'])
def stop_agent(id):
    check_admin()
    agent = Agent.query.get_or_404(id)
    agent.stop()
    db.session.commit()
    flash('Stop request for container {} submitted successfully.'.format(agent.name))
    return redirect(url_for('admin.list_agents'))

@admin.route('/agents/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_agent(id):
    check_admin()
    add_enpoint = False
    agent = Agent.query.get_or_404(id)
    form = AgentForm(obj=agent)
    if form.validate_on_submit():
        agent.name = form.name.data
        agent.type = form.type.data
        agent.port = form.port.data
        agent.encryption = form.encryption.data
        agent.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the agent.')
        # redirect to the agents page
        return redirect(url_for('admin.list_agents'))
    form.description.data = agent.description
    form.name.data = agent.name
    form.port.data = agent.port
    form.encryption.data = agent.encryption
    form.type.data = agent.type
    return render_template('admin/agents/agent.html', action="Edit",
                           add_agent=add_agent, form=form,
                           agent=agent, title="Edit Agent")

@admin.route('/agents/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_agent(id):
    check_admin()
    agent = Agent.query.get_or_404(id)
    agent.destroy()
    db.session.delete(agent)
    db.session.commit()
    flash('You have successfully deleted the agent.')
    # redirect to the agents page
    return redirect(url_for('admin.list_agents'))
    return render_template(title="Delete Agent")


@admin.route('/agents/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_agent(id):
    check_admin()
    agent = Agent.query.get_or_404(id)
    form = AgentAssignForm(obj=agent)
    assign_agent = True
    if form.validate_on_submit():
        agent.grant_device(form.device.data)
        db.session.add(agent)
        db.session.commit()
        flash('You have successfully assigned an device.')
        return redirect(url_for('admin.list_agents'))
    return render_template('admin/agents/agent.html',
                           agent=agent, form=form,
                           assign_agent=assign_agent,
                           title='Assign Agent')

@admin.route('/agents/revoke/<int:id>',methods=['GET','POST'])
@login_required
def revoke_agent(id):
    check_admin()
    agent = Agent.query.get_or_404(id)
    form = AgentAssignForm(obj=agent)
    unassign_agent = True
    if form.validate_on_submit():
        agent.revoke_device(form.device.data)
        db.session.add(agent)
        db.session.commit()
        flash('You have successfully revoked an device.')
        return redirect(url_for('admin.list_agents'))
    return render_template('admin/agents/agent.html',
                           agent=agent, form=form,
                           unassign_agent=unassign_agent,
                           title='Revoke Agent')


@admin.route('/brokers', methods=['GET', 'POST'])
@login_required
def list_brokers():
    check_admin()
    brokers = Broker.query.all()
    return render_template('admin/brokers/brokers.html',
                           brokers=brokers, title="Brokers")

@admin.route('/brokers/status', methods=['GET'])
def refresh_brokers():
    check_admin()
    brokers = Broker.query.all()
    for broker in brokers:
      broker.refresh_status()
    db.session.commit()
    return redirect(url_for('admin.list_brokers'))

@admin.route('/brokers/create/<int:id>',methods=['GET'])
def create_broker(id):
    check_admin()
    broker = Broker.query.get_or_404(id)
    broker.create()
    db.session.commit()
    flash('Create request for container {} submitted successfully.'.format(broker.name))
    return redirect(url_for('admin.list_brokers'))

@admin.route('/brokers/start/<int:id>',methods=['GET'])
def start_broker(id):
    check_admin()
    broker = Broker.query.get_or_404(id)
    broker.start()
    db.session.commit()
    flash('Start request for container {} submitted successfully.'.format(broker.name))
    return redirect(url_for('admin.list_brokers'))

@admin.route('/brokers/stop/<int:id>',methods=['GET'])
def stop_broker(id):
    check_admin()
    broker = Broker.query.get_or_404(id)
    broker.stop()
    db.session.commit()
    flash('Stop request for container {} submitted successfully.'.format(broker.name))
    return redirect(url_for('admin.list_brokers'))


@admin.route('/brokers/add', methods=['GET', 'POST'])
@login_required
def add_broker():
    check_admin()
    add_broker = True
    form = BrokerForm()
    if form.validate_on_submit():
        broker = Broker(name=form.name.data,
                      description=form.description.data,
                      ip=form.ip.data,
                      port=form.port.data,
                      tls=form.tls.data
                     )
        try:
            db.session.add(broker)
            db.session.commit()
            flash('You have successfully added a new broker.')
        except:
            flash('Error: broker name or port already registraded.')
        return redirect(url_for('admin.list_brokers'))

    form.port.data = "1026"
    form.ip.data = "127.0.0.1"

    return render_template('admin/brokers/broker.html', action="Add",
                           add_broker=add_broker, form=form,
                           title="Add Broker")


@admin.route('/brokers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_broker(id):
    check_admin()
    add_enpoint = False
    broker = Broker.query.get_or_404(id)
    form = BrokerForm(obj=broker)
    if form.validate_on_submit():
        broker.name = form.name.data
        broker.type = form.type.data
        broker.ip = form.ip.data
        broker.port = form.port.data
        broker.tls = form.tls.data
        broker.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the broker.')
        # redirect to the brokers page
        return redirect(url_for('admin.list_brokers'))
    form.name.data = broker.name
    form.type.data = broker.type
    form.ip.data = broker.ip
    form.port.data = broker.port
    form.tls.data = broker.tls
    form.description.data = broker.description
    return render_template('admin/brokers/broker.html', action="Edit",
                           add_broker=add_broker, form=form,
                           broker=broker, title="Edit Broker")

@admin.route('/brokers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_broker(id):
    check_admin()
    broker = Broker.query.get_or_404(id)
    broker.destroy()
    db.session.delete(broker)
    db.session.commit()
    flash('You have successfully deleted the broker.')
    # redirect to the brokers page
    return redirect(url_for('admin.list_brokers'))
    return render_template(title="Delete Broker")


@admin.route('/brokers/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_broker(id):
    check_admin()
    broker = Broker.query.get_or_404(id)
    form = BrokerAssignForm(obj=broker)
    assign_broker = True
    if form.validate_on_submit():
        broker.grant_agent(form.agent.data)
        db.session.add(broker)
        db.session.commit()
        flash('You have successfully assigned an agent.')
        return redirect(url_for('admin.list_brokers'))
    return render_template('admin/brokers/broker.html',
                           broker=broker, form=form,
                           assign_broker=assign_broker,
                           title='Assign Broker')

@admin.route('/brokers/revoke/<int:id>',methods=['GET','POST'])
@login_required
def revoke_broker(id):
    check_admin()
    broker = Broker.query.get_or_404(id)
    form = BrokerAssignForm(obj=broker)
    unassign_broker = True
    if form.validate_on_submit():
        broker.revoke_agent(form.agent.data)
        db.session.add(broker)
        db.session.commit()
        flash('You have successfully revoked an agent.')
        return redirect(url_for('admin.list_brokers'))
    return render_template('admin/brokers/broker.html',
                           broker=broker, form=form,
                           unassign_broker=unassign_broker,
                           title='Revoke Broker')

@admin.route('/users')
@login_required
def list_users():
    check_admin()
    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')

@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    check_admin()
    user = User.query.get_or_404(id)
    if user.is_admin:
        abort(403)
    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.grant_device(form.device.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned an device.')
        return redirect(url_for('admin.list_users'))
    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Assign User')

@admin.route('/users/revoke/<int:id>',methods=['GET','POST'])
@login_required
def revoke_user(id):
    check_admin()
    user = User.query.get_or_404(id)
    if user.is_admin:
        abort(403)
    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.revoke_device(form.device.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully revoked an device.')
        return redirect(url_for('admin.list_users'))
    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Revoke User')
