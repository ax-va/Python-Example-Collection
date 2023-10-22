"""
Lightweight scrapping by Beautiful Soup and lxml

Scrapping the table in https://en.wikipedia.org/wiki/List_of_Nobel_laureates

The DOM of the Wiki table:

<table class="wikitable sortable jquery-tablesorter">
    <thead>
        <tr>
            <th class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">
                Year
            </th>
            <th width="17%" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">
                <a href="/wiki/List_of_Nobel_laureates_in_Physics" title="List of Nobel laureates in Physics">
                    Physics
                </a>
            </th>
            <th width="18%" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">
                <a href="/wiki/List_of_Nobel_laureates_in_Chemistry" title="List of Nobel laureates in Chemistry">
                    Chemistry
                </a>
            </th>
            <th width="17%" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">
                <a href="/wiki/List_of_Nobel_laureates_in_Physiology_or_Medicine" title="List of Nobel laureates in Physiology or Medicine">
                    Physiology
                    <br>
                    or Medicine
                </a>
            </th>
            <th width="16%" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">
                <a href="/wiki/List_of_Nobel_laureates_in_Literature" title="List of Nobel laureates in Literature">
                    Literature
                </a>
            </th>
            <th width="16%" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">
                <a href="/wiki/List_of_Nobel_Peace_Prize_laureates" title="List of Nobel Peace Prize laureates">
                    Peace
                </a>
            </th>
            <th width="15%" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">
                <a href="/wiki/List_of_Nobel_laureates_in_Economics" class="mw-redirect" title="List of Nobel laureates in Economics">
                    Economics
                </a>
                <br>
                (The Sveriges Riksbank Prize)
                <sup id="cite_ref-13" class="reference">
                    <a href="#cite_note-13">
                        [13]
                    </a>
                </sup>
                <sup id="cite_ref-14" class="reference">
                    <a href="#cite_note-14">
                        [a]
                    </a>
                </sup>
            </th>
        </tr>
    </thead>
    <tbody>
        <tr id="1901">
            <td align="center">
                1901
            </td>
            <td>
                <span data-sort-value="Röntgen, Wilhelm">
                    <span class="vcard">
                        <span class="fn">
                            <a href="/wiki/Wilhelm_R%C3%B6ntgen" title="Wilhelm Röntgen">
                                Wilhelm Röntgen
                            </a>
                        </span>
                    </span>
                </span>
            </td>
            <td>
                <span data-sort-value="Hoff, Jacobus Henricus van 't">
                    <span class="vcard">
                        <span class="fn">
                            <a href="/wiki/Jacobus_Henricus_van_%27t_Hoff" title="Jacobus Henricus van 't Hoff">
                                Jacobus Henricus van 't Hoff
                            </a>
                        </span>
                    </span>
                </span>
            </td>
            <td>
                <span data-sort-value="von Behring, Emil">
                    <span class="vcard">
                        <span class="fn">
                            <a href="/wiki/Emil_von_Behring" title="Emil von Behring">
                                Emil von Behring
                            </a>
                        </span>
                    </span>
                </span>
            </td>
            <td>
                <span data-sort-value="Prudhomme, Sully">
                    <span class="vcard">
                        <span class="fn">
                            <a href="/wiki/Sully_Prudhomme" title="Sully Prudhomme">
                                Sully Prudhomme
                            </a>
                        </span>
                    </span>
                </span>
            </td>
            <td>
                <span data-sort-value="Dunant, Henry">
                    <span class="vcard">
                        <span class="fn">
                            <a href="/wiki/Henry_Dunant" title="Henry Dunant">
                                Henry Dunant
                            </a>
                        </span>
                    </span>
                </span>
                ;
                <br>
                <span data-sort-value="Passy, Frédéric">
                    <span class="vcard">
                        <span class="fn">
                            <a href="/wiki/Fr%C3%A9d%C3%A9ric_Passy" title="Frédéric Passy">
                                Frédéric Passy
                            </a>
                        </span>
                    </span>
                </span>
            </td>
            <td rowspan="68" align="center" bgcolor="eeeeee">
                —
            </td>
        </tr>
...
"""
from typing import List, Dict

import bs4
import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://en.wikipedia.org'
# Wikipedia will reject our request unless we add a 'User-Agent' attribute to our http header
HEADERS = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(
    url=BASE_URL+"/wiki/List_of_Nobel_laureates",
    headers=HEADERS,
)
response.content
# ...
# <table class="wikitable sortable">\n\n<tbody><tr>\n<th>Year\n</th>\n<th width="17%">...
# ...

# WARNING: The response content distinguishes from the HTML source

soup = BeautifulSoup(response.content, "lxml")
type(soup.find('table', {'class': 'wikitable sortable'}))
# bs4.element.Tag
str(soup.find('table', {'class': 'wikitable sortable'}))[:100]
# '<table class="wikitable sortable">\n<tbody><tr>\n<th>Year\n</th>\n<th width="17%"><a href="/wiki/List_of'

# Change the order of our CSS classes
soup.find('table', {'class': 'sortable wikitable'}) is None
#  True

# Use CSS selector
soup.select('table.sortable.wikitable')
type(soup.select('table.sortable.wikitable'))
# bs4.element.ResultSet
len(soup.select('table.sortable.wikitable'))
# 1
str(soup.select('table.sortable.wikitable')[0])[:100]
# '<table class="wikitable sortable">\n<tbody><tr>\n<th>Year\n</th>\n<th width="17%"><a href="/wiki/List_of'

# Find only the first tag that matches the selector
table = soup.select_one('table.sortable.wikitable')
type(table)
# bs4.element.Tag
len(table.select('th'))
# 14
# shorthand
len(table('th'))
# 14


def get_column_titles(table: bs4.element.Tag) -> List[Dict]:
    """
    Gets the Nobel categories from the table header
    """
    columns = []
    for th in table.select_one('tr').select('th'):
        link = th.select_one('a')
        # Store the category name and any Wikipedia link it has
        if link:
            columns.append(
                {
                    'name': link.text,
                    'href': link.attrs['href'],
                }
            )
        else:
            columns.append(
                {
                    'name': th.text,
                    'href': None,
                }
            )
    return columns


get_column_titles(table)
# [{'name': 'Year\n', 'href': None},
#  {'name': 'Physics', 'href': '/wiki/List_of_Nobel_laureates_in_Physics'},
#  {'name': 'Chemistry', 'href': '/wiki/List_of_Nobel_laureates_in_Chemistry'},
#  {'name': 'Physiologyor Medicine',
#   'href': '/wiki/List_of_Nobel_laureates_in_Physiology_or_Medicine'},
#  {'name': 'Literature', 'href': '/wiki/List_of_Nobel_laureates_in_Literature'},
#  {'name': 'Peace', 'href': '/wiki/List_of_Nobel_Peace_Prize_laureates'},
#  {'name': 'Economics', 'href': '/wiki/List_of_Nobel_laureates_in_Economics'}]


def get_nobel_winners(table: bs4.element.Tag) -> List[Dict]:
    column_titles = get_column_titles(table)
    column_titles_after_year = column_titles[1:]
    winners = []
    for row in table.select('tr')[1:-1]:  # without the first and last rows in the response.content
        year = int(row.select_one('td').text)  # only year
        for i, td in enumerate(row.select('td')[1:]):  # without year
            for winner in td.select('a'):
                href = winner.attrs['href']
                if not href.startswith('#endnote'):
                    winners.append(
                        {
                            'year': year,
                            'category': column_titles_after_year[i]['name'],
                            'name': winner.text,
                            'link': winner.attrs['href'],
                        }
                    )
    return winners


winners = get_nobel_winners(table)
# the first three winners
winners[:3]
# [{'year': 1901,
#   'category': 'Physics',
#   'name': 'Wilhelm Röntgen',
#   'link': '/wiki/Wilhelm_R%C3%B6ntgen'},
#  {'year': 1901,
#   'category': 'Chemistry',
#   'name': "Jacobus Henricus van 't Hoff",
#   'link': '/wiki/Jacobus_Henricus_van_%27t_Hoff'},
#  {'year': 1901,
#   'category': 'Physiologyor Medicine',
#   'name': 'Emil von Behring',
#   'link': '/wiki/Emil_von_Behring'}]
# the last three winners
winners[-3:]
# [{'year': 2023,
#   'category': 'Literature',
#   'name': 'Jon Fosse',
#   'link': '/wiki/Jon_Fosse'},
#  {'year': 2023,
#   'category': 'Peace',
#   'name': 'Narges Mohammadi',
#   'link': '/wiki/Narges_Mohammadi'},
#  {'year': 2023,
#   'category': 'Economics',
#   'name': 'Claudia Goldin',
#   'link': '/wiki/Claudia_Goldin'}]
