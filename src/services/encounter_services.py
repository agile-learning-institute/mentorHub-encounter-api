from src.config.config import config 
from src.utils.mongo_io import mongoIO
from datetime import datetime
from bson import ObjectId
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class encounterService:

    @staticmethod 
    def _check_user_access(data, token):
        """Role Based Access Control logic"""
        
        # Staff can edit all encounters
        if "Staff" in token["roles"]: return
        
        # Members can access their own encounters
        if "Member" in token["roles"] and data["person_id"] == token["user_id"]: return
        
        # Mentors can access their apprentices encounters
        if "Mentor" in token["roles"]:
            if data.mentor_id == token["user_id"]:
                return
        
        # User has No Access! Log a warning and raise an exception
        logger.warning(f"Access Denied: {data}, {token}")
        raise Exception("Access Denied")
      
    @staticmethod
    def _get_ids(encounter_id):
        encounter = mongoIO.get_document(encounter_id)
        ids = {
            "person_id": str(encounter["person_id"]),
            "mentor_id": str(encounter["mentor_id"]),
            "plan_id": str(encounter["plan_id"])
        }
        return ids

    @staticmethod
    def create_encounter(data, token, breadcrumb):
        """Get a encounter if it exits, if not create a new one and return that"""
        encounterService._check_user_access(data, token)
        
        collection_name = config.get_encounters_collection_name()
        logger.info(f"create_encounter called with {data}")
        encounter_data = {
            "person_id": ObjectId(data["person_id"]),
            "mentor_id": ObjectId(data["mentor_id"]),
            "plan_id": ObjectId(data["plan_id"]),
            "status": "Active",
            "lastSaved": breadcrumb
        }

        new_encounter_id = mongoIO.create_document(collection_name, encounter_data)
        encounter = mongoIO.get_document(new_encounter_id)
        return encounter

    @staticmethod
    def get_encounter(encounter_id, token):
        """Get a encounter if the user has access"""
        collection_name = config.get_encounters_collection_name()
        encounter = mongoIO.get_document(collection_name, encounter_id)
        user_ids = {
            "person_id": str(encounter["person_id"]),
            "mentor_id": str(encounter["mentor_id"]),
            "plan_id": str(encounter["plan_id"])
        }
        encounterService._check_user_access(user_ids, token)
        return encounter

    @staticmethod
    def update_encounter(encounter_id, patch_data, token, breadcrumb):
        """Update the specified encounter"""
        user_ids = encounterService._get_ids(encounter_id)
        encounterService._check_user_access(encounter_id, token)

        # Add breadcrumb to patch_data
        patch_data["lastSaved"] = breadcrumb
        
        collection_name = config.get_encounters_collection_name()
        encounter = mongoIO.update_document(collection_name, encounter_id, patch_data)
        return encounter

