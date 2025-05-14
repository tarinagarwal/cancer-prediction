# init_db.py
from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)
db = client['cancer_db']

if not db.counters.find_one({'_id': 'risk_records'}):
    db.counters.insert_one({'_id': 'risk_records', 'seq': 0})
    print("Initialized counter for 'risk_records'")
else:
    print("Counter for 'risk_records' already exists")
