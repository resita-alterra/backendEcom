from flask import Flask, request
import json
import os
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from datetime import timedelta
from functools import wraps
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

app.config['APP_DEBUG']= True

################################
# JWT
################################
app.config['JWT_SECRET_KEY'] = 'BisaResBisa'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        verify_jwt_in_request()
        role = get_jwt_identity()
        if role == 'admin':
            return fn(*args, **kwargs)
        else:
            return {'status':'Forbidden', 'message' : 'internal only'},403
    return wrapper
####################
# Database
#############

try :
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

except Exception as e :
    raise e
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://resita:alta123@localhost:3306/project' # //user:password@host/nama_database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Altabatch3@project.cwwlyuwat89s.ap-southeast-1.rds.amazonaws.com:3306/project' # //user:password@host/nama_database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

#########################################
# Middlewares
#########################################
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    app.logger.warning("REQUEST_LOG\t%s", json.dumps({
            'method' : request.method,
            'code' : response.status,
            'uri':request.full_path,
            'request': requestData, 
            'response': json.loads(response.data.decode('utf-8'))
            })
        )
    return response

#########################################
# import blueprints
#########################################

from blueprints.users.resources import bp_user
from blueprints.auth import bp_auth
from blueprints.buku.resources import bp_bacaan
from blueprints.transaksi.resources import bp_transaksi
from blueprints.auth import bp_auth
from blueprints.api import bp_weather

app.register_blueprint(bp_user,url_prefix='/user')
app.register_blueprint(bp_auth,url_prefix='/login')
app.register_blueprint(bp_bacaan, url_prefix='/bacaan')
app.register_blueprint(bp_transaksi, url_prefix='/transaksi')
app.register_blueprint(bp_weather, url_prefix='/weather')
db.create_all()
