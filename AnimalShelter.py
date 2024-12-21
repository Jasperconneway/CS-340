# AnimalShelter.py

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId


""" CRUD operations for Animal collection in MongoDB """


class AnimalShelter(object):
    
    def __init__(self, username, password):
        # Intitalizing the MongoClient. Helps to
        # access the MongoDB databases and collections.
        # Hard-wired to use the aac database, the
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto enviroment.
        #
        # Connection Variables
        #
        USER = username ##'root'
        PASS = password ##'YpRfY5f0Ky'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 32905
        DB = 'aac'
        COL = 'animals'
        #
        # Initialize Connection
        #
        try:
            self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
            self.database = self.client[DB]
            self.collection = self.database[COL]
            print("Connection to MongoDB initialized successfully")
        except PyMongoError as e:
            print(f"Error initializing connection: {e}")
            
            
    def clear_database(self):
        """ Clear the entire database. """
        try:
            self.client.drop_database('aac')
            print("Database 'aac' has been cleared.")
        except PyMongoError as e:
            print(f"Error clearing database: {e}")
        
        
    def clear_collection(self):
        """ Clear all documents in the collection. """
        try:
            self.collection.delete_many({})
            print("Collection 'animals' has been cleared.")
        except PyMongoError as e:
            print(f"Error clearing collection: {e}")
            

    # Method to Implement the C in CRUD
    def create(self, data):
        """ Insert a document into the collection. """
        if data is not None: 
            try:
                self.collection.insert_one(data)
                print("Document imported successfully")
                return True   # Return True if insert was successful
            except PyMongoError as e:
                print(f"Error during insert: {e}")
                return False
        else:
            raise Exception("Data parameter is empty")
                
                
    # Method to Implement the R in CRUD
    def read(self, query):
        """" Query for documents in the collection. """
        if query is not None: 
            try:
                # find each doc that matches query
                cursor = self.collection.find(query)
                return list(cursor)
            except PyMongoError as e:
                print(f"Error during query: {e}")
                return []
        else:
            print("Query parameter is empty.")
            return []
            
            
    # Method to Implement the U in CRUD
    def update(self, query, update):
        """ Update documents in the collection. """
        if query is not None:
            try:
                # update documents that match the query
                result = self.collection.update_many(query, { '$set' : update })
                return result.modified_count   # Return the number of modified documents
            except PyMongoError as e:
                print(f"Error during update: {e}")
                return 0   # Return zero documents were modified
        else:
            print("Query parameter is empty")
            return 0    # Return zero documents were modified
            
            
    # Method to Implement the D in CRUD
    def delete(self, query):
        """ Delete documents in the collection. """
        if query is not None:
            try:
                # remove documents that match the query
                result = self.collection.delete_many(query)
                return result.deleted_count
            except PyMongoError as e:
                print(f"Error during deletion: {e}")
                return 0   # Return zero documents were removed
        else: 
            print("Query parameter is empty")
            return 0    # Return zero documents were removed
