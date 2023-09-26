"""
This example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://oreil.ly/9zZvt.
"""

import csv
from datetime import datetime

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

# Get column names for CSV
cols = nobel_winners[0].keys()
# Sort the column names in alphabetical order
cols = sorted(cols)

# Write CSV from the list of dictionaries
with open('csv-files/nobel_winners.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=cols)
    # Write the header separately
    writer.writeheader()
    for w in nobel_winners:
        # Write each dictionaly from the list to a CSV row
        writer.writerow(w)

# Numbers are read in string form.
# Read each CSV row by row in a list.
with open('csv-files/nobel_winners.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
# ['category', 'gender', 'name', 'nationality', 'year']
# ['Physics', 'male', 'Albert Einstein', 'German and Swiss', '1921']
# ['Physics', 'male', 'Paul Dirac', 'British', '1933']
# ['Chemistry', 'female', 'Marie Curie', 'Polish', '1911']

# Read CSV in a list of dictionaries
with open('csv-files/nobel_winners.csv') as f:
    reader = csv.DictReader(f)
    nobel_winners = list(reader)
print(type(nobel_winners[0]))
# <class 'dict'>
print(nobel_winners)
# [{'category': 'Physics', 'gender': 'male', 'name': 'Albert Einstein', 'nationality': 'German and Swiss', 'year': '1921'}, {'category': 'Physics', 'gender': 'male', 'name': 'Paul Dirac', 'nationality': 'British', 'year': '1933'}, {'category': 'Chemistry', 'gender': 'female', 'name': 'Marie Curie', 'nationality': 'Polish', 'year': '1911'}]

# # Cast year in int
# for w in nobel_winners:
#     w['year'] = int(w['year'])

# Better: cast year in datetime
for w in nobel_winners:
    w['year'] = datetime.strptime(w['year'], '%Y')
