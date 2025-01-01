from mentorhub_utils import MentorHub_Config, MentorHubMongoIO

from datetime import datetime
from bson import ObjectId
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class PlanService:
    # TODO: Review all 

    @staticmethod 
    def _check_user_access(token):
        """Role Based Access Control logic"""
        
        # Staff can edit all plans
        if "Staff" in token["roles"]: return
        
        # Mentors can edit all plans
        if "Mentor" in token["roles"]: return
        
        # User has No Access! Log a warning and raise an exception
        logger.warning(f"Access Denied: {token}")
        raise Exception("Access Denied")
         
    @staticmethod
    def create_plan(data, token, breadcrumb):
        """Get a plan if it exits, if not create a new one and return that"""
        PlanService._check_user_access(token)
        
        config = MentorHub_Config.get_instance()
        mongoIO = MentorHubMongoIO.get_instance()
        
        # Add breadcrumb and Active status
        data["lastSaved"] = breadcrumb
        data["status"] = "Active"
        
        # Add the document and fetch the updated document
        collection_name = config.PLANS_COLLECTION_NAME
        new_plan_id = mongoIO.create_document(collection_name, data)
        plan = mongoIO.get_document(collection_name, new_plan_id)
        return plan

    @staticmethod
    def get_plan(plan_id, token):
        """Get a plan if the user has access"""
        PlanService._check_user_access(token)
        
        config = MentorHub_Config.get_instance()
        mongoIO = MentorHubMongoIO.get_instance()

        collection_name = config.PLANS_COLLECTION_NAME
        plan = mongoIO.get_document(collection_name, plan_id)
        return plan

    @staticmethod
    def update_plan(plan_id, patch_data, token, breadcrumb):
        """Update the specified plan"""
        PlanService._check_user_access(token)

        config = MentorHub_Config.get_instance()
        mongoIO = MentorHubMongoIO.get_instance()

        # Add breadcrumb 
        patch_data["lastSaved"] = breadcrumb
        
        # Update the document - the updated document is returned
        collection_name = config.PLANS_COLLECTION_NAME
        plan = mongoIO.update_document(collection_name, plan_id, patch_data)
        return plan

