"""
This example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- "How to install MongoDB 6 on Ubuntu 22.04 LTS Linux (2023)" https://www.youtube.com/watch?v=HSIh8UswVVY.

# Download MongoDB Community Server
# https://www.mongodb.com/try/download/community

cd Downloads

ls

sudo dpkg -i mongodb-org-server_7.0.2_amd64.deb

sudo systemctl status mongod

○ mongod.service - MongoDB Database Server
     Loaded: loaded (/lib/systemd/system/mongod.service; disabled; vendor preset: enabled)
     Active: inactive (dead)
       Docs: https://docs.mongodb.org/manual

# Start daemon
sudo systemctl start mongod

sudo systemctl status mongod

● mongod.service - MongoDB Database Server
     Loaded: loaded (/lib/systemd/system/mongod.service; disabled; vendor preset: enabled)
     Active: active (running) since Tue 2023-10-03 18:54:07 CEST; 59s ago
       Docs: https://docs.mongodb.org/manual
   Main PID: 8129 (mongod)
     Memory: 73.9M
        CPU: 792ms
     CGroup: /system.slice/mongod.service
             └─8129 /usr/bin/mongod --config /etc/mongod.conf

# Install MongoDB Tools: MongoDB Shell
# https://www.mongodb.com/try/download/shell

ls

sudo dpkg -i mongodb-mongosh_2.0.1_amd64.deb

mongosh

Current Mongosh Log ID:	651c4a3965b8922c8158b416
Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.1
Using MongoDB:		7.0.2
Using Mongosh:		2.0.1

test> show dbs
admin   40.00 KiB
config  60.00 KiB
local   40.00 KiB

test> use mydb
switched to db mydb
mydb>

mydb> db.createCollection("mycollection")
{ ok: 1 }

mydb> show collections
mycollection

mydb> db.mycollection.insert({"name": "John DOE"})
DeprecationWarning: Collection.insert() is deprecated. Use insertOne, insertMany, or bulkWrite.
{
  acknowledged: true,
  insertedIds: { '0': ObjectId("651c4d0965b8922c8158b417") }
}

mydb> show dbs
admin    40.00 KiB
config  108.00 KiB
local    40.00 KiB
mydb     40.00 KiB

mydb> exit

# Install MongoDB Tools: MongoDB Compass (GUI)
# https://www.mongodb.com/try/download/compass

ls

sudo dpkg -i mongodb-compass_1.40.2_amd64.deb

# Stop daemon
sudo systemctl stop mongod
"""
import bson
from pymongo import MongoClient

# It is recommended to use constants to avoid creating an unwanted database
DB_NOBEL_PRIZE = 'nobel_prize'  # database
COLL_WINNERS = 'winners'  # collection

# list of dictionaries
nobel_winners = [
    {
        'category': 'Physics',
        'name': 'Albert Einstein',
        'nationality': 'German and Swiss',
        'gender': 'male',
        'year': 1921
    },
    {
        'category': 'Physics',
        'name': 'Paul Dirac',
        'nationality': 'British',
        'gender': 'male',
        'year': 1933
    },
    {
        'category': 'Chemistry',
        'name': 'Marie Curie',
        'nationality': 'Polish',
        'gender': 'female',
        'year': 1911
    }
]


def mongo_coll_to_dicts(
        client,
        dbname='test',
        coll_name='test',
        query=None,
        delete_id=True,
):
    if query is None:
        # Find all documents in the collection
        query = {}
    db = client[dbname]
    dict_list = list(db[coll_name].find(query))
    if delete_id:
        # Delete id from the list of dictionaries
        for entry in dict_list:
            entry.pop('_id')
    return dict_list


client = MongoClient()  # default: host='localhost', port=27017
# MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)

# MongoDB version
print(client.server_info()["version"])
# 7.0.2

# Create or get a database
db = client[DB_NOBEL_PRIZE]
# Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'nobel_prize')

# Create or get a collection
coll = db[COLL_WINNERS]
# Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'nobel_prize'), 'winners')

coll.insert_many(nobel_winners)
# <pymongo.results.InsertManyResult at 0x7f0169681de0>

list(coll.find())
# [{'_id': ObjectId('654d3c74725019559e886f89'),
#   'category': 'Physics',
#   'name': 'Albert Einstein',
#   'nationality': 'German and Swiss',
#   'gender': 'male',
#   'year': 1921},
#  {'_id': ObjectId('654d3c74725019559e886f8a'),
#   'category': 'Physics',
#   'name': 'Paul Dirac',
#   'nationality': 'British',
#   'gender': 'male',
#   'year': 1933},
#  {'_id': ObjectId('654d3c74725019559e886f8b'),
#   'category': 'Chemistry',
#   'name': 'Marie Curie',
#   'nationality': 'Polish',
#   'gender': 'female',
#   'year': 1911}]

# Get the generation time of the ObjectId
bson.ObjectId().generation_time  # BSON is binary JSON
# datetime.datetime(2023, 10, 4, 6, 42, 16, tzinfo=<bson.tz_util.FixedOffset object at 0x7f89d0193650>)

result = coll.find({'category': 'Chemistry'})
# <pymongo.cursor.Cursor at 0x7f89cac24990>
list(result)
# [{'_id': ObjectId('651c42abbab104d494d367cc'),
#   'category': 'Chemistry',
#   'name': 'Marie Curie',
#   'nationality': 'Polish',
#   'gender': 'female',
#   'year': 1911}]

# Find all the winners after 1930 using the $gt (greater-than) operator
list(coll.find({'year': {'$gt': 1930}}))
# [{'_id': ObjectId('651c42abbab104d494d367cb'),
#   'category': 'Physics',
#   'name': 'Paul Dirac',
#   'nationality': 'British',
#   'gender': 'male',
#   'year': 1933}]

# Find all winners after 1930 or all female winners
list(coll.find(
    {
        '$or': [
            {'year': {'$gt': 1930}},
            {'gender': 'female'},
        ]
    }
))
# [{'_id': ObjectId('651c42abbab104d494d367cb'),
#   'category': 'Physics',
#   'name': 'Paul Dirac',
#   'nationality': 'British',
#   'gender': 'male',
#   'year': 1933},
#  {'_id': ObjectId('651c42abbab104d494d367cc'),
#   'category': 'Chemistry',
#   'name': 'Marie Curie',
#   'nationality': 'Polish',
#   'gender': 'female',
#   'year': 1911}]

mongo_coll_to_dicts(client, DB_NOBEL_PRIZE, COLL_WINNERS)
# [{'category': 'Physics',
#   'name': 'Albert Einstein',
#   'nationality': 'German and Swiss',
#   'gender': 'male',
#   'year': 1921},
#  {'category': 'Physics',
#   'name': 'Paul Dirac',
#   'nationality': 'British',
#   'gender': 'male',
#   'year': 1933},
#  {'category': 'Chemistry',
#   'name': 'Marie Curie',
#   'nationality': 'Polish',
#   'gender': 'female',
#   'year': 1911}]

client.drop_database(DB_NOBEL_PRIZE)
