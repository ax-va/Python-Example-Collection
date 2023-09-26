"""
This example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023.
"""
import datetime
import json

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

# Write JSON
with open('json-files/nobel_winners.json', 'w') as f:
    json.dump(nobel_winners, f)

# Read JSON in str
print(type(open('json-files/nobel_winners.json').read()))
# <class 'str'>
print(open('json-files/nobel_winners.json').read())
# [{"category": "Physics", "name": "Albert Einstein", "nationality": "German and Swiss", "gender": "male", "year": 1921}, {"category": "Physics", "name": "Paul Dirac", "nationality": "British", "gender": "male", "year": 1933}, {"category": "Chemistry", "name": "Marie Curie", "nationality": "Polish", "gender": "female", "year": 1911}]

# Read JSON in a list of dictionaries
with open('json-files/nobel_winners.json') as f:
    nobel_winners = json.load(f)

print(type(nobel_winners))
# <class 'list'>
print(nobel_winners)
# [{'category': 'Physics', 'name': 'Albert Einstein', 'nationality': 'German and Swiss', 'gender': 'male', 'year': 1921}, {'category': 'Physics', 'name': 'Paul Dirac', 'nationality': 'British', 'gender': 'male', 'year': 1933}, {'category': 'Chemistry', 'name': 'Marie Curie', 'nationality': 'Polish', 'gender': 'female', 'year': 1911}]

# The integer type of the year column is preserved.

# # # Deal with dates and times

# json.dumps(datetime.datetime.now())
# # TypeError: Object of type datetime is not JSON serializable


# Create a customer JSON encoder as a subclass of json.JSONEncoder
# to dump the datetime types into an ISO-format string
class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
            return obj.isoformat()  # e.g., '2021-11-16T16:41:14.650802'
        else:
            return json.JSONEncoder.default(self, obj)

    def dumps(self, obj):
        # Use the cls argument to set a custom date encoder
        return json.dumps(obj, cls=self.__class__)


print(JSONDateTimeEncoder().dumps({'datetime': datetime.datetime.now()}))
# {"datetime": "2023-09-26T08:19:22.582581"}

print(JSONDateTimeEncoder().dumps({'date': datetime.date(year=2023, month=9, day=26)}))
# {"date": "2023-09-26"}

print(JSONDateTimeEncoder().dumps({'time': datetime.time(hour=1, minute=2, second=3, microsecond=456)}))
# {"date": "01:02:03.000456"}

# The Python module 'dateutil' has a parser that will parse most dates and times.

time_str = '2021/01/01 12:32:11'
dt = datetime.datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S')
print(repr(dt))
# datetime.datetime(2021, 1, 1, 12, 32, 11)

## dt = datetime.datetime.strptime('1/2/2021 12:32:11', '%Y/%m/%d %H:%M:%S')
# ValueError: time data '1/2/2021 12:32:11' does not match format '%Y/%m/%d %H:%M:%S'
