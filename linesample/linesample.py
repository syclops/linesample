"""
Utility to randomly sample lines from an input file.

This module implements a command-line utility that randomly samples lines
from an input file. It is possible to sample lines by the probability of
each line being selected or by giving an overall number of lines. In either
case, the lines can be sampled with a single pass through the file, and the
ordering of lines in the original file is preserved. For reproducibility,
this module also supports seeding of the pseudorandom number generator used.

Only modules from the Python 3 standard library are used in this code. Type
hints (from the typing module), which at the time of writing is still a
provisional API, are also used.

This module is distributed under the MIT License, whose text is listed both
in the LICENSE file provided with this package and immediately below.

Copyright (c) 2019 Steve Matsumoto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import argparse
import fileinput
import math
import random
import sys
from typing import (
    List,
    Optional,
)


def sample_by_fraction(infile: str, fraction: float) -> None:
    """
    Print a fraction of the lines in an input file.

    Args:
        infile: the path to the input file.
        fraction: the probability with which to print each file, assumed to
            be between 0.0 and 1.0.

    Returns:
        None.
    """
    for line in fileinput.input(infile):
        if random.random() < fraction:
            print(line.strip())


def sample_by_number(infile: str, number: int) -> None:
    """
    Print a number of randomly-selected lines from an input file.

    Print up to a given number of randomly-selected lines from an input
    file, preserving the order of lines as they appear in the input. If the
    desired number of lines is greater than the number of lines in the file,
    the entire input is printed.

    Args:
        infile: the path to the input file.
        number: the maximum number of lines from the file to randomly print,
            assumed to be a positive integer.

    Returns:
        None.
    """
    lines_read = 0
    selected_lines = []

    # Use reservoir sampling to select a number of lines from the input.
    for line in fileinput.input(infile):
        lines_read += 1
        if len(selected_lines) < number:
            selected_lines.append(line)
            continue
        index = math.floor(random.random() * lines_read)
        if index < number - 1:
            # Preserve order by deleting a specified line and appending the
            # new line to the buffer.
            del selected_lines[index]
            selected_lines.append(line)

    for line in selected_lines:
        print(line.strip())


def sample_lines(infile: str, seed: Optional[int] = None,
                 fraction: Optional[float] = None,
                 number: Optional[int] = None) -> None:
    """
    Print a random sample of lines from a file.

    Given an input file, a fraction (between 0 and 1), and an optional seed for
    the random number generator, print a random sample of the lines in the
    input file. This function does not guarantee that exactly `fraction` of the
    lines in the input file `infile` will be printed because it uses a random
    number generator to determine whether to print each line independently.

    Args:
        `infile` (str): the path to the input file.
        `seed` (int): the seed for the random number generator. The default
                      is `None`, which will cause the RNG to use system time.
        `fraction` (float): the probability with which to print each line.
        `number` (int): a number of lines to return.

    Returns:
        None.

    Raises:
        ValueError: the given fraction was not between 0 and 1.
    """
    if fraction is None and number is None:
        raise ValueError('Either fraction or number must be given.')
    random.seed(seed)
    if fraction is not None:
        if fraction < 0.0 or fraction > 1.0:
            raise ValueError('Sampling fraction must be between 0 and 1')
        sample_by_fraction(infile, fraction)
    elif number is not None:
        if number < 1:
            raise ValueError('Number of lines must be a positive integer.')
        sample_by_number(infile, number)
    else:
        raise ValueError('Only one of fraction or number may be given.')


def parse(args: List[str] = sys.argv) -> argparse.Namespace:
    """
    Parse arguments to the main function.

    Args:
        `args` (list): a list of arguments (`sys.argv` by default).

    Returns:
        An `argparse.Namespace` instance containing the attributes resulting
        from the parsed arguments. If neither a fraction of lines or a
        number of lines is specified, the program will print an error and
        usage message and exit with status code 2.
    """
    parser = argparse.ArgumentParser(args)
    parser.add_argument('infile', default='-', help='input file')
    parser.add_argument('-s', '--seed', default=None, type=int,
                        help='seed for random number generator')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--fraction', type=float,
                       help='fraction of lines to select')
    group.add_argument('-n', '--number', type=int,
                       help='number of lines to select')

    args = parser.parse_args()

    # Check if neither fraction nor number has been set after parsing.
    # Checking whether both were set is not necessary because we defined a
    # mutually exclusive group above.
    if args.fraction is None and args.number is None:
        parser.error('A value for exactly one of -f/--fraction or '
                     '-n/--number is required.')

    return args


def main() -> None:
    args = parse()
    sample_lines(args.infile, args.seed, args.fraction, args.number)


if __name__ == '__main__':
    main()
