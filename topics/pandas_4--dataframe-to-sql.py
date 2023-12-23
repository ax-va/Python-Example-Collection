"""
This example of data exploring with Pandas is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023.
"""
import pandas as pd
import sqlalchemy
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

df = pd.read_parquet('parquet-files/nobel_winners_cleaned.parquet')  # fastparquet is needed
df.info()
# <class 'pandas.core.frame.DataFrame'>
# Index: 974 entries, Richard Adolf Zsigmondy to John Carew Eccles
# Data columns (total 13 columns):
#  #   Column          Non-Null Count  Dtype
# ---  ------          --------------  -----
#  0   link            974 non-null    object
#  1   year            974 non-null    int64
#  2   category        974 non-null    object
#  3   country         974 non-null    object
#  4   text            974 non-null    object
#  5   wikidata_code   974 non-null    object
#  6   date_of_birth   974 non-null    datetime64[ns]
#  7   date_of_death   667 non-null    datetime64[ns]
#  8   place_of_birth  974 non-null    object
#  9   place_of_death  665 non-null    object
#  10  gender          974 non-null    object
#  11  born_in         136 non-null    object
#  12  award_age       974 non-null    int64
# dtypes: datetime64[ns](2), int64(2), object(9)
# memory usage: 106.5+ KB

df = df.reset_index()
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 974 entries, 0 to 973
# Data columns (total 14 columns):
#  #   Column          Non-Null Count  Dtype
# ---  ------          --------------  -----
#  0   name            974 non-null    object
#  1   link            974 non-null    object
#  2   year            974 non-null    int64
#  3   category        974 non-null    object
#  4   country         974 non-null    object
#  5   text            974 non-null    object
#  6   wikidata_code   974 non-null    object
#  7   date_of_birth   974 non-null    datetime64[ns]
#  8   date_of_death   667 non-null    datetime64[ns]
#  9   place_of_birth  974 non-null    object
#  10  place_of_death  665 non-null    object
#  11  gender          974 non-null    object
#  12  born_in         136 non-null    object
#  13  award_age       974 non-null    int64
# dtypes: datetime64[ns](2), int64(2), object(10)
# memory usage: 106.7+ KB

df['date_of_birth'] = df['date_of_birth'].astype(str)  # Avoid any problem with serializing datetime objects
df['date_of_death'] = df['date_of_death'].astype(str)

Base = declarative_base()


class Winner(Base):
    """
    Object-relational mapping (ORM):
    This class will correspond to the table, the instances
    of this class will correspond to the rows of the table,
    and the class attributes correspond to the columns of the table.
    """
    __tablename__ = 'winners_cleaned'
    index = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    year = Column(Integer)
    category = Column(String)
    country = Column(String)
    text = Column(Text)
    wikidata_code = Column(String)
    date_of_birth = Column(String)  # string form dates
    date_of_death = Column(String)  # string form dates
    place_of_birth = Column(String)
    place_of_death = Column(String)
    gender = Column(String)
    born_in = Column(String)
    award_age = Column(Integer)


# Create SQLite database and start a session
engine = sqlalchemy.create_engine('sqlite:///sqlite-databases/nobel_winners.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
with Session() as session:
    for record_as_dict in df.to_dict(orient='records'):
        session.add(Winner(**record_as_dict))
    session.commit()


"""
select count(*) from winners_cleaned;
974
"""
