# LineSample

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

# Installation

Currently, this module is only available for Python 3. You can install it 
with `pip install linesample`.

# Usage

To sample half of all lines from an input file `foo.txt`, run

```
linesample -f0.5 foo.txt
```

To sample up to 100 lines from `bar.txt`, run
```
linesample -n100 bar.txt
```

You must use one of the forms above. Specifying neither or both options will
result in an error.

By default, the utility uses the system time as the seed for its 
pseudorandom number generator. You can choose your own seed using a form 
like this:

```
linesample -s42 -n100 baz.txt
```

For reference, the usage string is as follows:

```
usage: ['linesample.py', '-h'] [-h] [-s SEED] [-f FRACTION | -n NUMBER] infile

positional arguments:
  infile                input file

optional arguments:
  -h, --help            show this help message and exit
  -s SEED, --seed SEED  seed for random number generator
  -f FRACTION, --fraction FRACTION
                        fraction of lines to select
  -n NUMBER, --number NUMBER
                        number of lines to select
```

# License

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
