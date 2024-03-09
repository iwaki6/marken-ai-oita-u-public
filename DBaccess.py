import pymongo
import os
import datetime
import pandas

ATLAS_URI = os.environ['ATLAS_URI']
DB_NAME = 'marken'
COLLECTION_NAME = 'scores'
COLLECTION_NAME2 = 'superusers'
FILEPATH = 'quiz_result.xlsx'

clientDB = pymongo.MongoClient(ATLAS_URI)

db = clientDB[DB_NAME]
collection = db[COLLECTION_NAME]
superusers = db[COLLECTION_NAME2]

def write(username,questionID,userAnswer,score):
    data = {
        'username' : username,
        'date' : datetime.date.today().strftime('%Y/%m/%d'),
        'questionID' : questionID,
        'answer' : userAnswer,
        'score' : score
    }
    try:
        collection.insert_one(data)
        return True
    except Exception as e:
        return False

def export():
    try:
        cursor = collection.find()
    except Exception as e:
        return False

    df =  pandas.DataFrame(list(cursor))
    del df['_id']
    df.to_excel(FILEPATH)
    return True

def clear():
    try:
        collection.delete_many({})
    except Exception as e:
        return False
    return True

def inquire_user(email):
    try:
        user = superusers.find_one({"email": email})
        return user
    except Exception as e:
        return None
    
