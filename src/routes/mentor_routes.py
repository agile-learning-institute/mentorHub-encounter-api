from flask import Blueprint, jsonify
from mentorhub_utils import create_breadcrumb, create_token
from src.services.person_services import PersonService
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Blueprint for mentor routes
def create_mentor_routes():
    mentor_routes = Blueprint('mentor_routes', __name__)

    # GET /api/mentors - Return a list of Mentor's
    @mentor_routes.route('/', methods=['GET'])
    def get_mentors():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            result = PersonService.get_mentors(token) 
            return jsonify(result), 200
        except Exception as e:
            logger.warning(f"Get Mentors Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return mentor_routes