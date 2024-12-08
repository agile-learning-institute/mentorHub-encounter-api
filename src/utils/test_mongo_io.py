from copy import deepcopy
from datetime import datetime, timezone
import unittest

from bson import ObjectId
from src.config.config import config
from src.utils.mongo_io import MongoIO, mongoIO

class TestMongoIO(unittest.TestCase):
    
    def setUp(self):       
        self.test_id = "eeee00000000000000009999"
        
        MongoIO._instance = None
        mongo_io = MongoIO.get_instance()
        mongo_io.initialize()

    def tearDown(self):
        mongo_io = MongoIO.get_instance()
        mongo_io.delete_document("encounter", self.test_id)
        mongo_io.disconnect()
    
    def test_singleton_behavior(self):
        # Test that MongoIO is a singleton
        mongo_io1 = MongoIO.get_instance()
        mongo_io2 = MongoIO.get_instance()
        self.assertIs(mongo_io1, mongo_io2, "MongoIO should be a singleton")

    def test_config_loaded(self):
        # Test that Config loaded version and enumerators
        self.assertIsInstance(config.versions, list)
        self.assertEqual(len(config.versions), 9)

        self.assertIsInstance(config.enumerators, dict)

    def test_CRUD_document(self):
        # Create a Test Document
        test_data = {
            "personId": ObjectId("aaaa00000000000000000004"),
            "mentorId": ObjectId("aaaa00000000000000000027"),
            "planId": ObjectId("eeff00000000000000000002"),
            "status": "Active"
        }
        self.test_id = mongoIO.create_document("encounters", test_data)
        encounter_id_str = str(self.test_id)
        print(f"Encounter ID String {encounter_id_str}")
        
        self.assertEqual(encounter_id_str, str(self.test_id))

        # Retrieve the document
        encounter = mongoIO.get_document("encounters", encounter_id_str)
        self.assertIsInstance(encounter, dict)
        self.assertIsInstance(encounter["_id"], ObjectId)
        self.assertEqual(encounter["personId"], ObjectId("aaaa00000000000000000004"))
        self.assertEqual(encounter["mentorId"], ObjectId("aaaa00000000000000000027"))
        self.assertEqual(encounter["planId"],  ObjectId("eeff00000000000000000002"))
        
        # Update the document
        test_update = {
            "personId": ObjectId("aaaa00000000000000011111")
        }
        encounter = mongoIO.update_document("encounters", encounter_id_str, test_update)
        print(f"Update Returned {encounter}")
        self.assertIsInstance(encounter, dict)
        self.assertIsInstance(encounter["_id"], ObjectId)
        self.assertEqual(encounter["personId"], ObjectId("aaaa00000000000000011111"))
        

if __name__ == '__main__':
    unittest.main()