from functools import reduce

# Sum out over the list
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
odds = filter(lambda x: x % 2, nums)
odds_sq = map(lambda x: x * x, odds)
# Makes the iterator of odds_sq empty
# print(list(odds_sq))
# # [1, 9, 25, 49, 81]
total = reduce(lambda x_im1, x_i: x_im1 + x_i, odds_sq)
print(total)
# 165
