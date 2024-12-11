import sys
import signal
from flask import Flask
from src.routes.ejson_encoder import MongoJSONEncoder
from prometheus_flask_exporter import PrometheusMetrics

from src.config.config import config
from src.utils.mongo_io import MongoIO
from src.routes.encounter_routes import create_encounter_routes
from src.routes.config_routes import create_config_routes
from src.routes.mentor_routes import create_mentor_routes
from src.routes.people_routes import create_people_routes
from src.routes.plan_routes import create_plan_routes

# Initialize Logging
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize Flask App
app = Flask(__name__)
app.json = MongoJSONEncoder(app)

# Initialize Database Connection, and load one-time data
mongo = MongoIO()
mongo.initialize()

logger.info(f"API Version {config}")

# Apply Prometheus monitoring middleware
metrics = PrometheusMetrics(app, path='/api/health/')
metrics.info('app_info', 'Application info', version=config.api_version)

# Initialize Route Handlers
config_handler = create_config_routes()
encounter_handler = create_encounter_routes()
plan_handler = create_plan_routes()
people_handler = create_people_routes()
mentor_handler = create_mentor_routes()

# Register routes
app.register_blueprint(encounter_handler, url_prefix='/api/encounter')
app.register_blueprint(config_handler, url_prefix='/api/config')
app.register_blueprint(plan_handler, url_prefix='/api/plan')
app.register_blueprint(people_handler, url_prefix='/api/people')
app.register_blueprint(mentor_handler, url_prefix='/api/mentor')

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