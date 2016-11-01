#!/usr/bin/env python3
# -*- coding: utf-8 -*_

import unittest

import testpath
import simple_markdown.table
import simple_markdown.table as Table


class test_markdown_table(unittest.TestCase):
    def setUp(self):
        pass

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
"""
        offsets = simple_markdown.table.find_all(junk_tables)
        self.assertEqual(len(offsets), 3)

if __name__ == '__main__':
    unittest.main()
