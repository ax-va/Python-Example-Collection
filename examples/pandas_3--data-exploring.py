"""
This example of data exploring with Pandas is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html;
- https://seaborn.pydata.org/tutorial/color_palettes.html.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
plt.rcParams['figure.figsize'] = (8, 4)
plt.rcParams['font.size'] = '14'

df = pd.read_json('json-files/nobel_winners_cleaned.json')
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 974 entries, 0 to 973
# Data columns (total 13 columns):
#  #   Column          Non-Null Count  Dtype
# ---  ------          --------------  -----
#  0   link            974 non-null    object
#  1   year            974 non-null    int64
#  2   category        974 non-null    object
#  3   country         974 non-null    object
#  4   text            974 non-null    object
#  5   wikidata_code   974 non-null    object
#  6   date_of_birth   974 non-null    object
#  7   date_of_death   667 non-null    object
#  8   place_of_birth  974 non-null    object
#  9   place_of_death  665 non-null    object
#  10  gender          974 non-null    object
#  11  born_in         136 non-null    object
#  12  award_age       974 non-null    int64
# dtypes: int64(2), object(11)
# memory usage: 99.0+ KB

df = pd.read_parquet('parquet-files/nobel_winners_cleaned.parquet')  # precondition: fastparquet installed
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

df.groupby('gender').size()  # type: pd.Series
# gender
# female     65
# male      909
# dtype: int64
df.groupby('gender').size().plot(kind='bar')
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-01--genders.svg')
plt.close()

# arguments of kind:
# - "bar" or "barh"
# - "hist"
# - "box"
# - "scatter"

# # # Investigate gender disparities

by_cat_gen = df.groupby(['category','gender'])
by_cat_gen.size()  # pd.Series with pd.MultiIndex
# category                gender
# Chemistry               female      8
#                         male      185
# Economics               female      3
#                         male       90
# Literature              female     17
#                         male      103
# Peace                   female     19
#                         male       92
# Physics                 female      5
#                         male      223
# Physiology or Medicine  female     13
#                         male      216
# dtype: int64

by_cat_gen.get_group(('Physics', 'female'))
#                                                                      link  year category        country                                               text  ... place_of_birth place_of_death  gender  born_in award_age
# name                                                                                                                                                        ...
# Maria Goeppert-Mayer    https://en.wikipedia.org/wiki/Maria_Goeppert-M...  1963  Physics  United States  Maria Goeppert-Mayer ,  born in then Germany, ...  ...       Katowice      San Diego  female  Germany        57
# Andrea Ghez                  https://en.wikipedia.org/wiki/Andrea_M._Ghez  2020  Physics  United States                        Andrea Ghez , Physics, 2020  ...  New York City           None  female     None        55
# Anne L'Huillier           https://en.wikipedia.org/wiki/Anne_L%27Huillier  2023  Physics         Sweden  Anne L'Huillier ,  born in France , Physics, 2023  ...          Paris           None  female     None        65
# Marie Skłodowska-Curie          https://en.wikipedia.org/wiki/Marie_Curie  1903  Physics         Poland  Marie Skłodowska-Curie ,  born in Congress Pol...  ...         Warsaw    Sancellemoz  female     None        36
# Donna Strickland           https://en.wikipedia.org/wiki/Donna_Strickland  2018  Physics         Canada                   Donna Strickland , Physics, 2018  ...         Guelph           None  female     None        59
#
# [5 rows x 13 columns]

by_cat_gen.get_group(('Physics', 'female'))['year'].sort_values()
# name
# Marie Skłodowska-Curie    1903
# Maria Goeppert-Mayer      1963
# Donna Strickland          2018
# Andrea Ghez               2020
# Anne L'Huillier           2023
# Name: year, dtype: int64

by_cat_gen.size().plot(kind='barh')
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-02--categories-and-genders.svg')
plt.close()

# # # Unstack groups

# Unstack the second multiple index in columns
by_cat_gen.size().unstack()
# gender                  female  male
# category
# Chemistry                    8   185
# Economics                    3    90
# Literature                  17   103
# Peace                       19    92
# Physics                      5   223
# Physiology or Medicine      13   216

by_cat_gen.size().unstack().plot(kind='barh')
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-03--unstacked-categories-and-genders.svg')
plt.close()

cat_gen_sz = by_cat_gen.size().unstack()
cat_gen_sz['female_ratio'] = cat_gen_sz.female / (cat_gen_sz.female + cat_gen_sz.male)
cat_gen_sz
# gender                  female  male  female_ratio
# category
# Chemistry                    8   185      0.041451
# Economics                    3    90      0.032258
# Literature                  17   103      0.141667
# Peace                       19    92      0.171171
# Physics                      5   223      0.021930
# Physiology or Medicine      13   216      0.056769

# female_ratio in percent
cat_gen_sz['female_pct'] = cat_gen_sz['female_ratio'] * 100

cat_gen_sz = cat_gen_sz.sort_values(by='female_pct', ascending=True)
ax = cat_gen_sz[['female_pct']].plot(kind='barh')
ax.set_xlim([0, 100])
ax.set_xlabel('% of female Nobel Prize winners')
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-04--female-pct.svg')
plt.close()

df[(df.category == 'Physics') & (df.gender == 'female')][['country', 'year']].sort_values('year')
#                              country  year
# name
# Marie Skłodowska-Curie         Poland  1903
# Maria Goeppert-Mayer    United States  1963
# Donna Strickland               Canada  2018
# Andrea Ghez             United States  2020
# Anne L'Huillier                Sweden  2023

# # # Explore historical trends by gender

by_year_gender = df.groupby(['year', 'gender'])
by_year_gender.size().unstack()
# gender  female  male
# year
# 1901       NaN   6.0
# 1902       NaN   7.0
# 1903       1.0   6.0
# 1904       NaN   5.0
# 1905       1.0   4.0
# ...        ...   ...
# 2019       1.0  13.0
# 2020       4.0   7.0
# 2021       1.0  12.0
# 2022       2.0  10.0
# 2023       4.0   7.0
#
# [120 rows x 2 columns]

# Take into account missing years 1939-1945
new_index = pd.Index(np.arange(1901, 2024), name='year')
by_year_gender = df.groupby(['year', 'gender'])
year_gen_sz = by_year_gender.size().unstack().reindex(new_index)

# female winners in percent
year_gen_sz['female_pct'] = year_gen_sz.female / (year_gen_sz.female + year_gen_sz.male) * 100
ax = year_gen_sz.female_pct.plot(kind='bar', figsize=(16, 4))
# BUG:
# The problem is that the Pandas' "plot" does not take the "index" of Series
# or DataFrame as the x-axis values but sets sequential indices starting from 0.
# Thus, the x-axis values are wrong but the x-axis labels remain correct.

# ax.xaxis.get_ticklocs()
# array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,
# ...
#        117, 118, 119, 120, 121, 122])

# instead of
# array([1901, 1902, ..., 2022, 2023])

# [lb.get_text() for lb in ax.xaxis.get_ticklabels()]
# ['1901', ... '2023']

# BUG REPORT:
# https://github.com/pandas-dev/pandas/issues/55508
# pd.__version__
# '2.1.3'

# female and male historical trends
fig, axes = plt.subplots(
    nrows=2, ncols=1,
    sharex=True, sharey=True,
    figsize=(16, 8)
)
ax_f = axes[0]
ax_m = axes[1]
fig.suptitle('Nobel Prize-winners by gender', fontsize=16)
ax_f.bar(x=year_gen_sz.index, height=year_gen_sz.female)
ax_m.bar(x=year_gen_sz.index, height=year_gen_sz.male)
ax_f.set_ylabel('Female winners')
ax_m.set_ylabel('Male winners')
ax_m.set_xlabel('Year')
# Reduce xticks and rotate xtick labels
xticks = np.array(range(1900, 2024, 10))
ax_m.xaxis.set_ticks(xticks)
ax_m.xaxis.set_ticklabels([str(year) for year in xticks], rotation=45)
fig.tight_layout()
fig.savefig('pandas-data-exploring-figures/figure-05--female-and-male-historical-trends.svg')
plt.close()

# # # Explore national trends

df.groupby('country').size()
# country
# Argentina           4
# Australia          10
# Austria            16
# Bangladesh          1
# Belarus             2
#                  ...
# United Kingdom    120
# United States     375
# Vietnam             1
# Yemen               1
# Yugoslavia          2
# Length: 62, dtype: int64

df.groupby('country').size().sort_values(ascending=False)
# country
# United States     375
# United Kingdom    120
# Germany            85
# France             67
# Sweden             33
#                  ...
# Iceland             1
# Palestine           1
# Kenya               1
# Nigeria             1
# Philippines         1
# Length: 62, dtype: int64

df.groupby('country').size().sort_values(ascending=False)[:20].plot(kind='bar', figsize=(16, 8), fontsize=10)
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-06--national-trends.svg')
plt.close()

# # # Explore prize winners per capita

nat_group = df.groupby('country')
ngsz = nat_group.size()
# country
# Argentina           4
# Australia          10
# Austria            16
# Bangladesh          1
# Belarus             2
#                  ...
# United Kingdom    120
# United States     375
# Vietnam             1
# Yemen               1
# Yugoslavia          2
# Length: 62, dtype: int64

df_countries = pd.read_json('json-files/world-country-data.json')
df_countries["name"].head(3)
# 0    {'common': 'French Polynesia', 'official': 'Fr...
# 1    {'common': 'Saint Martin', 'official': 'Saint ...
# 2    {'common': 'Venezuela', 'official': 'Bolivaria...
# Name: name, dtype: object

pd.json_normalize(data=df_countries["name"]).head(3)
#              common                          official nativeName.fra.official nativeName.fra.common  ... nativeName.lit.official nativeName.lit.common nativeName.cal.official nativeName.cal.common
# 0  French Polynesia                  French Polynesia     Polynésie française   Polynésie française  ...                     NaN                   NaN                     NaN                   NaN
# 1      Saint Martin                      Saint Martin            Saint-Martin          Saint-Martin  ...                     NaN                   NaN                     NaN                   NaN
# 2         Venezuela  Bolivarian Republic of Venezuela                     NaN                   NaN  ...                     NaN                   NaN                     NaN                   NaN
#
# [3 rows x 308 columns]

df_countries["population"].head(3)
# 0      280904
# 1       38659
# 2    28435943
# Name: population, dtype: int64

df_final = pd.DataFrame(
    data={
        "country": pd.json_normalize(data=df_countries["name"])["common"],
        "population": df_countries["population"],
    }
)
df_final = df_final.set_index("country")
df_final
#                           population
# country
# French Polynesia              280904
# Saint Martin                   38659
# Venezuela                   28435943
# Réunion                       840974
# El Salvador                  6486201
# ...                              ...
# Northern Mariana Islands       57557
# Botswana                     2351625
# Panama                       4314768
# Gabon                        2225728
# Ecuador                     17643060
#
# [250 rows x 1 columns]

df_final.loc["Japan"]
# population    125836021
# Name: Japan, dtype: int64

df_final.loc["Argentina"]
# population    45376763
# Name: Argentina, dtype: int64

df_final.loc["Germany"]
# population    83240525
# Name: Germany, dtype: int64

df_final['nobel_wins'] = ngsz
#                           population  nobel_wins
# country
# French Polynesia              280904         NaN
# Saint Martin                   38659         NaN
# Venezuela                   28435943         NaN
# Réunion                       840974         NaN
# El Salvador                  6486201         NaN
# ...                              ...         ...
# Northern Mariana Islands       57557         NaN
# Botswana           df_final.loc["Germany"]          2351625         NaN
# Panama                       4314768         NaN
# Gabon                        2225728         NaN
# Ecuador                     17643060         NaN

df_final.loc["Germany"]
# population    83240525.0
# nobel_wins          85.0
# Name: Germany, dtype: float64

df_final.loc["Russia"]
# population               144104080.0
# nobel_wins                       NaN
# Name: Russia, dtype: float64

# df_final.loc["Russia and Soviet Union"]
# KeyError

df_final['nobel_wins_per_capita'] = df_final.nobel_wins / df_final.population
# Note:
# the analysis is not correct because, for example, we have "Russia" for population and
# "Russia and Soviet Union" for prize winners (that is not added to df_final), and so on.

df_final.nobel_wins_per_capita.sort_values(ascending=False)[:10].plot(kind='bar', figsize=(16, 8), fontsize=10)
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-07--nobel-wins-per-capita.svg')
plt.close()

df_final[df_final.nobel_wins > 2].nobel_wins_per_capita.sort_values(ascending=False)[:10].plot(kind='bar', figsize=(16, 8), fontsize=10)
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-08--nobel-wins-per-capita-with-more-than-two-wins.svg')
plt.close()

# # # Explore prizes by category

nat_cat_sz = df.groupby(['country', 'category']).size().unstack()
# category        Chemistry  Economics  Literature  Peace  Physics  Physiology or Medicine
# country
# Argentina             1.0        NaN         NaN    2.0      NaN                     1.0
# Australia             NaN        NaN         1.0    NaN      2.0                     7.0
# Austria               2.0        NaN         2.0    2.0      5.0                     5.0
# Bangladesh            NaN        NaN         NaN    1.0      NaN                     NaN
# Belarus               NaN        NaN         1.0    1.0      NaN                     NaN
# ...                   ...        ...         ...    ...      ...                     ...
# United Kingdom       30.0       10.0        13.0    9.0     26.0                    32.0
# United States        76.0       63.0        13.0   21.0     97.0                   105.0
# Vietnam               NaN        NaN         NaN    1.0      NaN                     NaN
# Yemen                 NaN        NaN         NaN    1.0      NaN                     NaN
# Yugoslavia            1.0        NaN         1.0    NaN      NaN                     NaN
#
# [62 rows x 6 columns]

# How to iterate by columns:
df2 = pd.DataFrame(
    data={
        "a": [1, 2, 3],
        "b": [4, 5, 6]
    },
    index=[1900, 1950, 2000]
)
#       a  b
# 1900  1  4
# 1950  2  5
# 2000  3  6

# Iterate by columns
for x, y in df2.items():
    print("column:", x)
    print(y.sort_values(ascending=False))
    print("-"*10)
# column: a
# 2000    3
# 1950    2
# 1900    1
# Name: a, dtype: int64
# ----------
# column: b
# 2000    6
# 1950    5
# 1900    4
# Name: b, dtype: int64
# ----------

ncols = 2
nrows = 3

fig, axes = plt.subplots(nrows, ncols, figsize=(12, 12))
for i, (category_name, category_ser) in enumerate(nat_cat_sz.items()):
    ax = axes[i // ncols, i % ncols]
    category_ser = category_ser.sort_values(ascending=False)[:10]
    category_ser.plot(kind='bar', ax=ax)
    ax.set_title(category_name)
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-09--categories-and-countires-bar-plot.svg')
plt.close()

fig, axes = plt.subplots(nrows, ncols, figsize=(12, 12))
for i, (category_name, category_ser) in enumerate(nat_cat_sz.items()):
    ax = axes[i // ncols, i % ncols]
    category_ser = category_ser.sort_values(ascending=False)[:10]
    # Sort again to plot barh correctly (so it plots from bottom to top)
    category_ser = category_ser.sort_values()
    category_ser.plot(kind='barh', ax=ax)
    ax.set_title(category_name)
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-10--categories-and-countires-barh-plot.svg')
plt.close()

# # # Explore historical trends in prize distribution

plt.rcParams['font.size'] = 20

new_index = pd.Index(np.arange(1901, 2024), name='year')
by_year_nat_sz = df.groupby(['year', 'country']).size().unstack().reindex(new_index)
# country  Argentina  Australia  Austria  Bangladesh  Belarus  Belgium  Bosnia and Herzegovina  Canada  Chile  ...  Tibet  Tunisia  Turkey  Ukraine  United Kingdom  United States  Vietnam  Yemen  Yugoslavia
# year                                                                                                         ...
# 1901           NaN        NaN      NaN         NaN      NaN      NaN                     NaN     NaN    NaN  ...    NaN      NaN     NaN      NaN             NaN            NaN      NaN    NaN         NaN
# 1902           NaN        NaN      NaN         NaN      NaN      NaN                     NaN     NaN    NaN  ...    NaN      NaN     NaN      NaN             1.0            NaN      NaN    NaN         NaN
# 1903           NaN        NaN      NaN         NaN      NaN      NaN                     NaN     NaN    NaN  ...    NaN      NaN     NaN      NaN             1.0            NaN      NaN    NaN         NaN
# 1904           NaN        NaN      NaN         NaN      NaN      NaN                     NaN     NaN    NaN  ...    NaN      NaN     NaN      NaN             2.0            NaN      NaN    NaN         NaN
# 1905           NaN        NaN      1.0         NaN      NaN      NaN                     NaN     NaN    NaN  ...    NaN      NaN     NaN      NaN             NaN            NaN      NaN    NaN         NaN
# ...            ...        ...      ...         ...      ...      ...                     ...     ...    ...  ...    ...      ...     ...      ...             ...            ...      ...    ...         ...
# 2019           NaN        NaN      1.0         NaN      NaN      NaN                     NaN     1.0    NaN  ...    NaN      NaN     NaN      NaN             1.0            6.0      NaN    NaN         NaN
# 2020           NaN        NaN      NaN         NaN      NaN      NaN                     NaN     NaN    NaN  ...    NaN      NaN     NaN      NaN             2.0            7.0      NaN    NaN         NaN
# 2021           NaN        NaN      NaN         NaN      NaN      NaN                     NaN     NaN    NaN  ...    NaN      NaN     NaN      NaN             2.0            4.0      NaN    NaN         NaN
# 2022           NaN        NaN      1.0         NaN      1.0      NaN                     NaN     NaN    NaN  ...    NaN      NaN     NaN      NaN             NaN            6.0      NaN    NaN         NaN
# 2023           NaN        NaN      1.0         NaN      NaN      NaN                     NaN     NaN    NaN  ...    NaN      1.0     NaN      NaN             NaN            4.0      NaN    NaN         NaN
#
# [123 rows x 62 columns]

by_year_nat_sz['United States']
# year
# 1901    NaN
# 1902    NaN
# 1903    NaN
# 1904    NaN
# 1905    NaN
#        ...
# 2019    6.0
# 2020    7.0
# 2021    4.0
# 2022    6.0
# 2023    4.0
# Name: United States, Length: 123, dtype: float64

# cumulative sum of Nobel Prizes by country over years
ax = by_year_nat_sz['United States'].cumsum().plot()
ax.set_xlim([1900, 2025])
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-11--us-wins-cumsum-with-gaps.svg')
plt.close()

by_year_nat_sz['United States'].fillna(0)
# year
# 1901    0.0
# 1902    0.0
# 1903    0.0
# 1904    0.0
# 1905    0.0
#        ...
# 2019    6.0
# 2020    7.0
# 2021    4.0
# 2022    6.0
# 2023    4.0
# Name: United States, Length: 123, dtype: float64

ax = by_year_nat_sz['United States'].fillna(0).cumsum().plot()
ax.set_xlim([1900, 2025])
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-12--us-wins-cumsum-without-gaps.svg')
plt.close()

ax = by_year_nat_sz['Germany'].cumsum().plot()
ax.set_xlim([1900, 2025])
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-13--germany-wins-cumsum-with-gaps.svg')
plt.close()

ax = by_year_nat_sz['Germany'].fillna(0).cumsum().plot()
ax.set_xlim([1900, 2025])
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-14--germany-wins-cumsum-without-gaps.svg')
plt.close()

ax = by_year_nat_sz[['United States', 'Germany']].fillna(0).cumsum().plot()
ax.set_xlim([1900, 2025])
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-15--us-and-germany-wins-cumsum-without-gaps.svg')
plt.close()

# # # Compare the US prize rate with that of the rest of the world

by_year_nat_sz = df.groupby(['year', 'country']).size().unstack().fillna(0)
not_US = by_year_nat_sz.columns.tolist()
# ['Argentina',
# ...
#  'Yugoslavia']
not_US.remove('United States')

by_year_nat_sz['Not US'] = by_year_nat_sz[not_US].sum(axis=1)
ax = by_year_nat_sz[['United States', 'Not US']].cumsum().plot(style=['-', '--'])
ax.set_xlim([1900, 2025])
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-16--us-vs-other-countries-wins-cumsum-without-gaps.svg')
plt.close()

# Investigate the winners in North America, Europe, and Asia

regions = [
    {
        'label': 'North America',
        'countries': ['United States', 'Canada']
    },
    {
        'label': 'Europe',
        'countries': ['United Kingdom', 'Germany', 'France', 'Sweden', 'Switzerland', 'Russia and Soviet Union', 'Netherlands']
    },
    {
        'label': 'Asia',
        'countries': ['Japan', 'India']
    }
]

for region in regions:
    by_year_nat_sz[region['label']] = by_year_nat_sz[region['countries']].sum(axis=1)

by_year_nat_sz[[r['label'] for r in regions]].cumsum().plot(style=['-', '--', '-.'])
ax.set_xlim([1900, 2025])
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-17--namerica-vs-europe-vs-asia-wins-cumsum-without-gaps.svg')
plt.close()

# Investigate 16 biggest winners, excluding the outlying United States

ncols = 4
nrows = 4

by_nat_sz = df.groupby('country').size()
by_nat_sz = by_nat_sz.sort_values(ascending=False)
fig, axes = plt.subplots(ncols, nrows, sharex=True, sharey=True, figsize=(12,12))
for i, nat in enumerate(by_nat_sz.index[1:17]):
    ax = axes[i //ncols, i % nrows]
    by_year_nat_sz[nat].cumsum().plot(ax=ax)
    ax.set_title(nat)
    ax.set_xlim([1900, 2025])
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-18--biggest-excl-us-wins-cumsum-without-gaps.svg')
plt.close()

# heatmap with seaborn

sns.set(font_scale=1.5)

# Gets our bin ranges for the decades from 1901
bins = np.arange(df.year.min(), df.year.max(), 10)
# array([1901, 1911, 1921, 1931, 1941, 1951, 1961, 1971, 1981, 1991, 2001,
#        2011, 2021])

pd.cut(df.year, bins, precision=0)
# 0      (1921, 1931]
# 1      (1921, 1931]
# 2      (1941, 1951]
# 3      (1941, 1951]
# 4      (2011, 2021]
#            ...
# 969    (1971, 1981]
# 970    (1961, 1971]
# 971    (1941, 1951]
# 972    (1931, 1941]
# 973    (1961, 1971]
# Name: year, Length: 974, dtype: category
# Categories (12, interval[int64, right]): [(1901, 1911] < (1911, 1921] < (1921, 1931] < (1931, 1941] <
#                                           ... < (1981, 1991] < (1991, 2001] <
#                                           (2001, 2011] < (2011, 2021]]

df.groupby(
    ['country', pd.cut(df.year, bins, precision=0)],
    observed=False
).size()
# country     year
# Argentina   (1901, 1911]    0
#             (1911, 1921]    0
#             (1921, 1931]    0
#             (1931, 1941]    1
#             (1941, 1951]    1
#                            ..
# Yugoslavia  (1971, 1981]    1
#             (1981, 1991]    0
#             (1991, 2001]    0
#             (2001, 2011]    0
#             (2011, 2021]    0
# Length: 744, dtype: int64

by_year_nat_binned = df.groupby(
    ['country', pd.cut(df.year, bins, precision=0)],
    observed=False
).size().unstack().fillna(0)
plt.figure(figsize=(8, 8))
sns.heatmap(
    by_year_nat_binned[by_year_nat_binned.sum(axis=1) > 2],  # Filter for those countries with over two Nobel Prizes
    cmap='rocket_r'
)
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-19--country-and-decades-heatmap.svg')
plt.close()

# # # Explore age and life expectancy of winners

# # # age at time of award

df['award_age'].hist(bins=30)
plt.savefig('pandas-data-exploring-figures/figure-20--award-age-hist.svg')
plt.close()

sns.displot(df['award_age'], kde=True, height=4, aspect=2)
plt.savefig('pandas-data-exploring-figures/figure-21--award-age-displot.svg')
plt.close()

sns.boxplot(df, x='gender', y='award_age')
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-22--award-age-and-gender-boxplot.svg')
plt.close()

# Combine the box plot with a kernel density estimation in the violin plot
sns.violinplot(data=df, x='gender', y='award_age')
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-23--award-age-and-gender-violinplot.svg')
plt.close()

# # # life expectancy of winners

df['age_at_death'] = (df.date_of_death - df.date_of_birth).dt.days / 365
# Remove all empty NaN rows
age_at_death = df[df.age_at_death.notnull()].age_at_death
sns.displot(age_at_death, bins=40, kde=True, aspect=2, height=4)
plt.savefig('pandas-data-exploring-figures/figure-24--age-at-death-displot.svg')
plt.close()

df[df.age_at_death > 100][['category', 'year']]
#                                     category  year
# name
# Rita Levi-Montalcini  Physiology or Medicine  1986
# Ronald Coase                       Economics  1991
# John B. Goodenough                 Chemistry  2019
# Edmond H. Fischer     Physiology or Medicine  1992

df_temp = df[df.age_at_death.notnull()]
sns.kdeplot(df_temp[df_temp.gender == 'male'].age_at_death, fill=True, label='male')
sns.kdeplot(df_temp[df_temp.gender == 'female'].age_at_death, fill=True, label='female')
plt.legend()
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-25--male-and-female-age-at-death-kdeplot.svg')
plt.close()

sns.violinplot(data=df_temp, x='gender', y='age_at_death')
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-26--male-and-female-age-at-death-violinplot.svg')
plt.close()

# # # increasing life expectancies over time

data = pd.DataFrame(
    {
        'age at death': df_temp.age_at_death,
        'date of birth': df_temp.date_of_birth.dt.year  # Grab only year by dt.year
    }
)
sns.lmplot(data=data, x='date of birth', y='age at death', height=6, aspect=1.5)
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-27--life-expectancies-lmplot.svg')
plt.close()

# # # the Nobel winners diaspora

by_bornin_nat = df[df.born_in.notnull()].groupby(['born_in', 'country']).size().unstack()
# country                             Argentina  Australia  Austria  Belarus  Belgium  Canada  Denmark  France  ...  Netherlands  Russia and Soviet Union  Spain  Sweden  Switzerland  United Kingdom  United States  Yugoslavia
# born_in                                                                                                       ...
# Algeria                                   NaN        NaN      NaN      NaN      NaN     NaN      NaN     2.0  ...          NaN                      NaN    NaN     NaN          NaN             NaN            NaN         NaN
# Argentina                                 NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            NaN         NaN
# Australia                                 NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            1.0         NaN
# Austria                                   NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            3.0         NaN
# Belarus                                   NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      1.0    NaN     NaN          NaN             NaN            NaN         NaN
# Bulgaria                                  NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            NaN         NaN
# Canada                                    NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN           10.0         NaN
# China (People's Republic of China)        NaN        NaN      NaN      NaN      NaN     NaN      NaN     1.0  ...          NaN                      NaN    NaN     NaN          NaN             1.0            1.0         NaN
# Croatia                                   NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            NaN         1.0
# Cyprus                                    NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            NaN         NaN
# Czech Republic                            NaN        NaN      2.0      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            1.0         NaN
# Faroe Islands                             NaN        NaN      NaN      NaN      NaN     NaN      1.0     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            NaN         NaN
# France                                    1.0        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          1.0             NaN            1.0         NaN
# Germany                                   NaN        NaN      1.0      NaN      NaN     2.0      NaN     2.0  ...          NaN                      NaN    NaN     2.0          1.0             4.0           15.0         NaN
# Hungary                                   NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            NaN         NaN
# India                                     NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             3.0            1.0         NaN
# Ireland                                   NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            NaN         NaN
# Israel                                    NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            1.0         NaN
# Italy                                     NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            6.0         NaN
# Japan                                     NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            3.0         NaN
# Latvia                                    NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            NaN         NaN
# Lebanon                                   NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            1.0         NaN
# Luxembourg                                NaN        NaN      NaN      NaN      NaN     NaN      NaN     2.0  ...          NaN                      NaN    NaN     NaN          NaN             NaN            NaN         NaN
# Morocco                                   NaN        NaN      NaN      NaN      NaN     NaN      NaN     1.0  ...          NaN                      NaN    NaN     NaN          NaN             NaN            NaN         NaN
# Netherlands                               NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            1.0         NaN
# New Zealand                               NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            NaN         NaN
# North Macedonia                           NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            NaN         NaN
# Pakistan                                  NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            1.0         NaN
# Peru                                      NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    1.0     NaN          NaN             NaN            NaN         NaN
# Poland                                    NaN        NaN      NaN      NaN      NaN     NaN      NaN     1.0  ...          NaN                      NaN    NaN     NaN          1.0             1.0            6.0         NaN
# Romania                                   NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            2.0         NaN
# Russia and Soviet Union                   NaN        NaN      NaN      NaN      1.0     NaN      NaN     1.0  ...          1.0                      NaN    NaN     NaN          NaN             1.0            2.0         NaN
# Saint Lucia                               NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            NaN         NaN
# South Africa                              NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             2.0            1.0         NaN
# Spain                                     NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            1.0         NaN
# Taiwan (Republic of China)                NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            3.0         NaN
# Tanzania                                  NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            NaN         NaN
# Trinidad and Tobago                       NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             1.0            NaN         NaN
# Turkey                                    NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            NaN         NaN
# Ukraine                                   NaN        NaN      NaN      1.0      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            NaN         NaN
# United Kingdom                            NaN        1.0      NaN      NaN      1.0     2.0      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            2.0         NaN
# United States                             NaN        NaN      NaN      NaN      NaN     NaN      1.0     NaN  ...          NaN                      NaN    NaN     NaN          NaN             2.0            NaN         NaN
# Venezuela                                 NaN        NaN      NaN      NaN      NaN     NaN      NaN     NaN  ...          NaN                      NaN    NaN     NaN          NaN             NaN            1.0         NaN
#
# [43 rows x 21 columns]

by_bornin_nat.index.name = 'Born in'
by_bornin_nat.columns.name = 'Moved to'
plt.figure(figsize=(12, 12))
ax = sns.heatmap(by_bornin_nat, vmin=0, vmax=8, cmap="crest", linewidth=0.5)
ax.set_title('The Nobel Winners Diaspora')
plt.tight_layout()
plt.savefig('pandas-data-exploring-figures/figure-28--winners-diaspora-heatmap.svg')
plt.close()

df[(df.born_in == 'Germany') & (df.country == 'United Kingdom')][['date_of_birth', 'category']]
#                   date_of_birth                category
# name
# Ernst Boris Chain    1906-06-19  Physiology or Medicine
# Hans Adolf Krebs     1900-08-25  Physiology or Medicine
# Max Born             1882-12-11                 Physics
# Bernard Katz         1911-03-26  Physiology or Medicine
