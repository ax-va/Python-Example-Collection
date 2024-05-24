from collections import Counter, defaultdict, OrderedDict

items = ['A', 'B', 'C', 'D', 'E', 'F', 'A', 'B', 'A']
counter = Counter(items)
print(counter)
# Counter({'A': 3, 'B': 2, 'C': 1, 'D': 1, 'E': 1, 'F': 1})

counter['C'] -= 1
print(counter)
# Counter({'A': 3, 'B': 2, 'D': 1, 'E': 1, 'F': 1, 'C': 0})

# Set the dictionary default to an integer, with value 0 by default
d = defaultdict(int)

for item in items:
    d[item] += 1
print(d)
# defaultdict(<class 'int'>, {'A': 3, 'B': 2, 'C': 1, 'D': 1, 'E': 1, 'F': 1})
print(d["G"])
# 0

# key, value: i[1] for value
ord_dict = OrderedDict(sorted(d.items(), key=lambda i: i[1]))
print(ord_dict)
# OrderedDict([('G', 0), ('C', 1), ('D', 1), ('E', 1), ('F', 1), ('B', 2), ('A', 3)])
