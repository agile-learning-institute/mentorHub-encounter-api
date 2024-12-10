from flask import Blueprint, jsonify
from src.config.config import config
from src.services.person_services import PersonService
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Blueprint for config routes
def create_people_routes():
    people_routes = Blueprint('people_routes', __name__)

    # GET /api/people - Return TODO
    @people_routes.route('/', methods=['GET'])
    def get_people():
        try:
            result = PersonService.get_people() # TODO: Pass Query Parameter
            return jsonify(config.to_dict()), 200
        except Exception as e:
            logger.warning(f"Get People Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return people_routes