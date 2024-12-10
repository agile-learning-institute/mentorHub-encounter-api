# Initialize Logging
import logging

from src.routes.ejson_encoder import MongoJSONEncoder
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import sys
import signal
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from src.config.config import config
from src.utils.mongo_io import MongoIO
from src.routes.encounter_routes import create_encounter_routes
from src.routes.config_routes import create_config_routes

# Initialize Flask App
app = Flask(__name__)
app.json = MongoJSONEncoder(app)

# Initialize Database Connection, and load one-time data
mongo = MongoIO()
mongo.initialize()

# Apply Prometheus monitoring middleware
metrics = PrometheusMetrics(app, path='/api/health/')
metrics.info('app_info', 'Application info', version=config.api_version)

# Initialize Route Handlers
config_handler = create_config_routes()
encounter_handler = create_encounter_routes()
# TODO Other handlers as needed
# plan_handler = create_plan_routes()

# Register routes
app.register_blueprint(encounter_handler, url_prefix='/api/encounter')
app.register_blueprint(config_handler, url_prefix='/api/config')
# TODO Other routes as needed
# app.register_blueprint(plan_handler, url_prefix='/api/plan')

# Define a signal handler for SIGTERM and SIGINT
def handle_exit(signum, frame):
    logger.info(f"Received signal {signum}. Initiating shutdown...")
    mongo.disconnect()
    logger.info('MongoDB connection closed.')
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# Expose the app object for Gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.get_port())