from flask import Blueprint, jsonify
from src.config.config import config
from src.services.person_services import PersonService
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Blueprint for mentor routes
def create_mentor_routes():
    mentor_routes = Blueprint('mentor_routes', __name__)

    # GET /api/mentors - Return TODO
    @mentor_routes.route('/', methods=['GET'])
    def get_mentors():
        try:
            result = PersonService.get_mentors() 
            return jsonify(result.to_dict()), 200
        except Exception as e:
            logger.warning(f"Get Mentors Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return mentor_routes