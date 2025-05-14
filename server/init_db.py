from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client['cancer_db']

if not db.counters.find_one({'_id': 'risk_records'}):
    db.counters.insert_one({'_id': 'risk_records', 'seq': 0})
    print("Initialized counter for 'risk_records'")
else:
    print("Counter for 'risk_records' already exists")