from functools import reduce

# Sum out over the list
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
odds = filter(lambda x: x % 2, nums)
odds_sq = map(lambda x: x * x, odds)
total = reduce(lambda x, y: x + y, odds_sq)
print(total)
# 165
