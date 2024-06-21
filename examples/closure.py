def get_counter(inc):
    count = 0

    def add():
        nonlocal count
        count += inc
        return count

    return add


count = get_counter(2)
print(count())
# 2
print(count())
# 4
print(count())
# 6
