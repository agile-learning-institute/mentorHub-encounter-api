from mentorhub_utils import MentorHubMongoIO, MentorHub_Config, encode_document

from datetime import datetime
from bson import ObjectId
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class EncounterService:

    @staticmethod 
    def _check_user_access(data, token):
        """Role Based Access Control logic"""
        
        # Staff can edit all encounters
        if "Staff" in token["roles"]: return
        
        # Members can access their own encounters
        if "Member" in token["roles"] and data["personId"] == token["user_id"]: return
        
        # Mentors can access their apprentices encounters
        if "Mentor" in token["roles"]:
            if data["mentorId"] == token["user_id"]:
                return
        
        # User has No Access! Log a warning and raise an exception
        logger.warning(f"Access Denied: {data}, {token}")
        raise Exception("Access Denied")
          
    @staticmethod
    def create_encounter(data, token, breadcrumb):
        """Get a encounter if it exits, if not create a new one and return that"""
        config = MentorHub_Config.get_instance()
        mongoIO = MentorHubMongoIO.get_instance()

        collection_name = config.ENCOUNTERS_COLLECTION_NAME
        EncounterService._check_user_access(data, token)
        
        # Add breadcrumb and Active status
        data["lastSaved"] = breadcrumb
        data["status"] = "Active"
        
        # Encode Mongo ObjectID and Dates
        id_properties = ["personId", "mentorId", "planId"]
        date_properties = ["date"]
        encode_document(data, id_properties, date_properties)
        
        # Add the document and fetch the updated document
        new_encounter_id = mongoIO.create_document(collection_name, data)
        encounter = mongoIO.get_document(collection_name, new_encounter_id)
        return encounter

    @staticmethod
    def get_encounter(encounter_id, token):
        """Get a encounter if the user has access"""
        config = MentorHub_Config.get_instance()
        mongoIO = MentorHubMongoIO.get_instance()

        collection_name = config.ENCOUNTERS_COLLECTION_NAME
        encounter = mongoIO.get_document(collection_name, encounter_id)
        EncounterService._check_user_access(encounter, token)
        return encounter

    @staticmethod
    def update_encounter(encounter_id, patch_data, token, breadcrumb):
        """Update the specified encounter"""
        config = MentorHub_Config.get_instance()
        mongoIO = MentorHubMongoIO.get_instance()
        collection_name = config.ENCOUNTERS_COLLECTION_NAME

        encounter = mongoIO.get_document(collection_name, encounter_id)
        EncounterService._check_user_access(encounter, token)

        # Add breadcrumb and Active status
        patch_data["lastSaved"] = breadcrumb
        
        # Encode Mongo ObjectID and Dates
        id_properties = ["personId", "mentorId", "planId"]
        date_properties = ["date"]
        encode_document(patch_data, id_properties, date_properties)
        
        # Update the document - the updated document is returned
        encounter = mongoIO.update_document(collection_name, encounter_id, patch_data)
        return encounter

