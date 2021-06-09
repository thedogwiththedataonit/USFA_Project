#MongoDB Connection

import pymongo 
from pymongo import MongoClient
import certifi


cluster = MongoClient("mongodb+srv://thomaspark:0806@cluster0.2kcsq.mongodb.net/python?retryWrites=true&w=majority")
db = cluster['python']
collection = db['python']

post = {"_id":0, "name":"Thom", "score":1}
collection.insert_one(post)




