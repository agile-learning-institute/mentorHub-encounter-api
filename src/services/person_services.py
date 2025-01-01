from mentorhub_utils import MentorHub_Config, MentorHubMongoIO

from datetime import datetime
from bson import ObjectId
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class PersonService:

    @staticmethod 
    def _check_rbac_access(token):
        """Role Based Access Control logic"""
        
        # Staff can view all people
        if "Staff" in token["roles"]: 
            return {}
        
        # Mentors can access their apprentices encounters
        if "Mentor" in token["roles"]:
            return {"mentorId":token["userId"]}

        # Only staff and mentors have access in this API
        logger.warning(f"access denied {token['userId']} {token["roles"]}")
        raise PermissionError("Access Denied!")
                  
    @staticmethod
    def get_people(token):
        """Get a list of people"""
        config = MentorHub_Config.get_instance()
        mongoIO = MentorHubMongoIO.get_instance()
        people_collection_name = config.PEOPLE_COLLECTION_NAME
        match = PersonService._check_rbac_access(token)
        # TODO: Add Search Query to match
        project = {"firstName": 1,"lastName": 1,"_id": 1}
                
        # Get the documents
        people = mongoIO.get_documents(people_collection_name, match, project)
        return people

    @staticmethod
    def get_mentors(token):
        """Get a list of mentors"""
        config = MentorHub_Config.get_instance()
        mongoIO = MentorHubMongoIO.get_instance()
        people_collection_name = config.PEOPLE_COLLECTION_NAME
        PersonService._check_rbac_access(token)
        match = {"roles": {"$in": ["mentor"]}}
        project = {"firstName": 1,"lastName": 1,"_id": 1}
                
        # Get the documents
        people = mongoIO.get_documents(people_collection_name, match, project)
        return people
