from flask import Blueprint, request, jsonify
from src.models.token import create_token
from src.services.encounter_services import encounterService
from src.models.breadcrumb import create_breadcrumb

import logging
logger = logging.getLogger(__name__)

def create_encounter_routes():
    # Define the Blueprint
    encounter_routes = Blueprint('encounter_routes', __name__)

    # POST /api/encounter/ - Create a encounter
    @encounter_routes.route('/<string:id>', methods=['GET'])
    def create_encounter(id):
        try:
            breadcrumb = create_breadcrumb()
            token = create_token()
            data = request.get_json()
            encounter = encounterService.post_encounter(data, token, breadcrumb)
            logger.info(f"Get encounter Successful {breadcrumb}")
            return jsonify(encounter), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # GET /api/encounter/{id}/ - Get a encounter
    @encounter_routes.route('/<string:id>', methods=['GET'])
    def get_encounter(id):
        try:
            breadcrumb = create_breadcrumb()
            token = create_token()
            encounter = encounterService.get_encounter(id, token, breadcrumb)
            logger.info(f"Get encounter Successful {breadcrumb}")
            return jsonify(encounter), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/encounter/{id} - Update a encounter
    @encounter_routes.route('/<string:id>', methods=['PATCH'])
    def update_encounter(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb()
            data = request.get_json()
            encounter = encounterService.update_encounter(id, data, token, breadcrumb)
            logger.info(f"Update encounter Successful {breadcrumb}")
            return jsonify(encounter), 200
        except Exception as e:
            logger.warn(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return encounter_routes