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
from pymongo import MongoClient

# It is recommended to use constants to avoid working with DBs of the same name
DB_NOBEL_PRIZE = 'nobel_prize'
COLL_WINNERS = 'winners'

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


def get_mongo_database(
        db_name,
        host='localhost',
        port=27017,
        username=None,
        password=None,
):
    """
    Get named database from MongoDB with(out) authentication .
    """
    # Make Mongo connection with(out) authentication
    if username and password:
        mongo_uri = f'mongodb://{username}:{password}@{host}/{db_name}'
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db_name]


db = get_mongo_database(DB_NOBEL_PRIZE)
# Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'nobel_prize')

coll = db[COLL_WINNERS]
# Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'nobel_prize'), 'winners')

coll.insert_many(nobel_winners)
# <pymongo.results.InsertManyResult at 0x7fdbacc651e0>

list(coll.find())
# [{'_id': ObjectId('651c42abbab104d494d367ca'),
#   'category': 'Physics',
#   'name': 'Albert Einstein',
#   'nationality': 'German and Swiss',
#   'gender': 'male',
#   'year': 1921},
#  {'_id': ObjectId('651c42abbab104d494d367cb'),
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
