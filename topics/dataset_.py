"""
This example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://dataset.readthedocs.io/en/latest/.
"""
import dataset
import sqlalchemy

print(dataset.__version__)
# 1.6.2
print(sqlalchemy.__version__)
# 1.4.49

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

db = dataset.connect('sqlite:///sqlite-databases/nobel_winners.db')
db.tables
# []

# Create a table
table = db.create_table('winners2', primary_id='id', primary_type=db.types.integer)
table.create_column('category', db.types.string)
table.create_column('name', db.types.string)
table.create_column('nationality', db.types.string)
table.create_column('gender', db.types.string)
table.create_column('year', db.types.integer)
db.tables
# ['winners2']

# Delete table
table.drop()
db.tables
# []

# Insert data creating the table automatically
with db as tx:
    tx['winners2'].insert_many(nobel_winners)
db.tables
# ['winners2']

winners = db['winners2'].find()
winners = list(winners)
# [OrderedDict([('id', 1),
#               ('category', 'Physics'),
#               ('name', 'Albert Einstein'),
#               ('nationality', 'German and Swiss'),
#               ('gender', 'male'),
#               ('year', 1921)]),
#  OrderedDict([('id', 2),
#               ('category', 'Physics'),
#               ('name', 'Paul Dirac'),
#               ('nationality', 'British'),
#               ('gender', 'male'),
#               ('year', 1933)]),
#  OrderedDict([('id', 3),
#               ('category', 'Chemistry'),
#               ('name', 'Marie Curie'),
#               ('nationality', 'Polish'),
#               ('gender', 'female'),
#               ('year', 1911)])]

db['winners2'].drop()
db.tables
# []
