from flask import Blueprint, request, jsonify
from src.models.token import create_token
from src.services.plan_services import planService
from src.models.breadcrumb import create_breadcrumb

import logging
logger = logging.getLogger(__name__)

def create_plan_routes():
    # Define the Blueprint
    plan_routes = Blueprint('plan_routes', __name__)

    # POST /api/plan/ - Create a plan
    @plan_routes.route('/', methods=['POST'])
    def create_plan():
        try:
            breadcrumb = create_breadcrumb()
            token = create_token()
            data = request.get_json()
            plan = planService.create_plan(data, token, breadcrumb)
            return jsonify(plan), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # GET /api/plan/{id} - Get a plan
    @plan_routes.route('/<string:id>', methods=['GET'])
    def get_plan(id):
        try:
            token = create_token()
            plan = planService.get_plan(id, token)
            return jsonify(plan), 200
        except Exception as e:
            logger.warning(f"Get plan, a processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/plan/{id} - Update a plan
    @plan_routes.route('/<string:id>', methods=['PATCH'])
    def update_plan(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb()
            data = request.get_json()
            plan = planService.update_plan(id, data, token, breadcrumb)
            return jsonify(plan), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return plan_routes