from src.config.config import config 
from src.utils.mongo_io import mongoIO
from datetime import datetime
from bson import ObjectId
from flask import jsonify
import logging

logger = logging.getLogger(__name__)
#############
## TODO: 
## - Encoding of OID values and dates
#############
## TODO: Open an Issue
## - Require future date, personId and mentorId on create
## - Disallow personId and mentorId updates unless Staff
## - Disallow date update values before now() unless Staff
###########
## TODO: New Schema Required
## - New properties for start date-time and end date-time
## - New Statuses of Scheduled, Active, Completed, Cancelled, Archived
## - Disallow status updates other that Scheduled -> Cancelled or * -> Archived
## - Disallow date changes unless status == Scheduled
## - Disallow observation updates unless status == Active
## - Disallow start/end updates
## - Start endpoint - If Status = Scheduled, sets status to Active and records start time
## - End endpoint - If Status = Active, sets status to Completed and record end time

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
    def _get_ids(collection_name, encounter_id):
        encounter = mongoIO.get_document(collection_name, encounter_id)
        ids = {
            "personId": str(encounter["personId"]),
            "mentorId": str(encounter["mentorId"])
        }
        return ids

    @staticmethod
    def create_encounter(data, token, breadcrumb):
        """Get a encounter if it exits, if not create a new one and return that"""
        collection_name = config.get_encounters_collection_name()
        encounterService._check_user_access(data, token)
        data["lastSaved"] = breadcrumb
        data["status"] = "Active"

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
        user_ids = encounterService._get_ids(collection_name, encounter_id)
        encounterService._check_user_access(user_ids, token)

        # Add breadcrumb to patch_data
        patch_data["lastSaved"] = breadcrumb
        
        encounter = mongoIO.update_document(collection_name, encounter_id, patch_data)
        return encounter

