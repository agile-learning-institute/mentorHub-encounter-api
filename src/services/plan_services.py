from src.config.config import config 
from src.utils.mongo_io import mongoIO

from datetime import datetime
from bson import ObjectId
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class planService:
    # TODO: Review all 

    @staticmethod 
    def _check_user_access(data, token):
        """Role Based Access Control logic"""
        
        # Staff can edit all plans
        if "Staff" in token["roles"]: return
        
        # Members can access their own plans
        if "Member" in token["roles"] and data["personId"] == token["user_id"]: return
        
        # Mentors can access their apprentices plans
        if "Mentor" in token["roles"]:
            if data["mentorId"] == token["user_id"]:
                return
        
        # User has No Access! Log a warning and raise an exception
        logger.warning(f"Access Denied: {data}, {token}")
        raise Exception("Access Denied")
      
    @staticmethod
    def _mongo_encode(document):
        """Encode ObjectId and datetime values for MongoDB"""
        id_properties = ["personId", "mentorId", "planId", "byUser"]
        date_properties = ["date", "atTime"]
        
        def encode_value(key, value):
            """Encode identified values"""
            if key in id_properties:
                if isinstance(value, str):
                    return ObjectId(value)
                if isinstance(value, list):
                    return [ObjectId(item) if isinstance(item, str) else item for item in value]
            if key in date_properties:
                if isinstance(value, str):
                    return datetime.fromisoformat(value)
                if isinstance(value, list):
                    return [datetime.fromisoformat(item) if isinstance(item, str) else item for item in value]
            return value

        # Traverse the document and encode relevant properties
        for key, value in document.items():
            if isinstance(value, dict):
                planService._mongo_encode(value)  
            elif isinstance(value, list):
                if all(isinstance(item, dict) for item in value):
                    document[key] = [planService._mongo_encode(item) for item in value]
                else:
                    document[key] = [encode_value(key, item) for item in value]
            else:
                document[key] = encode_value(key, value)  

        return document
    
    @staticmethod
    def create_plan(data, token, breadcrumb):
        """Get a plan if it exits, if not create a new one and return that"""
        collection_name = config.get_plans_collection_name()
        planService._check_user_access(data, token)
        
        # Add breadcrumb and Active status
        data["lastSaved"] = breadcrumb
        data["status"] = "Active"
        
        # Encode Mongo ObjectID and Dates
        planService._mongo_encode(data)
        
        # Add the document and fetch the updated document
        new_plan_id = mongoIO.create_document(collection_name, data)
        plan = mongoIO.get_document(collection_name, new_plan_id)
        return plan

    @staticmethod
    def get_plan(plan_id, token):
        """Get a plan if the user has access"""
        collection_name = config.get_plans_collection_name()
        plan = mongoIO.get_document(collection_name, plan_id)
        planService._check_user_access(plan, token)
        return plan

    @staticmethod
    def update_plan(plan_id, patch_data, token, breadcrumb):
        """Update the specified plan"""
        collection_name = config.get_plans_collection_name()
        plan = mongoIO.get_document(collection_name, plan_id)
        planService._check_user_access(plan, token)

        # Add breadcrumb and Active status
        patch_data["lastSaved"] = breadcrumb
        
        # Encode Mongo ObjectID and Dates
        planService._mongo_encode(patch_data)
        
        # Update the document - the updated document is returned
        plan = mongoIO.update_document(collection_name, plan_id, patch_data)
        return plan

