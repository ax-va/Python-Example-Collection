"""
This example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023.
"""
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
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
# 2023-09-28 21:15:30,844 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-09-28 21:15:30,844 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("winners")
# 2023-09-28 21:15:30,844 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2023-09-28 21:15:30,844 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("winners")
# 2023-09-28 21:15:30,845 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2023-09-28 21:15:30,846 INFO sqlalchemy.engine.Engine
# CREATE TABLE winners (
#         id INTEGER NOT NULL,
#         category VARCHAR,
#         name VARCHAR,
#         nationality VARCHAR,
#         gender VARCHAR(6),
#         year INTEGER,
#         PRIMARY KEY (id)
# )
#
#
# 2023-09-28 21:15:30,846 INFO sqlalchemy.engine.Engine [no key 0.00019s] ()
# 2023-09-28 21:15:30,852 INFO sqlalchemy.engine.Engine COMMIT

# # # Add rows with a session

# Create a session to interact with the database.
# Use the context manager.
Session = sessionmaker(bind=engine)
with Session() as session:
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
    # 2023-09-28 21:19:34,861 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    # 2023-09-28 21:19:34,864 INFO sqlalchemy.engine.Engine INSERT INTO winners (category, name, nationality, gender, year) VALUES (?, ?, ?, ?, ?) RETURNING id
    # 2023-09-28 21:19:34,864 INFO sqlalchemy.engine.Engine [generated in 0.00025s (insertmanyvalues) 1/3 (ordered; batch not supported)] ('Physics', 'Albert Einstein', 'German and Swiss', 'male', 1921)
    # 2023-09-28 21:19:34,864 INFO sqlalchemy.engine.Engine INSERT INTO winners (category, name, nationality, gender, year) VALUES (?, ?, ?, ?, ?) RETURNING id
    # 2023-09-28 21:19:34,864 INFO sqlalchemy.engine.Engine [insertmanyvalues 2/3 (ordered; batch not supported)] ('Physics', 'Paul Dirac', 'British', 'male', 1933)
    # 2023-09-28 21:19:34,865 INFO sqlalchemy.engine.Engine INSERT INTO winners (category, name, nationality, gender, year) VALUES (?, ?, ?, ?, ?) RETURNING id
    # 2023-09-28 21:19:34,865 INFO sqlalchemy.engine.Engine [insertmanyvalues 3/3 (ordered; batch not supported)] ('Chemistry', 'Marie Curie', 'Polish', 'female', 1911)
    # 2023-09-28 21:19:34,866 INFO sqlalchemy.engine.Engine COMMIT

    # # # Query the database

    cnt = session.query(Winner).count()
    # 2023-09-28 21:19:57,612 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    # 2023-09-28 21:19:57,618 INFO sqlalchemy.engine.Engine SELECT count(*) AS count_1
    # FROM (SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners) AS anon_1
    # 2023-09-28 21:19:57,619 INFO sqlalchemy.engine.Engine [generated in 0.00032s] ()
    print(cnt)
    # 3

    # Filter by
    result = session.query(Winner).filter_by(nationality='German and Swiss')
    print("type of result:", type(result))
    # type of result: <class 'sqlalchemy.orm.query.Query'>
    print(list(result))
    # 2023-09-28 21:21:32,454 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # WHERE winners.nationality = ?
    # 2023-09-28 21:21:32,454 INFO sqlalchemy.engine.Engine [cached since 34.76s ago] ('German and Swiss',)
    # [<Winner(name='Albert Einstein', category='Physics', year=1921)>]

    # Filter
    result = session.query(Winner).filter(Winner.category == 'Physics', Winner.nationality != 'German and Swiss')
    print(list(result))
    # 2023-09-28 21:24:38,018 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # WHERE winners.category = ? AND winners.nationality != ?
    # 2023-09-28 21:24:38,018 INFO sqlalchemy.engine.Engine [generated in 0.00026s] ('Physics', 'German and Swiss')
    # [<Winner(name='Paul Dirac', category='Physics', year=1933)>]

    """
    # In SQLAlchemy 1.x, get a row based on ID number.
    # Deprecated since SQLAlchemy 2.0.0
    row = session.query(Winner).get(3)
    print("type of row:", type(row))
    """

    # Since SQLAlchemy 2.0, get a row by ID
    row = session.get(Winner, 3)
    # 2023-09-28 21:25:57,728 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # WHERE winners.id = ?
    # 2023-09-28 21:25:57,728 INFO sqlalchemy.engine.Engine [generated in 0.00033s] (3,)
    print("type of row:", type(row))
    # type of row: <class '__main__.Winner'>
    print(row)
    # <Winner(name='Marie Curie', category='Chemistry', year=1911)>

    # Retrieve winners ordered by year
    result = session.query(Winner).order_by('year')
    print(list(result))
    # 2023-09-28 21:26:59,810 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners ORDER BY winners.year
    # 2023-09-28 21:26:59,811 INFO sqlalchemy.engine.Engine [generated in 0.00028s] ()
    # [<Winner(name='Marie Curie', category='Chemistry', year=1911)>, <Winner(name='Albert Einstein', category='Physics', year=1921)>, <Winner(name='Paul Dirac', category='Physics', year=1933)>]

    # Reconstruct the list of dictionaries
    winner_rows = session.query(Winner)
    nobel_winners = [inst_to_dict(w) for w in winner_rows]
    # 2023-09-28 21:28:21,011 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # 2023-09-28 21:28:21,011 INFO sqlalchemy.engine.Engine [generated in 0.00027s] ()
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
    # 2023-09-28 21:30:40,777 INFO sqlalchemy.engine.Engine UPDATE winners SET nationality=? WHERE winners.id = ?
    # 2023-09-28 21:30:40,777 INFO sqlalchemy.engine.Engine [generated in 0.00034s] ('French', 3)
    # 2023-09-28 21:30:40,778 INFO sqlalchemy.engine.Engine COMMIT

    print(session.dirty)
    # IdentitySet([])

    nationality = session.get(Winner, 3).nationality
    # 2023-09-28 21:31:11,990 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    # 2023-09-28 21:31:11,990 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # WHERE winners.id = ?
    # 2023-09-28 21:31:11,990 INFO sqlalchemy.engine.Engine [cached since 314.3s ago] (3,)
    print(nationality)
    # French

    # Delete a row from the database
    cnt = session.query(Winner).filter_by(name='Albert Einstein').delete()
    # 2023-09-28 21:31:52,898 INFO sqlalchemy.engine.Engine DELETE FROM winners WHERE winners.name = ?
    # 2023-09-28 21:31:52,898 INFO sqlalchemy.engine.Engine [generated in 0.00029s] ('Albert Einstein',)

    # The row will not be deleted without commit()

    print(cnt)
    # 1
    print(session.new)
    # IdentitySet([])

    data = list(session.query(Winner))
    # 2023-09-28 21:33:16,625 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # 2023-09-28 21:33:16,626 INFO sqlalchemy.engine.Engine [cached since 295.6s ago] ()
    print(data)
    # [<Winner(name='Paul Dirac', category='Physics', year=1933)>, <Winner(name='Marie Curie', category='Chemistry', year=1911)>]

# 2023-09-28 21:34:18,173 INFO sqlalchemy.engine.Engine ROLLBACK

# # # Use metadata to access the database
with Session() as session:
    metadata = MetaData()
    metadata.reflect(engine)
    # 2023-09-28 21:38:10,528 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    # 2023-09-28 21:38:10,528 INFO sqlalchemy.engine.Engine SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite~_%' ESCAPE '~' ORDER BY name
    # 2023-09-28 21:38:10,528 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,529 INFO sqlalchemy.engine.Engine SELECT name FROM sqlite_temp_master WHERE type='table' AND name NOT LIKE 'sqlite~_%' ESCAPE '~' ORDER BY name
    # 2023-09-28 21:38:10,529 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,529 INFO sqlalchemy.engine.Engine PRAGMA main.table_xinfo("winners")
    # 2023-09-28 21:38:10,529 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,530 INFO sqlalchemy.engine.Engine SELECT sql FROM  (SELECT * FROM sqlite_master UNION ALL   SELECT * FROM sqlite_temp_master) WHERE name = ? AND type in ('table', 'view')
    # 2023-09-28 21:38:10,530 INFO sqlalchemy.engine.Engine [raw sql] ('winners',)
    # 2023-09-28 21:38:10,530 INFO sqlalchemy.engine.Engine PRAGMA main.foreign_key_list("winners")
    # 2023-09-28 21:38:10,530 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,530 INFO sqlalchemy.engine.Engine PRAGMA temp.foreign_key_list("winners")
    # 2023-09-28 21:38:10,530 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,530 INFO sqlalchemy.engine.Engine SELECT sql FROM  (SELECT * FROM sqlite_master UNION ALL   SELECT * FROM sqlite_temp_master) WHERE name = ? AND type in ('table', 'view')
    # 2023-09-28 21:38:10,531 INFO sqlalchemy.engine.Engine [raw sql] ('winners',)
    # 2023-09-28 21:38:10,531 INFO sqlalchemy.engine.Engine PRAGMA main.index_list("winners")
    # 2023-09-28 21:38:10,531 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,531 INFO sqlalchemy.engine.Engine PRAGMA temp.index_list("winners")
    # 2023-09-28 21:38:10,531 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,531 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("winners")
    # 2023-09-28 21:38:10,532 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,532 INFO sqlalchemy.engine.Engine PRAGMA main.index_list("winners")
    # 2023-09-28 21:38:10,532 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,532 INFO sqlalchemy.engine.Engine PRAGMA temp.index_list("winners")
    # 2023-09-28 21:38:10,532 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,532 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("winners")
    # 2023-09-28 21:38:10,532 INFO sqlalchemy.engine.Engine [raw sql] ()
    # 2023-09-28 21:38:10,533 INFO sqlalchemy.engine.Engine SELECT sql FROM  (SELECT * FROM sqlite_master UNION ALL   SELECT * FROM sqlite_temp_master) WHERE name = ? AND type in ('table', 'view')
    # 2023-09-28 21:38:10,533 INFO sqlalchemy.engine.Engine [raw sql] ('winners',)
    # 2023-09-28 21:38:10,533 INFO sqlalchemy.engine.Engine ROLLBACK
    winners_table = Table("winners", metadata)
    result = session.query(winners_table).filter(winners_table.c.year.in_(range(1911, 1922)))
    print(list(result))
    # 2023-09-28 21:39:01,298 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    # 2023-09-28 21:39:01,300 INFO sqlalchemy.engine.Engine SELECT winners.id AS winners_id, winners.category AS winners_category, winners.name AS winners_name, winners.nationality AS winners_nationality, winners.gender AS winners_gender, winners.year AS winners_year
    # FROM winners
    # WHERE winners.year IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    # 2023-09-28 21:39:01,300 INFO sqlalchemy.engine.Engine [generated in 0.00050s] (1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921)
    # [(1, 'Physics', 'Albert Einstein', 'German and Swiss', 'male', 1921), (3, 'Chemistry', 'Marie Curie', 'French', 'female', 1911)]


# Delete the table
Winner.__table__.drop(engine)
# 2023-09-28 21:39:28,202 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-09-28 21:39:28,203 INFO sqlalchemy.engine.Engine
# DROP TABLE winners
# 2023-09-28 21:39:28,203 INFO sqlalchemy.engine.Engine [no key 0.00013s] ()
# 2023-09-28 21:39:28,210 INFO sqlalchemy.engine.Engine COMMIT
