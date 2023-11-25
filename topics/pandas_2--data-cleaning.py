"""
This example of data cleaning with Pandas is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://pandas.pydata.org/pandas-docs/stable/user_guide/text.html#string-methods.
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

# # # Inspect the data

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

{name: rows for name, rows in df.groupby('name')}["Ragnar Granit"]
#                                              link           name  year  \
# 624   https://en.wikipedia.org/wiki/Ragnar_Granit  Ragnar Granit  1967
# 1091  https://en.wikipedia.org/wiki/Ragnar_Granit  Ragnar Granit  1809
#
#                     category  country born_in  \
# 624   Physiology or Medicine   Sweden    None
# 1091  Physiology or Medicine  Finland    None
#
#                                                    text wikidata_code  \
# 624   Ragnar Granit ,  born in the Grand Duchy of Fi...       Q217722
# 1091  Ragnar Granit ,  born in the Grand Duchy of Fi...       Q217722
#
#         date_of_birth  date_of_death place_of_birth place_of_death gender
# 624   30 October 1900  12 March 1991      Riihimäki      Stockholm   male
# 1091  30 October 1900  12 March 1991      Riihimäki      Stockholm   male

{name: rows for name, rows in df.groupby('name')}["Sidney Altman"]
#                                              link           name  year  \
# 228   https://en.wikipedia.org/wiki/Sidney_Altman  Sidney Altman  1989
# 1140  https://en.wikipedia.org/wiki/Sidney_Altman  Sidney Altman  1989
#
#        category        country born_in  \
# 228   Chemistry  United States    None
# 1140  Chemistry           None  Canada
#
#                                                    text wikidata_code  \
# 228   Sidney Altman ,  born in Canada , Chemistry, 1989       Q102266
# 1140                   Sidney Altman *, Chemistry, 1989       Q102266
#
#      date_of_birth date_of_death place_of_birth place_of_death gender
# 228     7 May 1939  5 April 2022       Montreal      Rockleigh   male
# 1140    7 May 1939  5 April 2022       Montreal      Rockleigh   male

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

df_scored_names = pd.DataFrame(
    {
        'name': ['zak', 'alice', 'bob', 'mike', 'bob', 'bob'],
        'score': [4, 3, 5, 2, 3, 7]
    }
)
#     name  score
# 0    zak      4
# 1  alice      3
# 2    bob      5
# 3   mike      2
# 4    bob      3
# 5    bob      7

df_scored_names.sort_values(['name', 'score'], ascending=[True, False])
#     name  score
# 1  alice      3
# 5    bob      7
# 2    bob      5
# 4    bob      3
# 3   mike      2
# 0    zak      4

df[df.duplicated('name', keep=False)].sort_values('name')[['name', 'country', 'year']]
#                    name                  country  year
# 649          Aaron Klug                     None  1982
# 512          Aaron Klug           United Kingdom  1982
# 781          Aaron Klug                     None  1982
# 546   Abdulrazak Gurnah           United Kingdom  2021
# 571   Abdulrazak Gurnah                     None  2021
# ...                 ...                      ...   ...
# 797      Yoichiro Nambu                     None  2008
# 213         Yuan T. Lee            United States  1986
# 567         Yuan T. Lee                     None  1986
# 1174     Zhores Alferov                     None  2000
# 687      Zhores Alferov  Russia and Soviet Union  2000
#
# [432 rows x 3 columns]

df["country"][700]
# 'Poland'

df["country"][700] = "France"
# A value is trying to be set on a copy of a slice from a DataFrame
#
# See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
#   df["country"][700] = "France"

df["country"][700]
# 'France'

df.iloc[700]
# link                      https://en.wikipedia.org/wiki/Marie_Curie
# name                                         Marie Skłodowska-Curie
# year                                                           1911
# category                                                  Chemistry
# country                                                      France
# born_in                                                        None
# text              Marie Skłodowska-Curie ,  born in Congress Pol...
# wikidata_code                                                 Q7186
# date_of_birth                                       7 November 1867
# date_of_death                                           4 July 1934
# place_of_birth                                               Warsaw
# place_of_death                                          Sancellemoz
# gender                                                       female
# Name: 700, dtype: object

# A better practice is to use 'loc'
df.loc[700, 'country'] = 'Poland, France'

df.iloc[700]
# link                      https://en.wikipedia.org/wiki/Marie_Curie
# name                                         Marie Skłodowska-Curie
# year                                                           1911
# category                                                  Chemistry
# country                                              Poland, France
# born_in                                                        None
# text              Marie Skłodowska-Curie ,  born in Congress Pol...
# wikidata_code                                                 Q7186
# date_of_birth                                       7 November 1867
# date_of_death                                           4 July 1934
# place_of_birth                                               Warsaw
# place_of_death                                          Sancellemoz
# gender                                                       female
# Name: 700, dtype: object

df.loc[(df.name == 'Marie Sk\u0142odowska-Curie') & (df.year == 1911)]
#                                           link                    name  year  \
# 700  https://en.wikipedia.org/wiki/Marie_Curie  Marie Skłodowska-Curie  1911
#
#       category         country born_in  \
# 700  Chemistry  Poland, France    None
#
#                                                   text wikidata_code  \
# 700  Marie Skłodowska-Curie ,  born in Congress Pol...         Q7186
#
#        date_of_birth date_of_death place_of_birth place_of_death  gender
# 700  7 November 1867   4 July 1934         Warsaw    Sancellemoz  female

# The best practice is without using the index
df.loc[(df.name == 'Marie Sk\u0142odowska-Curie') & (df.year == 1911), 'country'] = 'France'
df.loc[(df.name == 'Marie Sk\u0142odowska-Curie') & (df.year == 1911), 'country']
# 700    France
# Name: country, dtype: object

# Drop a duplicate
df.drop(
    df[(df.name == 'Sidney Altman') & (df.year == 1990)].index,
    inplace=True
)

# Another way to drop rows is by using the logical not
df = df[~((df.name == 'Sidney Altman') & (df.year == 1990))]


# Summarize all the techniques considered above in a function
def clean_data_v1(df):
    df = df.replace('', np.nan)
    df = df[df.born_in.isnull()]  # The data have either "country" or "born_in"
    df = df.drop('born_in', axis=1)
    df.drop(df[df.year == 1809].index, inplace=True)
    df = df[~(df.name == 'Marie Curie')]
    df.loc[(df.name == 'Marie Sk\u0142odowska-Curie') & (df.year == 1911), 'country'] = 'France'
    df = df[~((df.name == 'Sidney Altman') & (df.year == 1990))]
    return df


df = pd.read_json('scrapy-projects/nobel_winners/Nobel_winners_by_request_chains.json')
df = clean_data_v1(df)

# Permutate the index randomly and reindex the pd.DataFrame with it
df = df.reindex(np.random.permutation(df.index))
# Drop the duplicates sharing name and year
df = df.drop_duplicates(['name', 'year'])
# Sort the index
df = df.sort_index()
df.count()
# link              974
# name              974
# year              974
# category          973
# country           974
# text              974
# wikidata_code     974
# date_of_birth     974
# date_of_death     667
# place_of_birth    974
# place_of_death    665
# gender            974
# dtype: int64

# Combine duplicates with keep="first" and keep="last" to get them all
df[
    df.duplicated('name') | df.duplicated('name', keep='last')
].sort_values(by='name')[
    ['name', 'country', 'year', 'category']
]
#                        name         country  year   category
# 492        Frederick Sanger  United Kingdom  1958  Chemistry
# 507        Frederick Sanger  United Kingdom  1980  Chemistry
# 91             John Bardeen   United States  1956    Physics
# 160            John Bardeen   United States  1972    Physics
# 292      K. Barry Sharpless   United States  2001  Chemistry
# 424      K. Barry Sharpless   United States  2022  Chemistry
# 88         Linus C. Pauling   United States  1954  Chemistry
# 105        Linus C. Pauling   United States  1962      Peace
# 700  Marie Skłodowska-Curie          France  1911  Chemistry
# 703  Marie Skłodowska-Curie          Poland  1903    Physics

# # # missing fields

df.count()
# link              974
# name              974
# year              974
# category          973  # missing value
# country           974
# text              974
# wikidata_code     974
# date_of_birth     974
# date_of_death     667
# place_of_birth    974
# place_of_death    665
# gender            974
# dtype: int64

df[
    df.category.isnull()
][
    ['name', 'category', 'text']
]
#               name category                                               text
# 881  Róbert Bárány     None  Róbert Bárány ,  born in Austria , Medicine, 1914

# Update the data correctly
df.loc[df.name == 'Róbert Bárány', 'category'] = 'Physiology or Medicine'

df[df.gender.isnull()]['name']
# Series([], Name: name, dtype: object)

# Remove genderless entries (that does not be needed here)
# df = df[df.gender.notnull()]


def clean_data_v2(df):
    df = df.replace('', np.nan)
    df = df[df.born_in.isnull()]  # The data have either "country" or "born_in"
    df = df.drop('born_in', axis=1)
    df.drop(df[df.year == 1809].index, inplace=True)
    df = df[~(df.name == 'Marie Curie')]
    df.loc[(df.name == 'Marie Sk\u0142odowska-Curie') & (df.year == 1911), 'country'] = 'France'
    df = df[~((df.name == 'Sidney Altman') & (df.year == 1990))]
    df = df[df.gender.notnull()]
    df.loc[df.name == 'Róbert Bárány', 'category'] = 'Physiology or Medicine'
    df = df.reindex(np.random.permutation(df.index))
    df = df.drop_duplicates(['name', 'year'])
    df = df.sort_index()
    return df


df = pd.read_json('scrapy-projects/nobel_winners/Nobel_winners_by_request_chains.json')
df = clean_data_v2(df)
df.count()
# link              974
# name              974
# year              974
# category          974
# country           974
# text              974
# wikidata_code     974
# date_of_birth     974
# date_of_death     667
# place_of_birth    974
# place_of_death    665
# gender            974
# dtype: int64

# # # Deal with times and dates

df[['name', 'date_of_birth']]
#                          name     date_of_birth
# 0     Richard Adolf Zsigmondy      1 April 1865
# 1                 Fritz Pregl  3 September 1869
# 2               Róbert Bárány     22 April 1876
# 4                  Gerty Cori    15 August 1896
# 5              Wolfgang Pauli     25 April 1900
# ...                       ...               ...
# 1201    Adolfo Pérez Esquivel  26 November 1931
# 1202     Luis Federico Leloir  6 September 1906
# 1203         Bernardo Houssay     10 April 1887
# 1204    Carlos Saavedra Lamas   1 November 1878
# 1205        John Carew Eccles   27 January 1903
#
# [974 rows x 2 columns]

# df.date_of_birth = pd.to_datetime(df.date_of_birth, errors='raise')  # default: errors='raise'
# ValueError: time data "1952" doesn't match format "%d %B %Y", at position ...

df.loc[df.name == 'Venkatraman Ramakrishnan', 'date_of_birth']
# 538   1952
# Name: date_of_birth, dtype: datetime64[ns]

df.loc[df.name == 'Michael Houghton', 'date_of_birth']
# 549    1949
# Name: date_of_birth, dtype: object

for i, row in df.iterrows():
    try:
        print(f"date_of_birth: {pd.to_datetime(row.date_of_birth, errors='raise')}; name: {row['name']}; index: {i}")
    except Exception as e:
        print(f"date_of_birth: {row['date_of_birth']}; name: {row['name']}")
        print(e)
# ...
# date_of_birth: 1949-01-01 00:00:00; name: Michael Houghton; index: 549
# ...

df.date_of_birth = pd.to_datetime(df.date_of_birth, errors='coerce')
df.loc[df.name == 'Michael Houghton', 'date_of_birth']
# 549   NaT
# Name: date_of_birth, dtype: datetime64[ns]

df[df.date_of_birth.isnull()].name
# 409                   David Card
# 538     Venkatraman Ramakrishnan
# 549             Michael Houghton
# 651                Albert Lutuli
# 860                  Nadia Murad
# 1117       Karl Adolph Gjellerup
# Name: name, dtype: object

df[df.date_of_birth.isnull()].name.count()
# 6

df.loc[df.name == 'Venkatraman Ramakrishnan', 'date_of_birth'] = pd.to_datetime("1 April 1952")
df.loc[df.name == 'Nadia Murad', 'date_of_birth'] = pd.to_datetime("10 March 1993")
df.loc[df.name == 'Karl Adolph Gjellerup', 'date_of_birth'] = pd.to_datetime("2 June 1857")

df[df.date_of_birth.isnull()].name.count()
# 3

df.loc[df.name == 'David Card', 'date_of_birth'] = pd.to_datetime("1956")
df.loc[df.name == 'Michael Houghton', 'date_of_birth'] = pd.to_datetime("1949")
df.loc[df.name == 'Albert Lutuli', 'date_of_birth'] = pd.to_datetime("1898")

df.date_of_death = pd.to_datetime(df.date_of_death, errors='coerce')

df['award_age'] = (df.year - pd.DatetimeIndex(df.date_of_birth).year).astype("int64")

# Get the youngest recipients of the Nobel Prize
df.sort_values('award_age').iloc[:10][['name', 'award_age', 'category', 'year']]
#                         name  award_age                category  year
# 727         Malala Yousafzai         17                   Peace  2014
# 860              Nadia Murad         25                   Peace  2018
# 1180  William Lawrence Bragg         25                 Physics  1915
# 50             Carl Anderson         31                 Physics  1936
# 926   Werner Karl Heisenberg         31                 Physics  1932
# 447               Paul Dirac         31                 Physics  1933
# 115            Tsung-Dao Lee         31                 Physics  1957
# 959         Rudolf Mössbauer         32                 Physics  1961
# 32           Tawakkol Karman         32                   Peace  2011
# 1149       Frederick Banting         32  Physiology or Medicine  1923

df.sort_values('award_age').iloc[-10:][['name', 'award_age', 'category', 'year']]
#                     name  award_age                category  year
# 984      Karl von Frisch         87  Physiology or Medicine  1973
# 540        Doris Lessing         88              Literature  2007
# 287    Raymond Davis Jr.         88                 Physics  2002
# 363     Lloyd S. Shapley         89               Economics  2012
# 548        Roger Penrose         89                 Physics  2020
# 11        Syukuro Manabe         90                 Physics  2021
# 334       Leonid Hurwicz         90               Economics  2007
# 1007    Klaus Hasselmann         90                 Physics  2021
# 394        Arthur Ashkin         96                 Physics  2018
# 405   John B. Goodenough         97               Chemistry  2019


def clean_data_v3(df):
    df = df.replace('', np.nan)
    df_born_in = df[df.born_in.notnull()][["name", "born_in"]]
    df = df[df.born_in.isnull()]  # The data have either "country" or "born_in"
    df = df.drop('born_in', axis=1)
    df.drop(df[df.year == 1809].index, inplace=True)
    df = df[~(df.name == 'Marie Curie')]
    df.loc[(df.name == 'Marie Sk\u0142odowska-Curie') & (df.year == 1911), 'country'] = 'France'
    df = df[~((df.name == 'Sidney Altman') & (df.year == 1990))]
    df = df[df.gender.notnull()]
    df.loc[df.name == 'Róbert Bárány', 'category'] = 'Physiology or Medicine'
    df = df.reindex(np.random.permutation(df.index))
    df = df.drop_duplicates(['name', 'year'])
    df = df.sort_index()
    df.date_of_birth = pd.to_datetime(df.date_of_birth, errors='coerce')
    df.loc[df.name == 'Venkatraman Ramakrishnan', 'date_of_birth'] = pd.to_datetime("1 April 1952")
    df.loc[df.name == 'Nadia Murad', 'date_of_birth'] = pd.to_datetime("10 March 1993")
    df.loc[df.name == 'Karl Adolph Gjellerup', 'date_of_birth'] = pd.to_datetime("2 June 1857")
    df.loc[df.name == 'David Card', 'date_of_birth'] = pd.to_datetime("1956")
    df.loc[df.name == 'Michael Houghton', 'date_of_birth'] = pd.to_datetime("1949")
    df.loc[df.name == 'Albert Lutuli', 'date_of_birth'] = pd.to_datetime("1898")
    return df, df_born_in


df = pd.read_json('scrapy-projects/nobel_winners/Nobel_winners_by_request_chains.json')
df, df_born_in = clean_data_v3(df)
df.count()
# link              974
# name              974
# year              974
# category          974
# country           974
# text              974
# wikidata_code     974
# date_of_birth     974
# date_of_death     667
# place_of_birth    974
# place_of_death    665
# gender            974
# dtype: int64

df_born_in.count()
# name       154
# born_in    154
# dtype: int64

df_born_in.drop_duplicates(subset=['name'], inplace=True)
df_born_in.count()
# name       144
# born_in    144
# dtype: int64

df_born_in.set_index('name', inplace=True)
df_born_in.loc['Albert Camus']
# born_in    Algeria
# Name: Albert Camus, dtype: object


def clean_data_v4(df):
    df = df.replace('', np.nan)
    df_born_in = df[df.born_in.notnull()][["name", "born_in"]]
    df = df[df.born_in.isnull()]  # The data have either "country" or "born_in"
    df = df.drop('born_in', axis=1)
    df.drop(df[df.year == 1809].index, inplace=True)
    df = df[~(df.name == 'Marie Curie')]
    df.loc[(df.name == 'Marie Sk\u0142odowska-Curie') & (df.year == 1911), 'country'] = 'France'
    df = df[~((df.name == 'Sidney Altman') & (df.year == 1990))]
    df = df[df.gender.notnull()]
    df.loc[df.name == 'Róbert Bárány', 'category'] = 'Physiology or Medicine'
    df = df.reindex(np.random.permutation(df.index))
    df = df.drop_duplicates(['name', 'year'])
    df = df.sort_index()
    df.date_of_birth = pd.to_datetime(df.date_of_birth, errors='coerce')
    df.loc[df.name == 'Venkatraman Ramakrishnan', 'date_of_birth'] = pd.to_datetime("1 April 1952")
    df.loc[df.name == 'Nadia Murad', 'date_of_birth'] = pd.to_datetime("10 March 1993")
    df.loc[df.name == 'Karl Adolph Gjellerup', 'date_of_birth'] = pd.to_datetime("2 June 1857")
    df.loc[df.name == 'David Card', 'date_of_birth'] = pd.to_datetime("1956")
    df.loc[df.name == 'Michael Houghton', 'date_of_birth'] = pd.to_datetime("1949")
    df.loc[df.name == 'Albert Lutuli', 'date_of_birth'] = pd.to_datetime("1898")
    df.date_of_death = pd.to_datetime(df.date_of_death, errors='coerce')
    df_born_in.drop_duplicates(subset=['name'], inplace=True)
    df_born_in.set_index('name', inplace=True)

    def get_born_in(name):
        try:
            born_in = df_born_in.loc[name]['born_in']
        except:
            born_in = np.nan
        return born_in

    df['born_in'] = df['name'].apply(get_born_in)
    return df


df = pd.read_json('scrapy-projects/nobel_winners/Nobel_winners_by_request_chains.json')
df = clean_data_v4(df)
df.count()
# link              974
# name              974
# year              974
# category          974
# country           974
# text              974
# wikidata_code     974
# date_of_birth     974
# date_of_death     667
# place_of_birth    974
# place_of_death    665
# gender            974
# born_in           136
# dtype: int64


def clean_data_v5(df):
    df = df.replace('', np.nan)
    df_born_in = df[df.born_in.notnull()][["name", "born_in"]]
    df = df[df.born_in.isnull()]  # The data have either "country" or "born_in"
    df = df.drop('born_in', axis=1)
    df.drop(df[df.year == 1809].index, inplace=True)
    df = df[~(df.name == 'Marie Curie')]
    df.loc[(df.name == 'Marie Sk\u0142odowska-Curie') & (df.year == 1911), 'country'] = 'France'
    df = df[~((df.name == 'Sidney Altman') & (df.year == 1990))]
    df = df[df.gender.notnull()]
    df.loc[df.name == 'Róbert Bárány', 'category'] = 'Physiology or Medicine'
    df = df.reindex(np.random.permutation(df.index))
    df = df.drop_duplicates(['name', 'year'])
    df = df.sort_index()
    df.date_of_birth = pd.to_datetime(df.date_of_birth, errors='coerce')
    df.loc[df.name == 'Venkatraman Ramakrishnan', 'date_of_birth'] = pd.to_datetime("1 April 1952")
    df.loc[df.name == 'Nadia Murad', 'date_of_birth'] = pd.to_datetime("10 March 1993")
    df.loc[df.name == 'Karl Adolph Gjellerup', 'date_of_birth'] = pd.to_datetime("2 June 1857")
    df.loc[df.name == 'David Card', 'date_of_birth'] = pd.to_datetime("1956")
    df.loc[df.name == 'Michael Houghton', 'date_of_birth'] = pd.to_datetime("1949")
    df.loc[df.name == 'Albert Lutuli', 'date_of_birth'] = pd.to_datetime("1898")
    df.date_of_death = pd.to_datetime(df.date_of_death, errors='coerce')
    df_born_in.drop_duplicates(subset=['name'], inplace=True)
    df_born_in.set_index('name', inplace=True)
    df.set_index('name', inplace=True)
    df['born_in'] = df_born_in.born_in
    df['award_age'] = (df.year - pd.DatetimeIndex(df.date_of_birth).year).astype("int64")
    return df


df = pd.read_json('scrapy-projects/nobel_winners/Nobel_winners_by_request_chains.json')
df = clean_data_v5(df)
df.count()
# link              974
# year              974
# category          974
# country           974
# text              974
# wikidata_code     974
# date_of_birth     974
# date_of_death     667
# place_of_birth    974
# place_of_death    665
# gender            974
# born_in           136
# award_age         974
# dtype: int64

df.loc['Albert Camus']
# link                     https://en.wikipedia.org/wiki/Albert_Camus
# year                                                           1957
# category                                                 Literature
# country                                                      France
# text              Albert Camus ,  born in French Algeria , Liter...
# wikidata_code                                                Q34670
# date_of_birth                                   1913-11-07 00:00:00
# date_of_death                                   1960-01-04 00:00:00
# place_of_birth                                                Dréan
# place_of_death                                          Villeblevin
# gender                                                         male
# born_in                                                     Algeria
# award_age                                                        44
# Name: Albert Camus, dtype: object

df.loc['Lê Đức Thọ']
# link              https://en.wikipedia.org/wiki/L%C3%AA_%C4%90%E...
# year                                                           1973
# category                                                      Peace
# country                                                     Vietnam
# text              Lê Đức Thọ ,  born in French Indochina , Peace...
# wikidata_code                                               Q233969
# date_of_birth                                   1911-10-14 00:00:00
# date_of_death                                   1990-10-13 00:00:00
# place_of_birth                                               Hà Nam
# place_of_death                                                Hanoi
# gender                                                         male
# born_in                                                         NaN
# award_age                                                        62
# Name: Lê Đức Thọ, dtype: object

df.to_json('json-files/nobel_winners_cleaned.json', orient='records', date_format='iso')

import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///sqlite-databases/nobel_winners_for_pandas.db')
df.to_sql('winners_cleaned', engine, if_exists='replace')
# 974

df_from_sql = pd.read_sql('winners_cleaned', engine)
df_from_sql.count()
# name              974
# link              974
# year              974
# category          974
# country           974
# text              974
# wikidata_code     974
# date_of_birth     974
# date_of_death     667
# place_of_birth    974
# place_of_death    665
# gender            974
# born_in           136
# award_age         974
# dtype: int64

df.to_parquet('parquet-files/nobel_winners_cleaned.parquet')  # precondition: fastparquet installed
