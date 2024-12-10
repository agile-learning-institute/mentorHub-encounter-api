from src.config.config import config 
from src.utils.mongo_io import mongoIO

from datetime import datetime
from bson import ObjectId
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class PersonService:

    @staticmethod 
    def _rbac_filter(match, data, token):
        """Role Based Access Control logic"""
        
        # PUT THIS SOMEWHERE
        
        # Staff can view all people
        if "Staff" in token["roles"]: return match
        
        # Mentors can access their apprentices encounters
        if "Mentor" in token["roles"]:
            match["mentorId"] = data["mentorId"]
            return match

        # Only staff and mentors have access in this API
        logger.warning(f"access denied {token["userId"]} {token["roles"]}")
        raise "Access Denied!"
                  
    @staticmethod
    def get_people(match, token):
        """Get a list of people"""
        people_collection_name = "" # TODO: config.get_people_collection_name()
        match = {} # TODO: populate from query parameters like query=firstName
        match = PersonService._rbac_filter(match, token) 
        project = {"firstName": 1,"lastName": 1,"_id": 1}
                
        # Get the documents
        people = mongoIO.get_documents(people_collection_name, match, project)
        return people

    @staticmethod
    def get_mentors(encounter_id, token):
        """Get a list of mentors"""
        people_collection_name = "" # TODO: config.get_people_collection_name()
        match = {"roles": {"$contains":"mentor"} }
        project = {"firstName": 1,"lastName": 1,"_id": 1}
                
        # Get the documents
        people = mongoIO.get_documents(people_collection_name, match, project)
        return people

