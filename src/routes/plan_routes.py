from flask import Blueprint, request, jsonify
from mentorhub_utils import create_breadcrumb, create_token
from src.services.plan_services import PlanService

import logging
logger = logging.getLogger(__name__)

def create_plan_routes():
    # Define the Blueprint
    plan_routes = Blueprint('plan_routes', __name__)

    # POST /api/plan/ - Create a plan
    @plan_routes.route('/', methods=['POST'])
    def create_plan():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            data = request.get_json()
            plan = PlanService.create_plan(data, token, breadcrumb)
            return jsonify(plan), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # GET /api/plan/{id} - Get a plan
    @plan_routes.route('/<string:id>', methods=['GET'])
    def get_plan(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            plan = PlanService.get_plan(id, token)
            return jsonify(plan), 200
        except Exception as e:
            logger.warning(f"Get plan, a processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/plan/{id} - Update a plan
    @plan_routes.route('/<string:id>', methods=['PATCH'])
    def update_plan(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            data = request.get_json()
            plan = PlanService.update_plan(id, data, token, breadcrumb)
            return jsonify(plan), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return plan_routes