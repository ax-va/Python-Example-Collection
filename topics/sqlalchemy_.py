"""
This example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://docs.sqlalchemy.org/en/20/orm/session_api.html#session-api.
"""
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, desc
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

print(sqlalchemy.__version__)
# 2.0.21

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

# Create an engine for working with the database
engine = create_engine('sqlite:///sqlite-databases/nobel_winners.db', echo=True)

# # # Use declarative mapping to work with tables

# Use Base to define various tables
Base = declarative_base()


class Winner(Base):
    """
    Declarative mapping:
    This class will correspond to the table and the instances
    of this class will correspond to the rows of the table.
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


def inst_to_dict(inst, delete_id=True):
    """
    Reconstruct the list of dictionaries.
    """
    dat = {}
    # Access the instance’s table class to get a list of column objects.
    for column in inst.__table__.columns:
        dat[column.name] = getattr(inst, column.name)
    if delete_id:
        # Remove the SQL primary ID item from the dictionary
        dat.pop('id')
    return dat


# Create nobel_winners.db
Base.metadata.create_all(engine)
# ... INFO sqlalchemy.engine.Engine BEGIN (implicit)
# ... INFO sqlalchemy.engine.Engine PRAGMA main.table_info("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine
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
# ... INFO sqlalchemy.engine.Engine [no key 0.00013s] ()
# ... INFO sqlalchemy.engine.Engine COMMIT

# # # Add rows with a session

# Unpack our first nobel_winners member into key-value pairs: (name='Albert Einstein', category='Physics', ...)
albert_einstein = Winner(**nobel_winners[0])

# Create a session to interact with the database.
# Use the context manager.
Session = sessionmaker(bind=engine)

with Session() as session:
    # Add the instance to the session
    session.add(albert_einstein)
    # 'new' is the set of any items that have been added to this session
    print(repr(session.new))
    # IdentitySet([<Winner(name='Albert Einstein', category='Physics', year=1921)>])

    # Note: only after the commit method, the database is altered.
    # Recommended: use as few commits as possible, allowing SQLAlchemy to work behind the scenes.

    # Remove the instance from the session using expunge
    session.expunge(albert_einstein)
    print(repr(session.new))
    # IdentitySet([])

    # The expunge_all removes all new objects added to the session.
    session.expunge_all()
    # Add all the entries
    winner_rows = [Winner(**w) for w in nobel_winners]
    session.add_all(winner_rows)
    print(repr(session.new))
    # IdentitySet([<Winner(name='Albert Einstein', category='Physics', year=1921)>, <Winner(name='Paul Dirac', category='Physics', year=1933)>, <Winner(name='Marie Curie', category='Chemistry', year=1911)>])
    session.commit()
    # ... INFO sqlalchemy.engine.Engine BEGIN (implicit)
    # ... INFO sqlalchemy.engine.Engine INSERT INTO winners (category, name, nationality, gender, year) VALUES (?, ?, ?, ?, ?) RETURNING id
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00023s (insertmanyvalues) 1/3 (ordered; batch not supported)] ('Physics', 'Albert Einstein', 'German and Swiss', 'male', 1921)
    # ... INFO sqlalchemy.engine.Engine INSERT INTO winners (category, name, nationality, gender, year) VALUES (?, ?, ?, ?, ?) RETURNING id
    # ... INFO sqlalchemy.engine.Engine [insertmanyvalues 2/3 (ordered; batch not supported)] ('Physics', 'Paul Dirac', 'British', 'male', 1933)
    # ... INFO sqlalchemy.engine.Engine INSERT INTO winners (category, name, nationality, gender, year) VALUES (?, ?, ?, ?, ?) RETURNING id
    # ... INFO sqlalchemy.engine.Engine [insertmanyvalues 3/3 (ordered; batch not supported)] ('Chemistry', 'Marie Curie', 'Polish', 'female', 1911)
    # ... INFO sqlalchemy.engine.Engine COMMIT

    # # # Query the database

    cnt = session.query(Winner).count()
    # ... INFO sqlalchemy.engine.Engine BEGIN (implicit)
    # ... INFO sqlalchemy.engine.Engine SELECT count(*) AS count_1
    # FROM (SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners) AS anon_1
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00028s] ()
    print(cnt)
    # 3

    # Filter by
    result = session.query(Winner).filter_by(nationality='German and Swiss')
    print("type of result:", type(result))
    # type of result: <class 'sqlalchemy.orm.query.Query'>
    print(list(result))
    # ... INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # WHERE winners.nationality = ?
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00030s] ('German and Swiss',)
    # [<Winner(name='Albert Einstein', category='Physics', year=1921)>]

    # Filter
    result = session.query(Winner).filter(Winner.category == 'Physics', Winner.nationality != 'German and Swiss')
    print(list(result))
    # ... INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # WHERE winners.category = ? AND winners.nationality != ?
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00020s] ('Physics', 'German and Swiss')
    # [<Winner(name='Paul Dirac', category='Physics', year=1933)>]

    """
    # In SQLAlchemy 1.x, get a row based on ID number.
    # Deprecated since SQLAlchemy 2.0.0.
    row = session.query(Winner).get(3)
    print("type of row:", type(row))
    """

    # Since SQLAlchemy 2.0, get a row by ID
    row = session.get(Winner, 3)
    # ... INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # WHERE winners.id = ?
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00018s] (3,)
    print("type of row:", type(row))
    # type of row: <class '__main__.Winner'>
    print(row)
    # <Winner(name='Marie Curie', category='Chemistry', year=1911)>

    # Retrieve winners ordered by year
    result = session.query(Winner).order_by('year')
    print("winners ordered by years:", list(result))
    # ... INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners ORDER BY winners.year
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00010s] ()
    # winners ordered by years: [<Winner(name='Marie Curie', category='Chemistry', year=1911)>, <Winner(name='Albert Einstein', category='Physics', year=1921)>, <Winner(name='Paul Dirac', category='Physics', year=1933)>]
    # Reconstruct the list of dictionaries
    winner_rows = session.query(Winner)
    nobel_winners = [inst_to_dict(w) for w in winner_rows]
    # ... INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00010s] ()
    print("reconstructed list of dictionaries:", nobel_winners)
    # reconstructed list of dictionaries: [{'category': 'Physics', 'name': 'Albert Einstein', 'nationality': 'German and Swiss', 'gender': 'male', 'year': 1921}, {'category': 'Physics', 'name': 'Paul Dirac', 'nationality': 'British', 'gender': 'male', 'year': 1933}, {'category': 'Chemistry', 'name': 'Marie Curie', 'nationality': 'Polish', 'gender': 'female', 'year': 1911}]

    # Update database rows
    marie = session.get(Winner, 3)
    marie.nationality = 'French'
    # 'dirty' shows any changed instances not yet committed to the database.
    print(session.dirty)
    # IdentitySet([<Winner(name='Marie Curie', category='Chemistry', year=1911)>])

    # Commit the changes
    session.commit()
    # ... INFO sqlalchemy.engine.Engine UPDATE winners SET nationality=? WHERE winners.id = ?
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00030s] ('French', 3)
    # ... INFO sqlalchemy.engine.Engine COMMIT

    print(session.dirty)
    # IdentitySet([])

    nationality = session.get(Winner, 3).nationality
    # ... INFO sqlalchemy.engine.Engine BEGIN (implicit)
    # ... INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # WHERE winners.id = ?
    # ... INFO sqlalchemy.engine.Engine [cached since 0.008956s ago] (3,)
    print(nationality)
    # French

    # Delete a row from the database
    cnt = session.query(Winner).filter_by(name='Albert Einstein').delete()
    # ... INFO sqlalchemy.engine.Engine DELETE FROM winners WHERE winners.name = ?
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00014s] ('Albert Einstein',)

    # The row will not be deleted without commit()

    print(cnt)
    # 1
    print(session.new)
    # IdentitySet([])

    data = list(session.query(Winner))
    # ... INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # ... INFO sqlalchemy.engine.Engine [cached since 0.009248s ago] ()
    print(data)
    # [<Winner(name='Paul Dirac', category='Physics', year=1933)>, <Winner(name='Marie Curie', category='Chemistry', year=1911)>]
# ... INFO sqlalchemy.engine.Engine ROLLBACK

# # # Use metadata to work with the database
metadata = MetaData()
metadata.reflect(engine)
# ... INFO sqlalchemy.engine.Engine BEGIN (implicit)
# ... INFO sqlalchemy.engine.Engine SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite~_%' ESCAPE '~' ORDER BY name
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine SELECT name FROM sqlite_temp_master WHERE type='table' AND name NOT LIKE 'sqlite~_%' ESCAPE '~' ORDER BY name
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine PRAGMA main.table_xinfo("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine SELECT sql FROM  (SELECT * FROM sqlite_master UNION ALL   SELECT * FROM sqlite_temp_master) WHERE name = ? AND type in ('table', 'view')
# ... INFO sqlalchemy.engine.Engine [raw sql] ('winners',)
# ... INFO sqlalchemy.engine.Engine PRAGMA main.foreign_key_list("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine PRAGMA temp.foreign_key_list("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine SELECT sql FROM  (SELECT * FROM sqlite_master UNION ALL   SELECT * FROM sqlite_temp_master) WHERE name = ? AND type in ('table', 'view')
# ... INFO sqlalchemy.engine.Engine [raw sql] ('winners',)
# ... INFO sqlalchemy.engine.Engine PRAGMA main.index_list("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine PRAGMA temp.index_list("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine PRAGMA main.table_info("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine PRAGMA main.index_list("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine PRAGMA temp.index_list("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine PRAGMA main.table_info("winners")
# ... INFO sqlalchemy.engine.Engine [raw sql] ()
# ... INFO sqlalchemy.engine.Engine SELECT sql FROM  (SELECT * FROM sqlite_master UNION ALL   SELECT * FROM sqlite_temp_master) WHERE name = ? AND type in ('table', 'view')
# ... INFO sqlalchemy.engine.Engine [raw sql] ('winners',)
# ... INFO sqlalchemy.engine.Engine ROLLBACK
winners_table = metadata.tables["winners"]  # equivalent to Table("winners", metadata)

with Session() as session:
    result = session.query(
        winners_table
    ).filter(
        winners_table.c.year.in_(range(1911, 1922)) if True else winners_table.c.year.in_(range(1922, 1932))
    ).order_by(
        desc(winners_table.c.year)
    )
    print("winners 1911-1921:", list(result))
    # ... INFO sqlalchemy.engine.Engine BEGIN (implicit)
    # ... INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # WHERE winners.year IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ORDER BY winners.year DESC
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00027s] (1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921)
    # winners 1911-1921: [(1, 'Physics', 'Albert Einstein', 'German and Swiss', 'male', 1921), (3, 'Chemistry', 'Marie Curie', 'French', 'female', 1911)]

    # Insert a new row
    richard_feynman = {
        'category': 'Physics',
        'name': 'Richard Feynman',
        'nationality': 'US-American',
        'gender': 'male',
        'year': 1965,
    }
    session.execute(winners_table.insert().values(**richard_feynman))
    # ... INFO sqlalchemy.engine.Engine INSERT INTO winners (category, name, nationality, gender, year) VALUES (?, ?, ?, ?, ?)
    # ... INFO sqlalchemy.engine.Engine [generated in 0.00008s] ('Physics', 'Richard Feynman', 'US-American', 'male', 1965)
    session.commit()
    # 2023-10-10 21:16:13,102 INFO sqlalchemy.engine.Engine COMMIT
# ... INFO sqlalchemy.engine.Engine ROLLBACK

# Delete the table
Winner.__table__.drop(engine)
# ... INFO sqlalchemy.engine.Engine BEGIN (implicit)
# ... INFO sqlalchemy.engine.Engine
# DROP TABLE winners
# ... INFO sqlalchemy.engine.Engine [no key 0.00009s] ()
# ... INFO sqlalchemy.engine.Engine COMMIT
