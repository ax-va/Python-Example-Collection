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

d = parser.parse('2021-11-16T22:55:48.738Z')
# datetime.datetime(2021, 11, 16, 22, 55, 48, 738000, tzinfo=tzutc())
