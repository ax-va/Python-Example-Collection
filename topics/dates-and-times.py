"""
Examples:

2021-09-23              Date (Python/C format code '%Y-%m-%d')
2021-09-23T16:32:35Z    UTC (Z after time) date and time ('T%H:%M:%S')
2021-09-23T16:32+02:00  Positive two-hour (+02:00) offset from UTC (e.g., Central European Time)
"""
from datetime import datetime
from dateutil import parser

d = datetime.now()
d.isoformat()
# '2023-10-04T09:14:27.797305'
# Microseconds are lost.

# Make datetime.datetime using datetime.datetime.strptime

d = datetime.strptime('2022-01-25 01:59:59.999', '%Y-%m-%d %H:%M:%S.%f')
# datetime.datetime(2022, 1, 25, 1, 59, 59, 999000)

d = datetime.strptime('20220125', '%Y%m%d')
# datetime.datetime(2022, 1, 25, 0, 0)

d = datetime.strptime('2022012', '%Y%m%d')
# datetime.datetime(2022, 1, 2, 0, 0)

# d = datetime.strptime('202201', '%Y%m%d')
# # ValueError: time data '202201' does not match format '%Y%m%d'

# d = datetime.strptime('2022012501', '%Y%m%d')
# # ValueError: unconverted data remains: 01

# Make datetime.datetime using dateutil.parser.parse

d = parser.parse('2022-01-25T22:55:44.738Z')
# datetime.datetime(2022, 1, 25, 22, 55, 44, 738000, tzinfo=tzutc())

