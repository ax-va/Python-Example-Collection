"""
https://pandas.pydata.org/pandas-docs/stable/user_guide/text.html#string-methods
"""
import numpy as np
import pandas as pd

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

# # # inspecting the data

df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 1206 entries, 0 to 1205
# Data columns (total 13 columns):
#  #   Column          Non-Null Count  Dtype
# ---  ------          --------------  -----
#  0   link            1206 non-null   object
#  1   name            1206 non-null   object
#  2   year            1206 non-null   int64
#  3   category        1202 non-null   object
#  4   country         1052 non-null   object
#  5   born_in         154 non-null    object
#  6   text            1206 non-null   object
#  7   wikidata_code   1206 non-null   object
#  8   date_of_birth   1206 non-null   object
#  9   date_of_death   817 non-null    object
#  10  place_of_birth  1206 non-null   object
#  11  place_of_death  815 non-null    object
#  12  gender          1206 non-null   object
# dtypes: int64(1), object(12)
# memory usage: 122.6+ KB

# By default, only numerical columns are described.
df.describe()
#               year
# count  1206.000000
# mean   1974.660033
# std      35.150212
# min    1809.000000
# 25%    1952.000000
# 50%    1980.000000
# 75%    2004.000000
# max    2023.000000

pd.set_option('display.max_columns', None)

df.describe(include=['object'])
#                                              link            name category  \
# count                                        1206            1206     1202
# unique                                        981             980        6
# top     https://en.wikipedia.org/wiki/Marie_Curie  Charles K. Kao  Physics
# freq                                            4               4      285
#
#               country  born_in  \
# count            1052      154
# unique             64       49
# top     United States  Germany
# freq              408       28
#
#                                                      text wikidata_code  \
# count                                                1206          1206
# unique                                               1185           965
# top     Michael Levitt ,  born in South Africa , Chemi...      Q6832227
# freq                                                    3             4
#
#        date_of_birth    date_of_death place_of_birth place_of_death gender
# count           1206              817           1206            815   1206
# unique           952              655            679            353      2
# top       9 May 1947  20 October 1984  New York City      Cambridge   male
# freq               4                4             40             46   1122


df.head()
#                                                 link                     name  \
# 0  https://en.wikipedia.org/wiki/Richard_Adolf_Zs...  Richard Adolf Zsigmondy
# 1          https://en.wikipedia.org/wiki/Fritz_Pregl              Fritz Pregl
# 2  https://en.wikipedia.org/wiki/R%C3%B3bert_B%C3...            Róbert Bárány
# 3  https://en.wikipedia.org/wiki/Carl_Ferdinand_Cori      Carl Ferdinand Cori
# 4           https://en.wikipedia.org/wiki/Gerty_Cori               Gerty Cori
#
#    year                category  country born_in  \
# 0  1925               Chemistry  Austria    None
# 1  1923               Chemistry  Austria    None
# 2  1914  Physiology or Medicine  Austria    None
# 3  1947  Physiology or Medicine  Austria    None
# 4  1947  Physiology or Medicine  Austria    None
#
#                                                 text wikidata_code  \
# 0          Richard Adolf Zsigmondy , Chemistry, 1925        Q78481
# 1  Fritz Pregl ,  born in Austria-Hungary, now Sl...        Q78482
# 2       Róbert Bárány , Physiology or Medicine, 1914        Q78478
# 3  Carl Ferdinand Cori ,  born in Austria , Physi...        Q78501
# 4  Gerty Cori ,  born in Austria , Physiology or ...       Q204733
#
#       date_of_birth      date_of_death place_of_birth  \
# 0      1 April 1865  23 September 1929         Vienna
# 1  3 September 1869   13 December 1930      Ljubljana
# 2     22 April 1876       8 April 1936         Vienna
# 3   5 December 1896    20 October 1984         Prague
# 4    15 August 1896    26 October 1957         Prague
#
#                place_of_death  gender
# 0                   Göttingen    male
# 1                        Graz    male
# 2  Uppsala Cathedral Assembly    male
# 3                   Cambridge    male
# 4                    Glendale  female

df.tail()
#                                                    link  \
# 1201  https://en.wikipedia.org/wiki/Adolfo_P%C3%A9re...
# 1202  https://en.wikipedia.org/wiki/Luis_Federico_Le...
# 1203     https://en.wikipedia.org/wiki/Bernardo_Houssay
# 1204  https://en.wikipedia.org/wiki/Carlos_Saavedra_...
# 1205  https://en.wikipedia.org/wiki/John_Eccles_(neu...
#
#                        name  year                category    country born_in  \
# 1201  Adolfo Pérez Esquivel  1980                   Peace  Argentina    None
# 1202   Luis Federico Leloir  1970               Chemistry  Argentina    None
# 1203       Bernardo Houssay  1947  Physiology or Medicine  Argentina    None
# 1204  Carlos Saavedra Lamas  1936                   Peace  Argentina    None
# 1205      John Carew Eccles  1963  Physiology or Medicine  Australia    None
#
#                                                    text wikidata_code  \
# 1201                Adolfo Pérez Esquivel , Peace, 1980       Q206505
# 1202  Luis Federico Leloir ,  born in France , Chemi...       Q233985
# 1203    Bernardo Houssay , Physiology or Medicine, 1947       Q237160
# 1204                Carlos Saavedra Lamas , Peace, 1936       Q193672
# 1205   John Carew Eccles , Physiology or Medicine, 1963       Q273223
#
#          date_of_birth      date_of_death place_of_birth place_of_death gender
# 1201  26 November 1931                NaN   Buenos Aires            NaN   male
# 1202  6 September 1906    2 December 1987          Paris      Catamarca   male
# 1203     10 April 1887  21 September 1971   Buenos Aires   Buenos Aires   male
# 1204   1 November 1878         5 May 1959   Buenos Aires   Buenos Aires   male
# 1205   27 January 1903         2 May 1997      Melbourne  Tenero-Contra   male

df = df.set_index("name")
#                                                                       link  \
# name
# Richard Adolf Zsigmondy  https://en.wikipedia.org/wiki/Richard_Adolf_Zs...
# Fritz Pregl                      https://en.wikipedia.org/wiki/Fritz_Pregl
# Róbert Bárány            https://en.wikipedia.org/wiki/R%C3%B3bert_B%C3...
# Carl Ferdinand Cori      https://en.wikipedia.org/wiki/Carl_Ferdinand_Cori
# Gerty Cori                        https://en.wikipedia.org/wiki/Gerty_Cori
#
#                          year                category  country born_in  \
# name
# Richard Adolf Zsigmondy  1925               Chemistry  Austria    None
# Fritz Pregl              1923               Chemistry  Austria    None
# Róbert Bárány            1914  Physiology or Medicine  Austria    None
# Carl Ferdinand Cori      1947  Physiology or Medicine  Austria    None
# Gerty Cori               1947  Physiology or Medicine  Austria    None
#
#                                                                       text  \
# name
# Richard Adolf Zsigmondy          Richard Adolf Zsigmondy , Chemistry, 1925
# Fritz Pregl              Fritz Pregl ,  born in Austria-Hungary, now Sl...
# Róbert Bárány                 Róbert Bárány , Physiology or Medicine, 1914
# Carl Ferdinand Cori      Carl Ferdinand Cori ,  born in Austria , Physi...
# Gerty Cori               Gerty Cori ,  born in Austria , Physiology or ...
#
#                         wikidata_code     date_of_birth      date_of_death  \
# name
# Richard Adolf Zsigmondy        Q78481      1 April 1865  23 September 1929
# Fritz Pregl                    Q78482  3 September 1869   13 December 1930
# Róbert Bárány                  Q78478     22 April 1876       8 April 1936
# Carl Ferdinand Cori            Q78501   5 December 1896    20 October 1984
# Gerty Cori                    Q204733    15 August 1896    26 October 1957
#
#                         place_of_birth              place_of_death  gender
# name
# Richard Adolf Zsigmondy         Vienna                   Göttingen    male
# Fritz Pregl                  Ljubljana                        Graz    male
# Róbert Bárány                   Vienna  Uppsala Cathedral Assembly    male
# Carl Ferdinand Cori             Prague                   Cambridge    male
# Gerty Cori                      Prague                    Glendale  female

# There is no guarantee that in place is faster
df.reset_index(inplace=True)
#                       name                                               link  \
# 0  Richard Adolf Zsigmondy  https://en.wikipedia.org/wiki/Richard_Adolf_Zs...
# 1              Fritz Pregl          https://en.wikipedia.org/wiki/Fritz_Pregl
# 2            Róbert Bárány  https://en.wikipedia.org/wiki/R%C3%B3bert_B%C3...
# 3      Carl Ferdinand Cori  https://en.wikipedia.org/wiki/Carl_Ferdinand_Cori
# 4               Gerty Cori           https://en.wikipedia.org/wiki/Gerty_Cori
#
#    year                category  country born_in  \
# 0  1925               Chemistry  Austria    None
# 1  1923               Chemistry  Austria    None
# 2  1914  Physiology or Medicine  Austria    None
# 3  1947  Physiology or Medicine  Austria    None
# 4  1947  Physiology or Medicine  Austria    None
#
#                                                 text wikidata_code  \
# 0          Richard Adolf Zsigmondy , Chemistry, 1925        Q78481
# 1  Fritz Pregl ,  born in Austria-Hungary, now Sl...        Q78482
# 2       Róbert Bárány , Physiology or Medicine, 1914        Q78478
# 3  Carl Ferdinand Cori ,  born in Austria , Physi...        Q78501
# 4  Gerty Cori ,  born in Austria , Physiology or ...       Q204733
#
#       date_of_birth      date_of_death place_of_birth  \
# 0      1 April 1865  23 September 1929         Vienna
# 1  3 September 1869   13 December 1930      Ljubljana
# 2     22 April 1876       8 April 1936         Vienna
# 3   5 December 1896    20 October 1984         Prague
# 4    15 August 1896    26 October 1957         Prague
#
#                place_of_death  gender
# 0                   Göttingen    male
# 1                        Graz    male
# 2  Uppsala Cathedral Assembly    male
# 3                   Cambridge    male
# 4                    Glendale  female

df.iloc[0]
# name                                        Richard Adolf Zsigmondy
# link              https://en.wikipedia.org/wiki/Richard_Adolf_Zs...
# year                                                           1925
# category                                                  Chemistry
# country                                                     Austria
# born_in                                                        None
# text                      Richard Adolf Zsigmondy , Chemistry, 1925
# wikidata_code                                                Q78481
# date_of_birth                                          1 April 1865
# date_of_death                                     23 September 1929
# place_of_birth                                               Vienna
# place_of_death                                            Göttingen
# gender                                                         male

mask = df.year > 2000
mask.info()
# <class 'pandas.core.series.Series'>
# RangeIndex: 1206 entries, 0 to 1205
# Series name: year
# Non-Null Count  Dtype
# --------------  -----
# 1206 non-null   bool
# dtypes: bool(1)
# memory usage: 1.3 KB

df[mask].count()
# name              351
# link              351
# year              351
# category          351
# country           310
# born_in            41
# text              351
# wikidata_code     351
# date_of_birth     351
# date_of_death      71
# place_of_birth    351
# place_of_death     71
# gender            351
# dtype: int64

df[mask].info()
# <class 'pandas.core.frame.DataFrame'>
# Index: 351 entries, 7 to 1193
# Data columns (total 13 columns):
#  #   Column          Non-Null Count  Dtype
# ---  ------          --------------  -----
#  0   name            351 non-null    object
#  1   link            351 non-null    object
#  2   year            351 non-null    int64
#  3   category        351 non-null    object
#  4   country         310 non-null    object
#  5   born_in         41 non-null     object
#  6   text            351 non-null    object
#  7   wikidata_code   351 non-null    object
#  8   date_of_birth   351 non-null    object
#  9   date_of_death   71 non-null     object
#  10  place_of_birth  351 non-null    object
#  11  place_of_death  71 non-null     object
#  12  gender          351 non-null    object
# dtypes: int64(1), object(12)
# memory usage: 38.4+ KB

df.born_in.describe()
# count         154
# unique         49
# top       Germany
# freq           28
# Name: born_in, dtype: object

set(df.born_in.apply(type))
# {NoneType, str}

df.born_in.replace('', np.nan, inplace=True)

# The NaN fields are discounted
df.born_in.count()
# 154

# Replace all empty strings with discounted NaNs
df.replace('', np.nan, inplace=True)

df[df.name.str.contains(r'\*')]['name']  # \ for the escape char of regex
# Series([], Name: name, dtype: object)

df.name = df.name.str.replace('*', '')
# df.name = df.name.str.replace(r'\*', '', regex=True)
df.name = df.name.str.strip()

df[df.country.isnull()].born_in.count()
# 154

df[df.born_in.isnull()].country.count()
# 1052

# Remove rows with NaN in born_in
df = df[df.born_in.isnull()]
# Remove the born_in column
df = df.drop('born_in', axis=1)  # df = df.drop('born_in', axis="columns")

# Find duplicates except for the first occurrence
df[df.duplicated('name')].name.count()  # default: df.duplicated('name', keep='first')
# 80

# Find all duplicates
df[df.duplicated('name', keep=False)].name.count()
# 155

df[df.duplicated('name') | df.duplicated('name', keep='last')].name.count()
# 155

df[df.name.isin(df[df.duplicated('name')].name)].name.count()
# 155

for name, rows in df.groupby('name'):
    print(f"name: {name}, number of rows: {len(rows)}")
# ...
# name: Marie Curie, number of rows: 2
# name: Marie Skłodowska-Curie, number of rows: 2
# ...

type(df.groupby('name'))
# pandas.core.groupby.generic.DataFrameGroupBy

{name: rows for name, rows in df.groupby('name')}["Marie Curie"]
#                                            link         name  year   category  \
# 1013  https://en.wikipedia.org/wiki/Marie_Curie  Marie Curie  1911  Chemistry
# 1022  https://en.wikipedia.org/wiki/Marie_Curie  Marie Curie  1903    Physics
#
#      country                                               text wikidata_code  \
# 1013  France  Marie Curie ,  born in Congress Poland (Russia...         Q7186
# 1022  France  Marie Curie ,  born in Congress Poland, (Russi...         Q7186
#
#         date_of_birth date_of_death place_of_birth place_of_death  gender
# 1013  7 November 1867   4 July 1934         Warsaw    Sancellemoz  female
# 1022  7 November 1867   4 July 1934         Warsaw    Sancellemoz  female

{name: rows for name, rows in df.groupby('name')}["Marie Skłodowska-Curie"]
#                                           link                    name  year  \
# 700  https://en.wikipedia.org/wiki/Marie_Curie  Marie Skłodowska-Curie  1911
# 703  https://en.wikipedia.org/wiki/Marie_Curie  Marie Skłodowska-Curie  1903
#
#       category country                                               text  \
# 700  Chemistry  Poland  Marie Skłodowska-Curie ,  born in Congress Pol...
# 703    Physics  Poland  Marie Skłodowska-Curie ,  born in Congress Pol...
#
#     wikidata_code    date_of_birth date_of_death place_of_birth  \
# 700         Q7186  7 November 1867   4 July 1934         Warsaw
# 703         Q7186  7 November 1867   4 July 1934         Warsaw
#
#     place_of_death  gender
# 700    Sancellemoz  female
# 703    Sancellemoz  female

pd.concat([g for _,g in df.groupby('name') if len(g) > 1])['name']
# 281            Alan MacDiarmid
# 741            Alan MacDiarmid
# 573            Albert Einstein
# 910            Albert Einstein
# 416              Alexei Ekimov
#                  ...
# 861        William C. Campbell
# 435        William Henry Bragg
# 1181       William Henry Bragg
# 436     William Lawrence Bragg
# 1180    William Lawrence Bragg
# Name: name, Length: 155, dtype: object




