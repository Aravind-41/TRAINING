"""Simple division example with robust exception handling and CLI support.

Usage:
  python exceptionhandling3.py 10 2
  python exceptionhandling3.py   # prompts for input
"""

from __future__ import annotations
import argparse
import sys


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b


def main(argv: list[str] | None = None) -> int:
    argv = list(argv) if argv is not None else None
    parser = argparse.ArgumentParser(description="Divide two numbers with error handling")
    parser.add_argument('a', nargs='?', type=float, help='numerator')
    parser.add_argument('b', nargs='?', type=float, help='denominator')
    args = parser.parse_args(argv)

    if args.a is None or args.b is None:
        try:
            args.a = float(input('Enter numerator: '))
            args.b = float(input('Enter denominator: '))
        except ValueError:
            print('Invalid numeric input')
            return 2

    try:
        result = divide(args.a, args.b)
    except ZeroDivisionError:
        print('Error: denominator is zero')
        return 1
    except Exception as exc:
        print(f'Unexpected error: {exc}')
        return 3
    else:
        print(result)
        print('Execution successful')
        return 0


if __name__ == '__main__':
    raise SystemExit(main())