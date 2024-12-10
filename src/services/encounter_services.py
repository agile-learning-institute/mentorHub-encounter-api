from src.config.config import config 
from src.utils.mongo_io import mongoIO

from datetime import datetime
from bson import ObjectId
from flask import jsonify
import logging

logger = logging.getLogger(__name__)
#############
## TODO: Open an Issue
## - Require future date, personId and mentorId on create
## - Disallow personId and mentorId updates unless Staff
## - Disallow date update values before now() unless Staff
###########
## TODO: New Schema Required - Issue on mongodb and encounter-api
## - New properties for start date-time and end date-time
## - New Statuses of Scheduled, Active, Completed, Cancelled, Archived
## - Disallow status updates other that Scheduled -> Cancelled or * -> Archived
## - Disallow date changes unless status == Scheduled
## - Disallow observation updates unless status == Active
## - Start endpoint - If Status = Scheduled, sets status to Active and records start time
## - End endpoint - If Status = Active, sets status to Completed and record end time
## - Disallow start/end updates

class encounterService:

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
                encounterService._mongo_encode(value)  
            elif isinstance(value, list):
                if all(isinstance(item, dict) for item in value):
                    document[key] = [encounterService._mongo_encode(item) for item in value]
                else:
                    document[key] = [encode_value(key, item) for item in value]
            else:
                document[key] = encode_value(key, value)  

        return document
    
    @staticmethod
    def create_encounter(data, token, breadcrumb):
        """Get a encounter if it exits, if not create a new one and return that"""
        collection_name = config.get_encounters_collection_name()
        encounterService._check_user_access(data, token)
        
        # Add breadcrumb and Active status
        data["lastSaved"] = breadcrumb
        data["status"] = "Active"
        
        # Encode Mongo ObjectID and Dates
        encounterService._mongo_encode(data)
        
        # Add the document and fetch the updated document
        new_encounter_id = mongoIO.create_document(collection_name, data)
        encounter = mongoIO.get_document(collection_name, new_encounter_id)
        return encounter

    @staticmethod
    def get_encounter(encounter_id, token):
        """Get a encounter if the user has access"""
        collection_name = config.get_encounters_collection_name()
        encounter = mongoIO.get_document(collection_name, encounter_id)
        encounterService._check_user_access(encounter, token)
        return encounter

    @staticmethod
    def update_encounter(encounter_id, patch_data, token, breadcrumb):
        """Update the specified encounter"""
        collection_name = config.get_encounters_collection_name()
        encounter = mongoIO.get_document(collection_name, encounter_id)
        encounterService._check_user_access(encounter, token)

        # Add breadcrumb and Active status
        patch_data["lastSaved"] = breadcrumb
        
        # Encode Mongo ObjectID and Dates
        encounterService._mongo_encode(patch_data)
        
        # Update the document - the updated document is returned
        encounter = mongoIO.update_document(collection_name, encounter_id, patch_data)
        return encounter

