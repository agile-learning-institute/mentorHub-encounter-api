from datetime import datetime
from bson import ObjectId
from flask import jsonify
from src.utils.mongo_io import MongoIO
import logging
logger = logging.getLogger(__name__)

class encounterService:

    @staticmethod 
    def _check_user_access(encounter_id, token):
        """Role Based Access Control logic"""
        
        # Staff can edit all encounters
        if "Staff" in token["roles"]: return
        
        # Members can access their own encounters
        encounter_member_id = MongoIO.get_member_id();
        if "Member" in token["roles"] and encounter_member_id == token["user_id"]: return
        
        # Mentors can access their apprentices encounters
        if "Mentor" in token["roles"]:
            encounter_mentor_id = MongoIO.get_mentor_id();
            if encounter_mentor_id == token["user_id"]:
                return
        
        # User has No Access! Log a warning and raise an exception
        logger.warning(f"Access Denied: {encounter_id}, {token['user_id']}, {token['roles']}")
        raise Exception("Access Denied")
      
    @staticmethod
    def create_encounter(encounter_id, token, breadcrumb):
        """Get a encounter if it exits, if not create a new one and return that"""
        encounterService._check_user_access(encounter_id, token)

        mongo_io = MongoIO()
        mongo_io.create_encounter(encounter_id, breadcrumb)
        encounter = mongo_io.get_encounter(encounter_id)
        return encounter

    @staticmethod
    def get_encounter(encounter_id, token, breadcrumb):
        """Get a encounter if it exits, if not create a new one and return that"""
        encounterService._check_user_access(encounter_id, token)

        mongo_io = MongoIO()
        mongo_io.get_encounter(encounter_id)
        encounter = mongo_io.get_encounter(encounter_id)
        return encounter

    @staticmethod
    def update_encounter(encounter_id, patch_data, token, breadcrumb):
        """Update the specified encounter"""
        encounterService._check_user_access(encounter_id, token)

        # Add breadcrumb to patch_data
        patch_data["lastSaved"] = breadcrumb
        mongo_io = MongoIO()
        mongo_io.update_encounter(encounter_id, patch_data)
        encounter = mongo_io.get_encounter(encounter_id)
        return encounter

