from pymongo import MongoClient
from alfred.config import MONGODB_URI, DATABASE_NAME

# Single connection that gets reused everywhere
client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

# Collections — import these directly in other files
memories = db["alfredKnowledge"]
conversations = db["conversations"]
tasks = db["tasks"]
preferences = db["preferences"]

def ping():
    """Test MongoDB connection."""
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False