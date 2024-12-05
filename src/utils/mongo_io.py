import logging
import sys
from datetime import datetime
from bson import ObjectId 
from pymongo import MongoClient
from src.config.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoIO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        config.get_instance()   # Ensure the config is constructed first
        if cls._instance is None:
            cls._instance = super(MongoIO, cls).__new__(cls, *args, **kwargs)
            cls._instance.connected = False
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    def initialize(self):
        """Initialize MongoDB connection and load configurations."""
        self._connect()
        self._load_versions()
        self._load_enumerators()

    def _connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(config.get_connection_string(), serverSelectionTimeoutMS=2000)
            self.client.admin.command('ping')  # Force connection
            self.db = self.client.get_database(config.get_db_name())
            self.connected = True
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.fatal(f"Failed to connect to MongoDB: {e} - exiting")
            sys.exit(1)

    def disconnect(self):
        """Disconnect from MongoDB."""
        if not self.connected: return
            
        try:
            if self.client:
                self.client.close()
                logger.info("Disconnected from MongoDB")
        except Exception as e:
            logger.fatal(f"Failed to disconnect from MongoDB: {e} - exiting")
            sys.exit(1)
      
    def _load_versions(self):
        """Load the versions collection into memory."""
        try:
            versions_collection = self.db.get_collection(config.get_version_collection_name())
            versions_cursor = versions_collection.find({})
            versions = list(versions_cursor) 
            config.versions = versions
            logger.info(f"{len(versions)} Versions Loaded.")
        except Exception as e:
            logger.fatal(f"Failed to get or load versions: {e} - exiting")
            sys.exit(1)

    def _load_enumerators(self):
        """Load the enumerators collection into memory."""
        if len(config.versions) == 0:
            logger.fatal("No Versions to load Enumerators from - exiting")
            sys.exit(1)
        
        try: 
            # Get the enumerators version from the curriculum version number.
            version_strings = [version['currentVersion'].split('.').pop() or "0" 
                            for version in config.versions 
                            if version['collectionName'] == config.get_encounters_collection_name()]
            the_version_string = version_strings.pop() if version_strings else "0"
            the_version = int(the_version_string)

            # Query the database            
            enumerators_collection = self.db.get_collection(config.get_enumerators_collection_name())
            query = { "version": the_version }
            enumerations = enumerators_collection.find_one(query)
    
            # Fail Fast if not found - critical error
            if not enumerations:
                logger.fatal(f"Enumerators not found for version: {config.get_encounters_collection_name()}:{the_version_string}")
                sys.exit(1)
    
            config.enumerators = enumerations['enumerators']
        except Exception as e:
            logger.fatal(f"Failed to get or load enumerators: {e} - exiting")
            sys.exit(1)

    def get_member_id(self, encounter_id):
        encounter = self.get_encounter(encounter_id)
        return encounter.personId
    
    def get_mentor_id(self, encounter_id):
        encounter = self.get_encounter(encounter_id)
        return encounter.mentorId
    
    def get_encounter(self, encounter_id):
        """Retrieve a encounter by ID."""
        if not self.connected:
            return None

        try:
            # Get the encounter document
            encounter_collection = self.db.get_collection(config.get_encounters_collection_name())
            encounter_object_id = ObjectId(encounter_id)
            encounter = encounter_collection.find_one({"_id": encounter_object_id})
            return encounter | {}
        except Exception as e:
            logger.error(f"Failed to get encounter: {e}")
            raise

    def create_encounter(self, person_id, mentor_id, plan_id, breadcrumb):
        """Create a curriculum by ID."""
        if not self.connected: return None

        try:
            encounter_data = {
                "person_id": ObjectId(person_id),
                "mentor_id": ObjectId(mentor_id),
                "plan_id": ObjectId(plan_id),
                "status": "Active",
                "lastSaved": breadcrumb
            }
            encounter_collection = self.db.get_collection(config.get_encounters_collection_name())
            result = encounter_collection.insert_one(encounter_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to create curriculum: {e}")
            raise   

    def update_encounter(self, encounter_id, data):
        """Update a encounter."""
        if not self.connected: return None

        try:
            encounter_collection = self.db.get_encounter(config.get_encounters_collection_name())
            encounter_object_id = ObjectId(encounter_id)
            
            match = {"_id": encounter_object_id}
            pipeline = {"$set": data}            
            result = encounter_collection.update_one(match, pipeline)
        except Exception as e:
            logger.error(f"Failed to update encounter: {e}")
            raise

        return result.modified_count

    # Singleton Getter
    @staticmethod
    def get_instance():
        """Get the singleton instance of the MongoIO class."""
        if MongoIO._instance is None:
            MongoIO()  # This calls the __new__ method and initializes the instance
        return MongoIO._instance
        
# Create a singleton instance of MongoIO
mongoIO = MongoIO.get_instance()