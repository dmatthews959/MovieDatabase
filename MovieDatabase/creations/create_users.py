from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.8")
db = client.Movies      # select the database
users = db.Users        # select the collection name

user_list = [
          { 
            "name" : "Declan Matthews",
            "username" : "dmatthews959",  
            "password" : b"adminpass",
            "email" : "declan_admin@googlemail.com",
            "admin" : True
          },
          { 
            "name" : "Blathnaid Moore",
            "username" : "bmoore166",  
            "password" : b"blathnaidm123",
            "email" : "blathnaidmoore27@googlemail.com",
            "admin" : False
          },
          { 
            "name" : "John Smyth",
            "username" : "jsmyth",  
            "password" : b"jsmyth123?",
            "email" : "johnsmyth@googlemail.com",
            "admin" : False
          },        
          { 
            "name" : "Ronan Larkin",
            "username" : "rlarkin672",  
            "password" : b"killeavy123",
            "email" : "ronanl@googlemail.com",
            "admin" : True
          },
          { 
            "name" : "Turlough McGivern",
            "username" : "tmac",  
            "password" : b"icansee",
            "email" : "turlmcg@googlemail.com",
            "admin" : False
          },
          { 
            "name" : "Test Admin",
            "username" : "admin1",  
            "password" : b"adminpass",
            "email" : "testadmin@googlemail.com",
            "admin" : True
          }
       ]

for new_user in user_list:
      new_user["password"] = bcrypt.hashpw(new_user["password"], bcrypt.gensalt())
      users.insert_one(new_user)
