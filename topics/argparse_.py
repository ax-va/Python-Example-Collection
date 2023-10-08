"""
The argparse package:
https://docs.python.org/3/library/argparse.html
"""
from typing import Sequence

DEFAULT_ARG1 = ("a", "b")
DEFAULT_ARG2 = 0
DEFAULT_ARG3 = (0, 1, 2)


def foo(
        arg0: str,
        arg1: Sequence[str] = DEFAULT_ARG1,
        arg2: int = DEFAULT_ARG2,
        arg3: Sequence[int] = DEFAULT_ARG3,
) -> None:
    print("Arguments passed to the function:")
    print("arg0:", repr(arg0))
    print("arg1:", repr(arg1))
    print("arg2:", repr(arg2))
    print("arg3:", repr(arg3))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Execution of the foo function",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Add one required argument
    parser.add_argument(
        "arg0",
        type=str,
        help="argument arg0",
    )

    # Add optional arguments
    parser.add_argument(
        "-a", "--arg1",
        nargs="+",
        default=DEFAULT_ARG1,
        type=str,
        help="argument arg1",
    )

    parser.add_argument(
        "-b", "--arg2",
        type=int,
        default=DEFAULT_ARG2,
        choices=[0, 1, 2],
        help="argument arg2",
    )

    parser.add_argument(
        "-c", "--arg3",
        nargs="*",
        default=DEFAULT_ARG3,
        type=int,
        help="argument arg3",
    )

    args = parser.parse_args()
    print("args:", args)
    kwargs = vars(args)
    print("Calling the script with arguments:")
    for key, value in kwargs.items():
        print(key, "=", repr(value))
    foo(**kwargs)

# python argparse_.py -h
# usage: argparse_.py [-h] [-a ARG1 [ARG1 ...]] [-b {0,1,2}] [-c [ARG3 ...]] arg0
#
# Execution of the foo function
#
# positional arguments:
#   arg0                  argument arg0
#
# options:
#   -h, --help            show this help message and exit
#   -a ARG1 [ARG1 ...], --arg1 ARG1 [ARG1 ...]
#                         argument arg1 (default: ('a', 'b'))
#   -b {0,1,2}, --arg2 {0,1,2}
#                         argument arg2 (default: 0)
#   -c [ARG3 ...], --arg3 [ARG3 ...]
#                         argument arg3 (default: (0, 1, 2))

# python argparse_.py "hello"
# args: Namespace(arg0='hello', arg1=('a', 'b'), arg2=0, arg3=(0, 1, 2))
# Calling the script with arguments:
# arg0 = 'hello'
# arg1 = ('a', 'b')
# arg2 = 0
# arg3 = (0, 1, 2)
# Arguments passed to the function:
# arg0: 'hello'
# arg1: ('a', 'b')
# arg2: 0
# arg3: (0, 1, 2)

# python argparse_.py "hello" -a "hello1" "hello2" "hello3"
# args: Namespace(arg0='hello', arg1=['hello1', 'hello2', 'hello3'], arg2=0, arg3=(0, 1, 2))
# Calling the script with arguments:
# arg0 = 'hello'
# arg1 = ['hello1', 'hello2', 'hello3']
# arg2 = 0
# arg3 = (0, 1, 2)
# Arguments passed to the function:
# arg0: 'hello'
# arg1: ['hello1', 'hello2', 'hello3']
# arg2: 0
# arg3: (0, 1, 2)

# python argparse_.py "hello" -a "hello1" "hello2" "hello3" -b 15
# usage: argparse_.py [-h] [-a ARG1 [ARG1 ...]] [-b {0,1,2}] [-c ARG3 [ARG3 ...]] arg0
# argparse_.py: error: argument -b/--arg2: invalid choice: 15 (choose from 0, 1, 2)

# python argparse_.py "hello" -a "hello1" "hello2" "hello3" -b 1
# args: Namespace(arg0='hello', arg1=['hello1', 'hello2', 'hello3'], arg2=1, arg3=(0, 1, 2))
# Calling the script with arguments:
# arg0 = 'hello'
# arg1 = ['hello1', 'hello2', 'hello3']
# arg2 = 1
# arg3 = (0, 1, 2)
# Arguments passed to the function:
# arg0: 'hello'
# arg1: ['hello1', 'hello2', 'hello3']
# arg2: 1
# arg3: (0, 1, 2)

# python argparse_.py "hello" -a "hello1" "hello2" "hello3" -b 1 --arg3 1 10 100
# args: Namespace(arg0='hello', arg1=['hello1', 'hello2', 'hello3'], arg2=1, arg3=[1, 10, 100])
# Calling the script with arguments:
# arg0 = 'hello'
# arg1 = ['hello1', 'hello2', 'hello3']
# arg2 = 1
# arg3 = [1, 10, 100]
# Arguments passed to the function:
# arg0: 'hello'
# arg1: ['hello1', 'hello2', 'hello3']
# arg2: 1
# arg3: [1, 10, 100]

# python argparse_.py "hello" -a "hello1" "hello2" "hello3" -b 1 -c
# args: Namespace(arg0='hello', arg1=['hello1', 'hello2', 'hello3'], arg2=1, arg3=[])
# Calling the script with arguments:
# arg0 = 'hello'
# arg1 = ['hello1', 'hello2', 'hello3']
# arg2 = 1
# arg3 = []
# Arguments passed to the function:
# arg0: 'hello'
# arg1: ['hello1', 'hello2', 'hello3']
# arg2: 1
# arg3: []
