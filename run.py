import os, sys

from flask import redirect, url_for, request

from app import create_app

try:
  config_name = os.environ['FLASK_CONFIG']
except:
  try:
    config_name = raw_input("Configuration (production/development): ").rstrip("\n")
  except KeyboardInterrupt:
    print
    sys.exit(0)
  except:
    try:
      config_name = str(input("Configuration (production/development): ")).rstrip("\n")
    except KeyboardInterrupt:
      print
      sys.exit(0)

if config_name == "production":
  os.environ['FLASK_ENV'] = 'production'
else:
  os.environ['FLASK_ENV'] = 'development'

app, db = create_app(config_name)
db.create_all()

from app.models import User

def load_user_from_request(request):
    if current_user.is_authenticated and user.is_admin: 
      return current_user
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    api_key = request.headers.get('api-key')
    if api_key:
        try:
          api_key = api_key.replace("\n","")
        except TypeError:
          pass
        user = User.query.filter_by(api_key=api_key).first()
        if user and user.is_admin:
            return user
    return None

@app.before_request
def before_request():
  admin_created = User.query.filter_by(is_admin=True).first()
  if not admin_created and request.endpoint != 'auth.admin_setup' and request.endpoint != 'static':
    return redirect(url_for('auth.admin_setup'))



if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True)
