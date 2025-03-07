from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

class MongoManager:
    def __init__(self, db_password, db_name):
        self.uri = f"mongodb+srv://recyclewala4:{db_password}@cluster0.oa5gb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = None
        self.db_name = db_name

    def connect(self):
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def read_from_db(self, collection_name):
        try:
            db = self.client[self.db_name]
            collection = db[collection_name]
            return list(collection.find())
        except Exception as e:
            print(e)
            return []

    def write_to_db(self, collection_name, data):
        try:
            db = self.client[self.db_name]
            collection = db[collection_name]
            collection.insert_many(data)
            print("Data inserted successfully!")
        except Exception as e:
            print(e)

# # Usage
# if __name__ == "__main__":
#     db_password = "0o31l4nD7w5Iz3iy"
#     db_name = "recyclya"
#     collection_name = "users"
    
#     mongo_manager = MongoManager(db_password, db_name)
#     mongo_manager.connect()
    
#     # Read data from JSON file
#     with open('/Users/anshulmaurya/Desktop/Projects/recyclya/aws-backend/db.json', 'r') as file:
#         data = json.load(file)
    
#     # Write data to MongoDB
#     mongo_manager.write_to_db(collection_name, data)
    
#     # Read data from MongoDB
#     users = mongo_manager.read_from_db(collection_name)
#     print(users)