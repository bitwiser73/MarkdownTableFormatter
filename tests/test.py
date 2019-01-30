#!/usr/bin/env python3
# -*- coding: utf-8 -*_

import unittest

import testpath
import simple_markdown.table
import simple_markdown.table as Table


class test_markdown_table(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_format(self):
        raw_table = """\
|   Tables        | Are       | Cool  |
|:-------------|-------------|-----:|
 | col 1 is      | left-aligned                                    | $1600 |
col 2 is      | centered|   $12
  | zebra stripes |       | are neat   $1 |
|| |$hello
|    $2 |"""

        expected_table_2_2 = """\
|  Tables           |       Are        |             Cool  |
|:------------------|:----------------:|------------------:|
|  col 1 is         |   left-aligned   |            $1600  |
|  col 2 is         |     centered     |              $12  |
|  zebra stripes    |                  |    are neat   $1  |
|                   |                  |           $hello  |
|  $2               |                  |                   |"""

        table = Table.format(raw_table, margin=2, padding=2,
                             default_justify=Table.Justify.CENTER)
        self.assertEqual(table, expected_table_2_2)

        expected_table_0_0 = """\
|Tables       |Are         |         Cool|
|:------------|:-----------|------------:|
|col 1 is     |left-aligned|        $1600|
|col 2 is     |centered    |          $12|
|zebra stripes|            |are neat   $1|
|             |            |       $hello|
|$2           |            |             |"""

        table = Table.format(raw_table, margin=0, padding=0)
        self.assertEqual(table, expected_table_0_0)

        # test table with minimal form (#7)
        small = """\
foo|bar
--------|:---
123|4567777789
a|"""

        expected_small = """\
| foo | bar        |
|:----|:-----------|
| 123 | 4567777789 |
| a   |            |"""

        table = Table.format(small, margin=1, padding=0)
        self.assertEqual(table, expected_small)

        code_with_pipes = """\
param | regex | description
------|-------|-----------|
foo|`/cat|dog|dino/`|blabla|
bar|just escaped pipe >> \\| <<|Lorem ipsum dolor sit amet, consectetur adipisicing elit. Distinctio, id.|
foo bar | ** `a|d` ** | `\\`` |"""

        expected_code_with_pipes = """\
| param   | regex                      | description                                                               |
|:--------|:---------------------------|:--------------------------------------------------------------------------|
| foo     | `/cat|dog|dino/`           | blabla                                                                    |
| bar     | just escaped pipe >> \\| << | Lorem ipsum dolor sit amet, consectetur adipisicing elit. Distinctio, id. |
| foo bar | ** `a|d` **                | `\\``                                                                      |"""

        table = Table.format(code_with_pipes, margin=1, padding=0)
        self.assertEqual(table, expected_code_with_pipes)

    def test_find_all(self):
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

| ok | more | col | and more | col
|----|-----|--|----|---|--|-|-|-|
|ok | still good

junk junk junk
and some | to test |
if it's still working ||||||
is it?

param | regex | description
------|-------|-----------|
foo|`/cat|dog|dino/`|blabla|
bar|just escaped pipe >> \| <<|Lorem ipsum dolor sit amet, consectetur adipisicing elit. Distinctio, id.|
foo bar | ** `a|d` ** | `\\`` |
"""
        offsets = simple_markdown.table.find_all(junk_tables)
        self.assertEqual(len(offsets), 4)

    def test_parse_row_to_cols(self):
        self.assertEqual(Table.parse_row_to_cols('|simple string, nothing else|'), ['simple string, nothing else'])
        self.assertEqual(Table.parse_row_to_cols('|a|b|c|'), ['a', 'b', 'c'])
        self.assertEqual(Table.parse_row_to_cols('|foo bar | `asd` | `\`` |'), ['foo bar ', ' `asd` ', ' `\`` '])
        self.assertEqual(Table.parse_row_to_cols('|foo bar | `a|d` | `\`` |'), ['foo bar ', ' `a|d` ', ' `\`` '])
        self.assertEqual(Table.parse_row_to_cols('|foo bar | ** `a|d` ** | `\\`` |'), ['foo bar ', ' ** `a|d` ** ', ' `\\`` '])
        self.assertEqual(Table.parse_row_to_cols('|`foo`|`bar`|'), ['`foo`', '`bar`'])


if __name__ == '__main__':
    unittest.main()
