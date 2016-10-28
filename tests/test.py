#!/usr/bin/env python3
# -*- coding: utf-8 -*_

import os
import sys

sys.path.append(os.path.realpath('..'))
import simple_markdown.table

#import unittest

raw_table = """\
|   Tables        | Are       | Cool  |
|-------------|:-------------|:-----:|
 | col 1 is      | left-aligned | $1600 |  
col 2 is      ||   $12  
  | zebra stripes | are neat      |    $1 |  
|| |$hello
|    $2 |"""

expected_table = """\
| Tables        | Are          | Cool   |
|:--------------|:-------------|:------:|
| col 1 is      | left-aligned | $1600  |
| col 2 is      |              | $12    |
| zebra stripes | are neat     | $1     |
|               |              | $hello |
| $2            |              |        |"""

print(raw_table)
table = simple_markdown.table.format(raw_table)
print(table)

if table == expected_table:
    print("OK")

junk_tables = """
|   Tables        | Are       | Cool #1  |
|-------------|:-------------:|:-----|
 | col 3 is      | right-aligned | $1600 |  
col 2 is      ||   $12  
  | zebra stripes|are neat|    $1 |  
|| |$hello
|    $2 |

hellobar
fooworld
and junk

|   Tables        | Are       | Cool #2 |
|-------------|:-------------:|:-----|
 | col 3 is      | right-aligned | $1600 |  
col 2 is      ||   $12  
  | zebra stripes | are neat                                |    $1 |  
|| |$hello
|    $2 |

junk junk junk
and some | to test
if it's still working ||||||
is it?
"""

offsets = simple_markdown.table.find_all(junk_tables)
for offset in offsets:
    table = simple_markdown.table.format(junk_tables[offset[0]:offset[1]])
    print(table + "\n")
