"""
This example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023.
"""
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


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

engine = create_engine('sqlite:///sqlite-databases/nobel_winners.db', echo=True)

# recommend: declarative mapping

# Use Base to define various tables
Base = declarative_base()


class Winner(Base):
    """
    This class corresponds to the table and the instances
    of this class correspond to the rows of the table.
    """
    __tablename__ = 'winners'
    id = Column(Integer, primary_key=True)
    category = Column(String)
    name = Column(String)
    nationality = Column(String)
    gender = Column(Enum('male', 'female'))
    year = Column(Integer)

    def __repr__(self):
        return f"<Winner(name='{self.name}', category='{self.category}', year={self.year})>"


# Create nobel_winners.db
Base.metadata.create_all(engine)
# 2023-09-27 16:20:06,517 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-09-27 16:20:06,517 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("winners")
# 2023-09-27 16:20:06,517 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2023-09-27 16:20:06,517 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("winners")
# 2023-09-27 16:20:06,517 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2023-09-27 16:20:06,518 INFO sqlalchemy.engine.Engine
# CREATE TABLE winners (
# 	id INTEGER NOT NULL,
# 	category VARCHAR,
# 	name VARCHAR,
# 	nationality VARCHAR,
# 	gender VARCHAR(6),
# 	year INTEGER,
# 	PRIMARY KEY (id)
# )
#
#
# 2023-09-27 16:20:06,518 INFO sqlalchemy.engine.Engine [no key 0.00005s] ()
# 2023-09-27 16:20:06,521 INFO sqlalchemy.engine.Engine COMMIT

# # # Add rows with a session

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Unpack our first nobel_winners member into key-value pairs: (name='Albert Einstein', category='Physics'...)
albert = Winner(**nobel_winners[0])

# Add the instance to the session
session.add(albert)
# 'new' is the set of any items that have been added to this session
print(repr(session.new))
# IdentitySet([<Winner(name='Albert Einstein', category='Physics', year=1921)>])

# Note: only after the commit method, the database is altered.
# Recommended: use as few commits as possible, allowing SQLAlchemy to work behind the scenes.

# Remove the instance from the session using expunge
session.expunge(albert)
session.new
print(repr(session.new))
# IdentitySet([])

# The expunge_all removes all new objects added to the session.
session.expunge_all()

# Add all the instancies
winner_rows = [Winner(**w) for w in nobel_winners]
session.add_all(winner_rows)
print(repr(session.new))
# IdentitySet([<Winner(name='Albert Einstein', category='Physics', year=1921)>, <Winner(name='Paul Dirac', category='Physics', year=1933)>, <Winner(name='Marie Curie', category='Chemistry', year=1911)>])
session.commit()
# 2023-09-28 08:37:40,254 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-09-28 08:37:40,259 INFO sqlalchemy.engine.Engine INSERT INTO winners (category, name, nationality, gender, year) VALUES (?, ?, ?, ?, ?) RETURNING id
# 2023-09-28 08:37:40,259 INFO sqlalchemy.engine.Engine [generated in 0.00027s (insertmanyvalues) 1/3 (ordered; batch not supported)] ('Physics', 'Albert Einstein', 'German and Swiss', 'male', 1921)
# 2023-09-28 08:37:40,260 INFO sqlalchemy.engine.Engine INSERT INTO winners (category, name, nationality, gender, year) VALUES (?, ?, ?, ?, ?) RETURNING id
# 2023-09-28 08:37:40,260 INFO sqlalchemy.engine.Engine [insertmanyvalues 2/3 (ordered; batch not supported)] ('Physics', 'Paul Dirac', 'British', 'male', 1933)
# 2023-09-28 08:37:40,260 INFO sqlalchemy.engine.Engine INSERT INTO winners (category, name, nationality, gender, year) VALUES (?, ?, ?, ?, ?) RETURNING id
# 2023-09-28 08:37:40,260 INFO sqlalchemy.engine.Engine [insertmanyvalues 3/3 (ordered; batch not supported)] ('Chemistry', 'Marie Curie', 'Polish', 'female', 1911)
# 2023-09-28 08:37:40,261 INFO sqlalchemy.engine.Engine COMMIT

# # # Query the database

cnt = session.query(Winner).count()
# 2023-09-28 08:52:56,888 INFO sqlalchemy.engine.Engine SELECT count(*) AS count_1
# FROM (SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
# FROM winners) AS anon_1
# 2023-09-28 08:52:56,888 INFO sqlalchemy.engine.Engine [generated in 0.00028s] ()
print(cnt)
# 3

# Filter by
result = session.query(Winner).filter_by(nationality='German and Swiss')
# 2023-09-28 08:52:56,890 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
# FROM winners
# WHERE winners.nationality = ?
# 2023-09-28 08:52:56,890 INFO sqlalchemy.engine.Engine [generated in 0.00024s] ('German and Swiss',)
print("type of result:", type(result))
# type of result: <class 'sqlalchemy.orm.query.Query'>
print(list(result))
# [<Winner(name='Albert Einstein', category='Physics', year=1921)>]

# Filter
result = session.query(Winner).filter(Winner.category == 'Physics', Winner.nationality != 'German and Swiss')
# 2023-09-28 08:52:56,892 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
# FROM winners
# WHERE winners.category = ? AND winners.nationality != ?
# 2023-09-28 08:52:56,892 INFO sqlalchemy.engine.Engine [generated in 0.00022s] ('Physics', 'German and Swiss')
print(list(result))
# [<Winner(name='Paul Dirac', category='Physics', year=1933)>]

# # In SQLAlchemy series 1.x, get a row based on ID number.
# # Deprecated since SQLAlchemy 2.0.
# row = session.query(Winner).get(3)
# print("type of row:", type(row))

# Since SQLAlchemy 2.0, get a row by ID
row = session.get(Winner, 3)
# 2023-09-28 10:41:08,923 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
# FROM winners
# WHERE winners.id = ?
# 2023-09-28 10:41:08,923 INFO sqlalchemy.engine.Engine [generated in 0.00016s] (3,)
print("type of row:", type(row))
# type of row: <class '__main__.Winner'>
print(row)
# <Winner(name='Marie Curie', category='Chemistry', year=1911)>

# Retrieve winners ordered by year
result = session.query(Winner).order_by('year')
# 2023-09-28 10:48:13,174 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
# FROM winners ORDER BY winners.year
# 2023-09-28 10:48:13,174 INFO sqlalchemy.engine.Engine [generated in 0.00027s] ()
print(list(result))
# [<Winner(name='Marie Curie', category='Chemistry', year=1911)>, <Winner(name='Albert Einstein', category='Physics', year=1921)>, <Winner(name='Paul Dirac', category='Physics', year=1933)>]


# Reconstruct the list of dictionaries

def inst_to_dict(inst, delete_id=True):
    dat = {}
    # Access the instance’s table class to get a list of column objects.
    for column in inst.__table__.columns:
        dat[column.name] = getattr(inst, column.name)
    if delete_id:
        # Remove the SQL primary ID item from the dictionary
        dat.pop('id')
    return dat


winner_rows = session.query(Winner)
# [<Winner(name='Marie Curie', category='Chemistry', year=1911)>, <Winner(name='Albert Einstein', category='Physics', year=1921)>, <Winner(name='Paul Dirac', category='Physics', year=1933)>]
# 2023-09-28 11:12:32,797 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
# FROM winners
# 2023-09-28 11:12:32,797 INFO sqlalchemy.engine.Engine [generated in 0.00012s] ()
nobel_winners = [inst_to_dict(w) for w in winner_rows]
print("reconstructed:", nobel_winners)
# reconstructed: [{'category': 'Physics', 'name': 'Albert Einstein', 'nationality': 'German and Swiss', 'gender': 'male', 'year': 1921}, {'category': 'Physics', 'name': 'Paul Dirac', 'nationality': 'British', 'gender': 'male', 'year': 1933}, {'category': 'Chemistry', 'name': 'Marie Curie', 'nationality': 'Polish', 'gender': 'female', 'year': 1911}]

# Update database rows
marie = session.get(Winner, 3)
marie.nationality = 'French'
# 'dirty' shows any changed instances not yet committed to the database.
print(session.dirty)
# IdentitySet([<Winner(name='Marie Curie', category='Chemistry', year=1911)>])

# Commit the changes
session.commit()
# 2023-09-28 13:21:08,440 INFO sqlalchemy.engine.Engine UPDATE winners SET nationality=? WHERE winners.id = ?
# 2023-09-28 13:21:08,440 INFO sqlalchemy.engine.Engine [generated in 0.00019s] ('French', 3)
# 2023-09-28 13:21:08,440 INFO sqlalchemy.engine.Engine COMMIT

print(session.dirty)
# IdentitySet([])

nationality = session.get(Winner, 3).nationality
# 2023-09-28 14:01:45,798 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-09-28 14:01:45,798 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
# FROM winners
# WHERE winners.id = ?
# 2023-09-28 14:01:45,798 INFO sqlalchemy.engine.Engine [cached since 0.008044s ago] (3,)
print(nationality)
# French

# Delete a row from the database
cnt = session.query(Winner).filter_by(name='Albert Einstein').delete()
# 2023-09-28 14:12:16,759 INFO sqlalchemy.engine.Engine DELETE FROM winners WHERE winners.name = ?
# 2023-09-28 14:12:16,759 INFO sqlalchemy.engine.Engine [generated in 0.00013s] ('Albert Einstein',)
print(cnt)
# 1

data = list(session.query(Winner))
# 2023-09-28 14:14:07,458 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
# FROM winners
# 2023-09-28 14:14:07,458 INFO sqlalchemy.engine.Engine [cached since 0.007961s ago] ()
print(data)
# [<Winner(name='Paul Dirac', category='Physics', year=1933)>, <Winner(name='Marie Curie', category='Chemistry', year=1911)>]

session.close()

# Drop the whole table
Winner.__table__.drop(engine)
