from datetime import datetime
from pathlib import Path
from bson import ObjectId

import os
import logging

logger = logging.getLogger(__name__)

class Config:
    _instance = None  # Singleton instance

    def __init__(self):
        if Config._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Config._instance = self
            self.config_items = []
            self.versions = []
            self.enumerators = {}
            self.api_version = ""

            # Private properties
            self.CONFIG_FOLDER = "./"
            self.PORT = 8088
            self.CONNECTION_STRING = ""
            self.DB_NAME = ""
            self.VERSION_COLLECTION_NAME = ""
            self.ENUMERATORS_COLLECTION_NAME = ""
            self.ENCOUNTERS_COLLECTION_NAME = ""
            self.PLANS_COLLECTION_NAME = ""
            self.PEOPLE_COLLECTION_NAME = ""

            # Initialize configuration
            self.initialize()

    def initialize(self):
        """Initialize configuration values."""
        self.config_items = []
        self.versions = []
        self.enumerators = {}
        self.api_version = "1.0." + self._get_config_value("BUILT_AT", "LOCAL", False)
        self.CONFIG_FOLDER = self._get_config_value("CONFIG_FOLDER", "/opt/mentorhub-encounter-api", False)
        self.PORT = int(self._get_config_value("PORT", "8088", False))
        self.VERSION_COLLECTION_NAME = self._get_config_value("VERSION_COLLECTION_NAME", "msmCurrentVersions", False)
        self.ENUMERATORS_COLLECTION_NAME = self._get_config_value("ENUMERATORS_COLLECTION_NAME", "enumerators", False)
        self.ENCOUNTERS_COLLECTION_NAME = self._get_config_value("ENCOUNTERS_COLLECTION_NAME", "encounters", False)
        self.PLANS_COLLECTION_NAME = self._get_config_value("PLANS_COLLECTION_NAME", "plans", False)
        self.PEOPLE_COLLECTION_NAME = self._get_config_value("PEOPLE_COLLECTION_NAME", "people", False)
        self.CONNECTION_STRING = self._get_config_value("CONNECTION_STRING", "mongodb://mongodb:27017/?replicaSet=rs0", True)
        self.DB_NAME = self._get_config_value("DB_NAME", "mentorHub", False)
        
        logger.info(f"Configuration Initialized: {self.config_items}")
            
    def _get_config_value(self, name, default_value, is_secret):
        """Retrieve a configuration value, first from a file, then environment variable, then default."""
        value = default_value
        from_source = "default"

        # Check for config file first
        file_path = Path(self.CONFIG_FOLDER) / name
        if file_path.exists():
            value = file_path.read_text().strip()
            from_source = "file"
        # If no file, check for environment variable
        elif os.getenv(name):
            value = os.getenv(name)
            from_source = "environment"

        # Record the source of the config value
        self.config_items.append({
            "name": name,
            "value": "secret" if is_secret else value,
            "from": from_source
        })
        return value

    # Serializer
    def to_dict(self):
        """Convert the Config object to a dictionary with the required fields."""
        return {
            "api_version": self.api_version,
            "config_items": self.config_items,
            "versions": self.versions,
            "enumerators": self.enumerators
        }    

    # Singleton Getter
    @staticmethod
    def get_instance():
        """Get the singleton instance of the Config class."""
        if Config._instance is None:
            Config()
        return Config._instance
        
# Create a singleton instance of Config and export it
config = Config.get_instance()