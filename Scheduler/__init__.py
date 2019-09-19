from flask import Flask
from Helper import Log
from Status import Status
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from Helper import Config
from .heartbeat import HeartBeat

config = Config()
print("Config validation:")
for level, message in config.Validation:
    print(f"  {level.name:8}: {message}")

app = Flask(__name__)
app.config.from_mapping(config.Flask)
bootstrap = Bootstrap(app)
moment = Moment(app)
Log.Initialize(app)
Status.Initialize()
HeartBeat.Initialize()

from Scheduler.experiment import bp as ExperimentBp
app.register_blueprint(ExperimentBp, url_prefix='/experiment')

from Scheduler.dispatcher import bp as DispatcherBp
app.register_blueprint(DispatcherBp, url_prefix='/api/v0')

from Scheduler import routes
