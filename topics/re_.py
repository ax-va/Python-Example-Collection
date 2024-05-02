"""
This example of regular expressions is based on:
- "Python How-To: 63 Techniques to Improve Your Python Code", Yong Cui, Manning Publications Co., 2023;
- https://docs.python.org/3/howto/regex.html.

Test Python regexes:
http://www.pyregex.com/
"""
import re

# # # regular expressions - regex (Python 3.11)

# There are two approaches: the OOP one and the functional one.

# # # - the OOP approach

# Create a pattern
regex = re.compile(r"do")  # Compile the pattern only once and cache it

# attribute
regex.pattern
# 'do'

regex.search("do homework")
# <re.Match object; span=(0, 2), match='do'>

regex.findall("don't do that")
# ['do', 'do']

# # # - the functional approach

re.search(pattern=r"do", string="do homework")  # Compile the pattern every time without caching
# <re.Match object; span=(0, 2), match='do'>

re.findall(pattern=r"do", string="don't do that")
#  ['do', 'do']

task_pattern = re.compile("\\\\task")
texts = ["\task", "\\task", "\\\task", "\\\\task"]
for text in texts:
    print(f"Match {text!r}: {task_pattern.match(text)}")
# Match '\task': None
# Match '\\task': <re.Match object; span=(0, 5), match='\\task'>
# Match '\\\task': None
# Match '\\\\task': None

task_pattern_r = re.compile(r"\\task")
texts = ["\task", "\\task", "\\\task", "\\\\task"]
for text in texts:
    print(f"Match {text!r}: {task_pattern_r.match(text)}")
# Match '\task': None
# Match '\\task': <re.Match object; span=(0, 5), match='\\task'>
# Match '\\\task': None
# Match '\\\\task': None

# # # boundary anchors

# ^hi           starts with "hi"
# task$         ends with "task"
# ^hi task$     starts and ends with "hi task"

re.search(r"^hi", "hi Python")
# <re.Match object; span=(0, 2), match='hi'>

re.search(r"task$", "do the task")
# <re.Match object; span=(7, 11), match='task'>

re.search(r"task$", "do the task but not another task")
# <re.Match object; span=(28, 32), match='task'>

re.search(r"^hi task$", "hi task")
# <re.Match object; span=(0, 7), match='hi task'>

re.search(r"^hi task$", "hi Python task")
# None

# # # quantifiers

# hi?           "h" followed by zero or one "i"
# hi*           "h" followed by zero or more "i"
# hi+           "h" followed by one or more "i"
# hi{3}         "h" followed by "iii"
# hi{1,3}       "h" followed by "i", "ii", or "iii"
# hi{2,}        "h" followed by 2 or more "i"

# The pattern matches the longest sequence whenever possible.
# The additional "?" suffix results in the shortest sequence.

test_patterns = [r"hi?", r"hi*", r"hi+", r"hi{3}", r"hi{1,3}", r"hi{2,}",r"hi??", r"hi*?", r"hi+?", r"hi{2,}?"]
test_string = "h hi hii hiii hiiii hiiiii ih hih hihi"
for pattern in test_patterns:
    print(f"{pattern:<9} -> {re.findall(pattern, test_string)}")
# hi?       -> ['h', 'hi', 'hi', 'hi', 'hi', 'hi', 'h', 'hi', 'h', 'hi', 'hi']
# hi*       -> ['h', 'hi', 'hii', 'hiii', 'hiiii', 'hiiiii', 'h', 'hi', 'h', 'hi', 'hi']
# hi+       -> ['hi', 'hii', 'hiii', 'hiiii', 'hiiiii', 'hi', 'hi', 'hi']
# hi{3}     -> ['hiii', 'hiii', 'hiii']
# hi{1,3}   -> ['hi', 'hii', 'hiii', 'hiii', 'hiii', 'hi', 'hi', 'hi']
# hi{2,}    -> ['hii', 'hiii', 'hiiii', 'hiiiii']
# hi??      -> ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h']
# hi*?      -> ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h']
# hi+?      -> ['hi', 'hi', 'hi', 'hi', 'hi', 'hi', 'hi', 'hi']
# hi{2,}?   -> ['hii', 'hii', 'hii', 'hii']

# # # character classes and sets

# \d            any decimal digit
# \D            any character that is not a decimal digit
# \s            any whitespace, including space, \t, \n, \r, \f, \v
# \S            any character that isn't a whitespace
# \w            any word character, means alphanumeric plus underscores
# \W            any character that is not a word character
# \b            word boundary position
# .             any character except a newline
# []            a set of characters that are OR-coupled
# \.            a dot

# - individual characters: [abcxyz]
# - a range of characters: [a-z], [A-Z]
# - combined different ranges of characters: [a-dw-z]

# The escape character \ for \. is redundant in []

some_email = "ax-va.@gmail.com"
print(re.search(r"[\w\-.]+", some_email))
# <re.Match object; span=(0, 6), match='ax-va.'>
print(re.findall(r"[\w\-.]+", some_email))
# ['ax-va.', 'gmail.com']

# Here in [], we use . for a dot instead of \.
print(re.search(r"[.]+", some_email))
# <re.Match object; span=(5, 6), match='.'>
print(re.findall(r"[.]+", some_email))
# ['.', '.']

patterns = ["\d", "\D", "\s", "\S", "\w", "\W", ".", "[lmn]"]
test_text = "#1$2m_ M\t ä \n lm ml"
for pattern in patterns:
    print(f"{pattern: <9} -> {re.findall(pattern, test_text)}")
# \d        -> ['1', '2']
# \D        -> ['#', '$', 'm', '_', ' ', 'M', '\t', ' ', 'ä', ' ', '\n', ' ', 'l', 'm', ' ', 'm', 'l']
# \s        -> [' ', '\t', ' ', ' ', '\n', ' ', ' ']
# \S        -> ['#', '1', '$', '2', 'm', '_', 'M', 'ä', 'l', 'm', 'm', 'l']
# \w        -> ['1', '2', 'm', '_', 'M', 'ä', 'l', 'm', 'm', 'l']
# \W        -> ['#', '$', ' ', '\t', ' ', ' ', '\n', ' ', ' ']
# .         -> ['#', '1', '$', '2', 'm', '_', ' ', 'M', '\t', ' ', 'ä', ' ', ' ', 'l', 'm', ' ', 'm', 'l']
# [lmn]     -> ['m', 'l', 'm', 'm', 'l']

# # # or, groups, and complements

# a|b           "a" or "b"
# (abc)         "abc" as a group of characters to extract only it
# [^a]          any character other than "a"

re.findall(r"a|b", "a c d d b ab")  # Replace with [ab] for cleaner code
# ['a', 'b', 'a', 'b']

# equivalent
re.findall(r"[ab]", "a c d d b ab")
# ['a', 'b', 'a', 'b']

re.findall(r"a|b", "c d d b")  # Replace with [ab] for cleaner code
#  ['b']

re.findall(r"(a|b)", "c d d b")  # Replace with ([ab]) for cleaner code
# ['b']

# equivalent
re.findall(r"[ab]", "c d d b")
# ['b']

re.findall(r"(abc)", "ab bc abc ac .abcd")
# ['abc', 'abc']

re.findall(r"(abc)", "ab bc ac")
#  []

re.findall(r"[^a]", "abcde")
# ['b', 'c', 'd', 'e']

# Patterns [^(...)] and [^...^...]

re.findall(r"[^(ab)]", "abcde")
# ['c', 'd', 'e']

re.findall(r"[^a^b]", "abcde")
# ['c', 'd', 'e']

re.findall(r"[^(ae)]", "abcde")
# ['b', 'c', 'd']

re.findall(r"[^a^e]", "abcde")
# ['b', 'c', 'd']

# Find words by using word boundary position \b
pattern = re.compile(r"\b" + re.escape(r"word") + r"\b")
text = "word word wordword wordwordword word"
pattern.findall(text)
# ['word', 'word', 'word']

# The difference between re.search() and re.match():
# 1) re.search() searches for the first match anywhere in the string
# 2) re.match() searches for matches from the beginning of a string

re.search(r"(\w\d)", "xyza2b1c3dd")
# <re.Match object; span=(3, 5), match='a2'>

re.match(r"(\w\d)", "xyza2b1c3dd")
# None

re.search(r"(\w\w)", "xyza2b1c3dd")
# <re.Match object; span=(0, 2), match='xy'>

re.match(r"(\w\w)", "xyza2b1c3dd")
# <re.Match object; span=(0, 2), match='xy'>

re.search(r"(\w\d)", "y1xyza2b1c3dd")
# <re.Match object; span=(0, 2), match='y1'>

re.match(r"(\w\d)", "y1xyza2b1c3dd")
# <re.Match object; span=(0, 2), match='y1'>

re.search(r"(abcd)+", "xyza2b1c3dd")
# None

re.match(r"(abcd)+", "xyza2b1c3dd")
# None

# # # Match.group(), Match.span(), Match.start(), Match.end()

match = re.search(r"(\w\d)+", "xyza2b1c3dd")
# <re.Match object; span=(3, 9), match='a2b1c3'>

match.group()
# 'a2b1c3'

match.span()
# (3, 9)

match.start()
# 3

match.end()
# 9

# # # multiple groups and spans

match = re.match(r"(\w+), (\w+)", "Homework, urgent; today")
# <re.Match object; span=(0, 16), match='Homework, urgent'>

match.groups()
# ('Homework', 'urgent')

match.group(0)
# 'Homework, urgent'

match.group(1)
# 'Homework'

match.group(2)
# 'urgent'

match.span(0)
# (0, 16)

match.span(1)
# (0, 8)

match.span(2)
# (10, 16)

# # # Summarize common regex methods

# search                returns a Match if a match is found anywhere in the string

re.search(r"\d+", "ab12xy")
# <re.Match object; span=(2, 4), match='12'>

re.search(r"\d+", "abxy")
# None

# match                 returns a Match only if a match is found at the string’s beginning

re.match(r"\d+", "ab12xy")
# None

re.match(r"\d+", "12abxy")
# <re.Match object; span=(0, 2), match='12'>

# findall               returns a list of strings that match the pattern

re.findall(r"h[ie]\w", "hi hey hello")
# ['hey', 'hel']

# When the pattern has multiple groups, the item is a tuple.

re.findall(r"(h|H)(i|e)", "Hey hello")  # Replace with ([hH]) and ([ie]) for cleaner code
#  [('H', 'e'), ('h', 'e')]

# finditer              returns an iterator that yields the Match objects

type(re.finditer(r"(h|H)(i|e)", "hi Hey hello"))  # Replace with ([hH]) and ([ie]) for cleaner code
# callable_iterator

# split                 splits the string by the pattern

re.split(r"\d+", 'a1b2c3d4e')
# ['a', 'b', 'c', 'd', 'e']

# sub                   creates a string by replacing the matched with the replacement

re.sub(r"\D", "-", '123,456_789')
# '123-456-789'
