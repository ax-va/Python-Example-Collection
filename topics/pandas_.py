"""
...
https://pandas.pydata.org/pandas-docs/dev/user_guide/io.html
https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#reading-json
https://jsonlint.com/
https://pandas.pydata.org/pandas-docs/dev/user_guide/io.html#json
https://pandas.pydata.org/pandas-docs/dev/user_guide/io.html#csv-text-files
https://pandas.pydata.org/pandas-docs/dev/user_guide/io.html#reading-excel-files
https://pandas.pydata.org/pandas-docs/dev/user_guide/io.html#sql-queries
"""
import pandas as pd

print(pd.__version__)
# 2.1.2

df = pd.read_json('scrapy-projects/nobel_winners/Nobel_winners_by_request_chains.json')
df.head()
#                                                 link                     name  year                category  country  ...     date_of_birth      date_of_death place_of_birth              place_of_death  gender
# 0  https://en.wikipedia.org/wiki/Richard_Adolf_Zs...  Richard Adolf Zsigmondy  1925               Chemistry  Austria  ...      1 April 1865  23 September 1929         Vienna                   Göttingen    male
# 1          https://en.wikipedia.org/wiki/Fritz_Pregl              Fritz Pregl  1923               Chemistry  Austria  ...  3 September 1869   13 December 1930      Ljubljana                        Graz    male
# 2  https://en.wikipedia.org/wiki/R%C3%B3bert_B%C3...            Róbert Bárány  1914  Physiology or Medicine  Austria  ...     22 April 1876       8 April 1936         Vienna  Uppsala Cathedral Assembly    male
# 3  https://en.wikipedia.org/wiki/Carl_Ferdinand_Cori      Carl Ferdinand Cori  1947  Physiology or Medicine  Austria  ...   5 December 1896    20 October 1984         Prague                   Cambridge    male
# 4           https://en.wikipedia.org/wiki/Gerty_Cori               Gerty Cori  1947  Physiology or Medicine  Austria  ...    15 August 1896    26 October 1957         Prague                    Glendale  female
#
# [5 rows x 13 columns]


df.columns
# Index(['link', 'name', 'year', 'category', 'country', 'born_in', 'text',
#        'wikidata_code', 'date_of_birth', 'date_of_death', 'place_of_birth',
#        'place_of_death', 'gender'],
#       dtype='object')

df.index
# RangeIndex(start=0, stop=1206, step=1)

df = df.set_index('name')
df.head()
#                                                                       link  year                category  country born_in  ...     date_of_birth      date_of_death place_of_birth              place_of_death  gender
# name                                                                                                                       ...
# Richard Adolf Zsigmondy  https://en.wikipedia.org/wiki/Richard_Adolf_Zs...  1925               Chemistry  Austria    None  ...      1 April 1865  23 September 1929         Vienna                   Göttingen    male
# Fritz Pregl                      https://en.wikipedia.org/wiki/Fritz_Pregl  1923               Chemistry  Austria    None  ...  3 September 1869   13 December 1930      Ljubljana                        Graz    male
# Róbert Bárány            https://en.wikipedia.org/wiki/R%C3%B3bert_B%C3...  1914  Physiology or Medicine  Austria    None  ...     22 April 1876       8 April 1936         Vienna  Uppsala Cathedral Assembly    male
# Carl Ferdinand Cori      https://en.wikipedia.org/wiki/Carl_Ferdinand_Cori  1947  Physiology or Medicine  Austria    None  ...   5 December 1896    20 October 1984         Prague                   Cambridge    male
# Gerty Cori                        https://en.wikipedia.org/wiki/Gerty_Cori  1947  Physiology or Medicine  Austria    None  ...    15 August 1896    26 October 1957         Prague                    Glendale  female
#
# [5 rows x 12 columns]

df.loc['Albert Einstein']
#                                                           link  year category      country born_in  ...  date_of_birth  date_of_death place_of_birth place_of_death gender
# name                                                                                                ...
# Albert Einstein  https://en.wikipedia.org/wiki/Albert_Einstein  1921  Physics  Switzerland    None  ...  14 March 1879  18 April 1955            Ulm      Princeton   male
# Albert Einstein  https://en.wikipedia.org/wiki/Albert_Einstein  1921  Physics      Germany    None  ...  14 March 1879  18 April 1955            Ulm      Princeton   male
#
# [2 rows x 12 columns]

df = df.reset_index()
df.head()
#                       name                                               link  year                category  country  ...     date_of_birth      date_of_death place_of_birth              place_of_death  gender
# 0  Richard Adolf Zsigmondy  https://en.wikipedia.org/wiki/Richard_Adolf_Zs...  1925               Chemistry  Austria  ...      1 April 1865  23 September 1929         Vienna                   Göttingen    male
# 1              Fritz Pregl          https://en.wikipedia.org/wiki/Fritz_Pregl  1923               Chemistry  Austria  ...  3 September 1869   13 December 1930      Ljubljana                        Graz    male
# 2            Róbert Bárány  https://en.wikipedia.org/wiki/R%C3%B3bert_B%C3...  1914  Physiology or Medicine  Austria  ...     22 April 1876       8 April 1936         Vienna  Uppsala Cathedral Assembly    male
# 3      Carl Ferdinand Cori  https://en.wikipedia.org/wiki/Carl_Ferdinand_Cori  1947  Physiology or Medicine  Austria  ...   5 December 1896    20 October 1984         Prague                   Cambridge    male
# 4               Gerty Cori           https://en.wikipedia.org/wiki/Gerty_Cori  1947  Physiology or Medicine  Austria  ...    15 August 1896    26 October 1957         Prague                    Glendale  female
#
# [5 rows x 13 columns]

df.iloc[2]
# link              https://en.wikipedia.org/wiki/R%C3%B3bert_B%C3...
# name                                                  Róbert Bárány
# year                                                           1914
# category                                     Physiology or Medicine
# country                                                     Austria
# born_in                                                        None
# text                   Róbert Bárány , Physiology or Medicine, 1914
# wikidata_code                                                Q78478
# date_of_birth                                         22 April 1876
# date_of_death                                          8 April 1936
# place_of_birth                                               Vienna
# place_of_death                           Uppsala Cathedral Assembly
# gender                                                         male
# Name: 2, dtype: object

# # # selecting groups

category_groups = df.groupby('category')
# <pandas.core.groupby.generic.DataFrameGroupBy object at 0x7f5a30558910>

category_groups.groups.keys()
# dict_keys(['Chemistry', 'Economics', 'Literature', 'Peace', 'Physics', 'Physiology or Medicine'])

physics_group = category_groups.get_group('Physics')
physics_group.head()
#                                             link            name  year category         country born_in  ... wikidata_code      date_of_birth     date_of_death       place_of_birth place_of_death gender
# 5   https://en.wikipedia.org/wiki/Wolfgang_Pauli  Wolfgang Pauli  1945  Physics         Austria    None  ...        Q65989      25 April 1900  15 December 1958               Vienna         Zürich   male
# 8      https://en.wikipedia.org/wiki/Peter_Higgs     Peter Higgs  2013  Physics  United Kingdom    None  ...       Q192112        29 May 1929               NaN  Newcastle upon Tyne            NaN   male
# 11  https://en.wikipedia.org/wiki/Syukuro_Manabe  Syukuro Manabe  2021  Physics   United States    None  ...      Q3675789  21 September 1931               NaN            Shinritsu            NaN   male
# 16    https://en.wikipedia.org/wiki/John_L._Hall    John L. Hall  2005  Physics   United States    None  ...       Q206390     21 August 1934               NaN               Denver            NaN   male
# 17  https://en.wikipedia.org/wiki/Roy_J._Glauber  Roy J. Glauber  2005  Physics   United States    None  ...        Q64188   1 September 1925  26 December 2018        New York City         Newton   male

df.category == 'Physics'
# 0       False
# 1       False
# 2       False
# 3       False
# 4       False
#         ...
# 1201    False
# 1202    False
# 1203    False
# 1204    False
# 1205    False
# Name: category, Length: 1206, dtype: bool

df[df.category == 'Physics'].head()
#                                             link            name  year category         country born_in  ... wikidata_code      date_of_birth     date_of_death       place_of_birth place_of_death gender
# 5   https://en.wikipedia.org/wiki/Wolfgang_Pauli  Wolfgang Pauli  1945  Physics         Austria    None  ...        Q65989      25 April 1900  15 December 1958               Vienna         Zürich   male
# 8      https://en.wikipedia.org/wiki/Peter_Higgs     Peter Higgs  2013  Physics  United Kingdom    None  ...       Q192112        29 May 1929               NaN  Newcastle upon Tyne            NaN   male
# 11  https://en.wikipedia.org/wiki/Syukuro_Manabe  Syukuro Manabe  2021  Physics   United States    None  ...      Q3675789  21 September 1931               NaN            Shinritsu            NaN   male
# 16    https://en.wikipedia.org/wiki/John_L._Hall    John L. Hall  2005  Physics   United States    None  ...       Q206390     21 August 1934               NaN               Denver            NaN   male
# 17  https://en.wikipedia.org/wiki/Roy_J._Glauber  Roy J. Glauber  2005  Physics   United States    None  ...        Q64188   1 September 1925  26 December 2018        New York City         Newton   male
#
# [5 rows x 13 columns]

# # # creating and saving DataFrames

# from a dict[column_name, list] specifying the columns separately
df = pd.DataFrame(
    {
        'name': ['Albert Einstein', 'Marie Curie', 'William Faulkner'],
        'category': ['Physics', 'Chemistry', 'Literature']
    }
)
#                name    category
# 0   Albert Einstein     Physics
# 1       Marie Curie   Chemistry
# 2  William Faulkner  Literature

# from a list of dictionaries
df = pd.DataFrame.from_dict(
    [
        {'name': 'Albert Einstein', 'category':'Physics'},
        {'name': 'Marie Curie', 'category':'Chemistry'},
        {'name': 'William Faulkner', 'category':'Literature'},
    ]
)
#                name    category
# 0   Albert Einstein     Physics
# 1       Marie Curie   Chemistry
# 2  William Faulkner  Literature

# # # JSON
# Store the JSON as dataviz-friendly records
df.to_json('json-files/nobel_winners_from_dataframe.json', orient='records')

# # # CSV
from io import StringIO
data = " `Albert Einstein`| Physics \n  `Marie Curie`|   Chemistry  "
df = pd.read_csv(
    StringIO(data),
    sep='|',  # pipe-separated
    names=['name', 'category'],
    skipinitialspace=True,
    quotechar="`"
)
#               name         category
# 0  Albert Einstein         Physics
# 1      Marie Curie  Chemistry

df.iloc[0]["name"]
# 'Albert Einstein'

df.iloc[1]["name"]
# 'Marie Curie'

df.iloc[0]["category"]
# 'Physics '

df.iloc[1]["category"]
# 'Chemistry  '

df.to_csv('csv-files/novel_winners_from_dataframe.csv', encoding='utf-8')

# # # Excel-like files
# Pandas uses xlrd to read Excel 2003 (.xls) and openpyxl to read Excel 2007+ (.xlsx) files.

# method 1 to read XLSX: creating and then parsing an ExcelFile object
dfs = {}
xls = pd.ExcelFile('excel-like-files/nobel_winners.xlsx')  # Load Excel file
dfs['Physics'] = xls.parse(
    sheet_name='Physics',
    na_values=['NA'],
)
dfs['Chemistry'] = xls.parse(
    sheet_name='Chemistry',
    index_col=0,
    na_values=['-'],  # Recognize as NaN
    # skiprows=3,  # Skip before processing
)
dfs["Physics"]
#               name       nationality gender  year
# 0  Albert Einstein  German and Swiss   male  1921
# 1       Paul Dirac          Britisch   male  1933
dfs["Chemistry"]
#             nationality  gender  year
# name
# Marie Curie      Polish  female  1911

# method 2 to read XLSX: a convenience method read_excel
# Reading the Excel file is with the same arguments.
# The 'sheet_name' argument can be a single name string or index (beginning at 0) or a mixed list.
# sheet_name t= None returns a sheet_name-keyed dictionary of DataFrames.
dfs = pd.read_excel(
    io='excel-like-files/nobel_winners.xlsx',
    sheet_name=['Physics', 'Chemistry'],  # Specify sheets by index or name. Default: sheet_name = 0.
    index_col=None,
    na_values=['NA'],
    # usecols=[0],
)
dfs["Physics"]
#               name       nationality gender  year
# 0  Albert Einstein  German and Swiss   male  1921
# 1       Paul Dirac          Britisch   male  1933
dfs["Chemistry"]
#           name nationality  gender  year
# 0  Marie Curie      Polish  female  1911

# one sheet
dfs["Physics"].to_excel('excel-like-files/nobel_winners_from_dataframe.xlsx', sheet_name='Physics')

# multiple sheets
with pd.ExcelWriter('excel-like-files/nobel_winners_from_dataframe.xlsx') as writer:
    dfs["Physics"].to_excel(writer, sheet_name='Physics')
    dfs["Chemistry"].to_excel(writer, sheet_name='Chemistry')

# # # SQL
import sqlalchemy

print(sqlalchemy.__version__)
# 2.0.21

sql_engine = sqlalchemy.create_engine('sqlite:///sqlite-databases/nobel_winners_for_pandas.db')
# read_sql is a wrapper of read_sql_table and read_sql_query
df = pd.read_sql('nobel_winners', sql_engine)
#    id   category             name       nationality  gender  year
# 0   1    Physics  Albert Einstein  German and Swiss    male  1921
# 1   2    Physics       Paul Dirac           British    male  1933
# 2   3  Chemistry      Marie Curie            Polish  female  1911

df_physics = pd.read_sql("select * from nobel_winners where category='Physics'", sql_engine)
#    id category             name       nationality gender  year
# 0   1  Physics  Albert Einstein  German and Swiss   male  1921
# 1   2  Physics       Paul Dirac           British   male  1933

df_physics[["name", "nationality", "gender", "year"]].to_sql(
    'nobel_winners_in_physics',
    sql_engine,
    if_exists='replace',
    chunksize=500
)

from sqlalchemy.types import String

df_chemistry = pd.read_sql("select * from nobel_winners where category='Chemistry'", sql_engine)
#    id   category         name nationality  gender  year
# 0   3  Chemistry  Marie Curie      Polish  female  1911

df_chemistry[["name", "nationality", "gender", "year"]].to_sql(
    'nobel_winners_in_chemistry',
    sql_engine,
    dtype={'year': String}
)

# # # MongoDB
from pymongo import MongoClient

# Create a Mongo client, using the default host and ports
client = MongoClient()  # default: host='localhost', port=27017
# MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)

# MongoDB version
print(client.server_info()["version"])
# 7.0.2

# Get the nobel_prize database
db = client.nobel_prize_for_pandas
# Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'nobel_prize')

# Find all documents in the winner collection
cursor = db.winners.find()
df = pd.DataFrame(list(cursor))
#                         _id   category             name       nationality  gender  year
# 0  654d41f3b726ff4e0d962389    Physics  Albert Einstein  German and Swiss    male  1921
# 1  654d41f3b726ff4e0d96238a    Physics       Paul Dirac           British    male  1933
# 2  654d41f3b726ff4e0d96238b  Chemistry      Marie Curie            Polish  female  1911

# Ignore the first row
records = df[1:].to_dict('records')
# [{'_id': ObjectId('654d41f3b726ff4e0d96238a'),
#   'category': 'Physics',
#   'name': 'Paul Dirac',
#   'nationality': 'British',
#   'gender': 'male',
#   'year': 1933},
#  {'_id': ObjectId('654d41f3b726ff4e0d96238b'),
#   'category': 'Chemistry',
#   'name': 'Marie Curie',
#   'nationality': 'Polish',
#   'gender': 'female',
#   'year': 1911}]

# Ignore the _id column
records = df.loc[:, df.columns != "_id"].to_dict('records')
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

db["winners"].insert_many(
    [
        {
            'category': 'Literature',
            'name': 'Albert Camus',
            'nationality': 'French',
            'gender': 'male',
            'year': 1957
        },
        {
            'category': 'Physics',
            'name': 'Richard P. Feynman',
            'nationality': 'US-American',
            'gender': 'male',
            'year': 1965
        },
    ]
)
# <pymongo.results.InsertManyResult at 0x7fab1bfd3430>

list(db["winners"].find())
# [{'_id': ObjectId('654d41f3b726ff4e0d962389'),
#   'category': 'Physics',
#   'name': 'Albert Einstein',
#   'nationality': 'German and Swiss',
#   'gender': 'male',
#   'year': 1921},
#  {'_id': ObjectId('654d41f3b726ff4e0d96238a'),
#   'category': 'Physics',
#   'name': 'Paul Dirac',
#   'nationality': 'British',
#   'gender': 'male',
#   'year': 1933},
#  {'_id': ObjectId('654d41f3b726ff4e0d96238b'),
#   'category': 'Chemistry',
#   'name': 'Marie Curie',
#   'nationality': 'Polish',
#   'gender': 'female',
#   'year': 1911},
#  {'_id': ObjectId('654d4697725019559e886f8f'),
#   'category': 'Literature',
#   'name': 'Albert Camus',
#   'nationality': 'French',
#   'gender': 'male',
#   'year': 1957},
#  {'_id': ObjectId('654d4697725019559e886f90'),
#   'category': 'Physics',
#   'name': 'Richard P. Feynman',
#   'nationality': 'US-American',
#   'gender': 'male',
#   'year': 1965}]

db["winners"].delete_many({'year': {'$gt': 1950}})

list(db["winners"].find())
# [{'_id': ObjectId('654d41f3b726ff4e0d962389'),
#   'category': 'Physics',
#   'name': 'Albert Einstein',
#   'nationality': 'German and Swiss',
#   'gender': 'male',
#   'year': 1921},
#  {'_id': ObjectId('654d41f3b726ff4e0d96238a'),
#   'category': 'Physics',
#   'name': 'Paul Dirac',
#   'nationality': 'British',
#   'gender': 'male',
#   'year': 1933},
#  {'_id': ObjectId('654d41f3b726ff4e0d96238b'),
#   'category': 'Chemistry',
#   'name': 'Marie Curie',
#   'nationality': 'Polish',
#   'gender': 'female',
#   'year': 1911}]
