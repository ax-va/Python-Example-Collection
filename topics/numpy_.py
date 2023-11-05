"""
This NumPy example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://numpy.org/doc/stable/reference/arrays.ndarray.html;
- https://numpy.org/doc/stable/reference/routines.math.html.
"""
import numpy as np

a = np.array([1, 2, 3, 4, 5, 6, 7, 8])
# array([1, 2, 3, 4, 5, 6, 7, 8])

a.ndim, a.shape, a.dtype
# (1, (8,), dtype('int64'))

a = a.reshape([2, 4])
# array([[1, 2, 3, 4],
#        [5, 6, 7, 8]])

a.ndim, a.shape, a.dtype
# (2, (2, 4), dtype('int64'))

a = a.reshape([2, 2, 2])
# array([[[1, 2],
#         [3, 4]],
#
#        [[5, 6],
#         [7, 8]]])

a.ndim, a.shape, a.dtype
# (3, (2, 2, 2), dtype('int64'))

x = np.array([[1, 2, 3], [4, 5, 6]], np.int32)
# array([[1, 2, 3],
#        [4, 5, 6]], dtype=int32)

x.shape
# (2, 3)

x.shape = (6,)
x
# array([1, 2, 3, 4, 5, 6], dtype=int32)

x = x.astype('int64')
# array([1, 2, 3, 4, 5, 6])

x.dtype
# dtype('int64')

# # # creating arrays

a = np.zeros([2,3])
# array([[0., 0., 0.],
#        [0., 0., 0.]])

a.dtype
# dtype('float64')

np.ones([2, 3])
# array([[1., 1., 1.],
#        [1., 1., 1.]])

# Create an uninitialized array
empty_array = np.empty((2, 3))
# array([[1., 1., 1.],
#        [1., 1., 1.]])

# Create an array of random numbers within the range [0, 1)
np.random.random((2, 3))
# array([[0.25631708, 0.24057082, 0.21659182],
#        [0.57630477, 0.31927474, 0.43333808]])

np.linspace(2, 10, 5)  # 5 numbers in range [2, 10]
# array([ 2.,  4.,  6.,  8., 10.])

np.arange(2, 10, 2)  # numbers in range [2, 10) with step of 2
# array([2, 4, 6, 8])

# # # array indexing and slicing

a = np.array([1, 2, 3, 4, 5, 6])
# array([1, 2, 3, 4, 5, 6])

a[2]
# 3

a[3:5]  # index of 5 exclusive
# array([4, 5])

# Set to 0 every second item from [0, 4)
a[:4:2] = 0
a
# array([0, 2, 0, 4, 5, 6])

# Get a reversed array
a[::-1]
# array([6, 5, 4, 0, 2, 0])

a
# array([0, 2, 0, 4, 5, 6])

a = np.arange(24, dtype='int32')
a = a.reshape([2, 3, 4])
# array([[[ 0,  1,  2,  3],
#         [ 4,  5,  6,  7],
#         [ 8,  9, 10, 11]],
#
#        [[12, 13, 14, 15],
#         [16, 17, 18, 19],
#         [20, 21, 22, 23]]], dtype=int32)

a[0, :, :]
# array([[ 0,  1,  2,  3],
#        [ 4,  5,  6,  7],
#        [ 8,  9, 10, 11]], dtype=int32)

a[0, :]
# array([[ 0,  1,  2,  3],
#        [ 4,  5,  6,  7],
#        [ 8,  9, 10, 11]], dtype=int32)

np.array_equal(a[0, :, :], a[0, :])
# True

a[0]
# array([[ 0,  1,  2,  3],
#        [ 4,  5,  6,  7],
#        [ 8,  9, 10, 11]], dtype=int32)

np.array_equal(a[0, :], a[0])
# True

np.array_equal(a[..., 0], a[:, :, 0])
# True

a[1]
# array([[12, 13, 14, 15],
#        [16, 17, 18, 19],
#        [20, 21, 22, 23]], dtype=int32)

a[0, 0]
# array([0, 1, 2, 3], dtype=int32)

a[0, 1]
# array([4, 5, 6, 7], dtype=int32)

a[0, :, 1:3]
# array([[ 1,  2],
#        [ 5,  6],
#        [ 9, 10]], dtype=int32)

a[1, 1]
# array([16, 17, 18, 19], dtype=int32)

a[1, 1, :-1]
# array([16, 17, 18], dtype=int32)

# # # a few basic operations

a = np.arange(2, 10, 2)
# array([2, 4, 6, 8])

a + a
# array([ 4,  8, 12, 16])

a + 1
# array([3, 5, 7, 9])

a - 1
# array([1, 3, 5, 7])

a / 2
# array([1., 2., 3., 4.])

a = np.array([45, 65, 76, 32, 99, 22])
# array([45, 65, 76, 32, 99, 22])

a < 50
# array([ True, False, False,  True, False,  True])

a = np.arange(8).reshape((2, 4))
# array([[0, 1, 2, 3],
#        [4, 5, 6, 7]])

a[0]
# array([0, 1, 2, 3])

a[:, 0]
# array([0, 4])

a.sum()
# 28

# Sum out all elements a[:, i] (add all rows)
a.sum(axis=0)
# array([ 4,  6,  8, 10])

# Sum out all elements a[i, :] (add all columns)
a.sum(axis=1)
# array([ 6, 22])

a.min()
# 0

a.min(axis=0)
# array([0, 1, 2, 3])

a.min(axis=1)
# array([0, 4])

a[0, 1] = 100
a
# array([[  0, 100,   2,   3],
#        [  4,   5,   6,   7]])

a.min(axis=0)
# array([0, 5, 2, 3])

a.mean(axis=0)
# array([ 2. , 52.5,  4. ,  5. ])

a.mean(axis=1)
# array([26.25,  5.5 ])

a.std(axis=1)
# array([42.59327999,  1.11803399])


pi = np.pi
a = np.array([pi, pi/2, pi/4, pi/6])
# array([3.14159265, 1.57079633, 0.78539816, 0.52359878])

np.degrees(a)
# array([180.,  90.,  45.,  30.])

sin_a = np.sin(a)
# array([1.22464680e-16, 1.00000000e+00, 7.07106781e-01, 5.00000000e-01])

np.round(sin_a, 6)
# array([0.      , 1.      , 0.707107, 0.5     ])

a = np.arange(8).reshape((2, 4))
# array([[0, 1, 2, 3],
#        [4, 5, 6, 7]])

np.cumsum(a, axis=0)
# array([[ 0,  1,  2,  3],
#        [ 4,  6,  8, 10]])

np.cumsum(a, axis=1)
# array([[ 0,  1,  3,  6],
#        [ 4,  9, 15, 22]])

np.cumsum(a)
# array([ 0,  1,  3,  6, 10, 15, 21, 28])


def moving_average(arr: np.array, n: int = 3) -> np.float64:
    """
    Description by example:
    arr = np.arange(10)
    # array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    csum = np.cumsum(arr)
    # array([ 0,  1,  3,  6, 10, 15, 21, 28, 36, 45])
    csum[4:]
    # array([10, 15, 21, 28, 36, 45])
    csum[:-4]
    array([ 0,  1,  3,  6, 10, 15])
    csum[4:] - csum[:-4]
    # array([10, 14, 18, 22, 26, 30])
    csum[4:] = csum[4:] - csum[:-4]
    csum
    # array([ 0,  1,  3,  6, 10, 14, 18, 22, 26, 30])
    csum / 4
    # array([0.  , 0.25, 0.75, 1.5 , 2.5 , 3.5 , 4.5 , 5.5 , 6.5 , 7.5 ])

    Wikipedia: https://en.wikipedia.org/wiki/Moving_average

    (NumPy has the 'convolve' method.)

    Args:
        arr: NumPy array
        n: moving mean or rolling mean (the size of the moving window)
    Return:
        moving average
    """
    ret = np.cumsum(arr, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


a = np.arange(10)
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
moving_average(a, 4)
# array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5])
