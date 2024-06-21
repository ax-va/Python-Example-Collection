"""
This example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data",
 Kyran Dale, O'Reilly, 2023.
"""
# For writting or reading CSV, use the "csv" package

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

# Write in CSV
with open('csv-files/nobel_winners.csv', 'w') as f:
    # At first, write the column names for CSV
    f.write(','.join(cols) + '\n')
    for nobel_winner in nobel_winners:
        row = [str(nobel_winner[col]) for col in cols]
        f.write(','.join(row) + '\n')

# Read the file
with open('csv-files/nobel_winners.csv') as f:
    for line in f.readlines():
        print(line, end="")
# category,gender,name,nationality,year
# Physics,male,Albert Einstein,German and Swiss,1921
# Physics,male,Paul Dirac,British,1933
# Chemistry,female,Marie Curie,Polish,1911
