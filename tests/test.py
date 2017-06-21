#!/usr/bin/env python3
# -*- coding: utf-8 -*_

import unittest

import testpath
import simple_markdown.table
import simple_markdown.table as Table


def print_all_tables(raw_table, table, expected_table):
    print("\n" + "=" * 80)
    print("\nraw table:\n")
    print(raw_table)
    print("\nformatted table:\n")
    print(table)
    print("\nexpected table:\n")
    print(expected_table)


def print_tables(table, expected_table):
    print("\n" + "=" * 80)
    print("\nformatted table:\n")
    print(table)
    print("\nexpected table:\n")
    print(expected_table)

class test_markdown_table(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
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
|  Tables           |      Are         |             Cool  |
|:------------------|:----------------:|------------------:|
|  col 1 is         |  left-aligned    |            $1600  |
|  col 2 is         |    centered      |              $12  |
|  zebra stripes    |                  |    are neat   $1  |
|                   |                  |           $hello  |
|  $2               |                  |                   |"""

        table = Table.format(raw_table, margin=2, padding=2,
                             default_justify=Table.Justify.CENTER)
        print_tables(table, expected_table_2_2)
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
        print_tables(table, expected_table_0_0)
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
        print_tables(table, expected_small)
        self.assertEqual(table, expected_small)


    def test_fullwidth(self):
        raw_table = """\
|   Tables        | Are       | Cool  |
:-------------|:-------------:|:-----|
 | col 1 is      | left-aligned                                    | $1600 |
col 2 is      | centered|   $12
  | zebra stripes|       |            are neat   $1 |
|| |$hello
|    $2 |
| 业务方向      | 线人  |线人2       |
| 运营后台 - 销售 | 雪、鹏、丽 | 雪、
| 智能商业部     | 瑞mixed         |  雪、"""

        expected_table_0_0_cjk = """\
|Ｔａｂｌｅｓ　　　　　　　|　　　　Ａｒｅ　　　　　|Ｃｏｏｌ　　　　　　　　　|
|:-------------------------|:----------------------:|:-------------------------|
|ｃｏｌ　１　ｉｓ　　　　　|ｌｅｆｔ－ａｌｉｇｎｅｄ|＄１６００　　　　　　　　|
|ｃｏｌ　２　ｉｓ　　　　　|　　ｃｅｎｔｅｒｅｄ　　|＄１２　　　　　　　　　　|
|ｚｅｂｒａ　ｓｔｒｉｐｅｓ|　　　　　　　　　　　　|ａｒｅ　ｎｅａｔ　　　＄１|
|　　　　　　　　　　　　　|　　　　　　　　　　　　|＄ｈｅｌｌｏ　　　　　　　|
|＄２　　　　　　　　　　　|　　　　　　　　　　　　|　　　　　　　　　　　　　|
|业务方向　　　　　　　　　|　　　　　线人　　　　　|线人２　　　　　　　　　　|
|运营后台　－　销售　　　　|　　　雪、鹏、丽　　　　|雪、　　　　　　　　　　　|
|智能商业部　　　　　　　　|　　　瑞ｍｉｘｅｄ　　　|雪、　　　　　　　　　　　|"""

        table = Table.format(raw_table, margin=0, padding=0,
            default_justify=Table.Justify.CENTER, convert_cjk=True)
        print_tables(table, expected_table_0_0_cjk)
        self.assertEqual(table, expected_table_0_0_cjk)

        expected_table_2_2_cjk = """\
|  Ｔａｂｌｅｓ　　　　　　　    |  　　　　Ａｒｅ　　　　　    |  Ｃｏｏｌ　　　　　　　　　    |
|:-------------------------------|:----------------------------:|:-------------------------------|
|  ｃｏｌ　１　ｉｓ　　　　　    |  ｌｅｆｔ－ａｌｉｇｎｅｄ    |  ＄１６００　　　　　　　　    |
|  ｃｏｌ　２　ｉｓ　　　　　    |  　　ｃｅｎｔｅｒｅｄ　　    |  ＄１２　　　　　　　　　　    |
|  ｚｅｂｒａ　ｓｔｒｉｐｅｓ    |  　　　　　　　　　　　　    |  ａｒｅ　ｎｅａｔ　　　＄１    |
|  　　　　　　　　　　　　　    |  　　　　　　　　　　　　    |  ＄ｈｅｌｌｏ　　　　　　　    |
|  ＄２　　　　　　　　　　　    |  　　　　　　　　　　　　    |  　　　　　　　　　　　　　    |
|  业务方向　　　　　　　　　    |  　　　　　线人　　　　　    |  线人２　　　　　　　　　　    |
|  运营后台　－　销售　　　　    |  　　　雪、鹏、丽　　　　    |  雪、　　　　　　　　　　　    |
|  智能商业部　　　　　　　　    |  　　　瑞ｍｉｘｅｄ　　　    |  雪、　　　　　　　　　　　    |"""

        table = Table.format(raw_table, margin=2, padding=2,
            default_justify=Table.Justify.CENTER, convert_cjk=True)
        print_tables(table, expected_table_2_2_cjk)
        self.assertEqual(table, expected_table_2_2_cjk)

        expected_table_0_0 = """\
|Tables         |    Are     |Cool         |
|:--------------|:----------:|:------------|
|col 1 is       |left-aligned|$1600        |
|col 2 is       |  centered  |$12          |
|zebra stripes  |            |are neat   $1|
|               |            |$hello       |
|$2             |            |             |
|业务方向       |    线人    |线人2        |
|运营后台 - 销售| 雪、鹏、丽 |雪、         |
|智能商业部     |  瑞mixed   |雪、         |"""
        
        table = Table.format(raw_table, margin=0, padding=0,
            default_justify=Table.Justify.CENTER, convert_cjk=False)
        print_tables(table, expected_table_0_0)
        self.assertEqual(table, expected_table_0_0)

        expected_table_2_2 = """\
|  Tables             |      Are         |  Cool             |
|:--------------------|:----------------:|:------------------|
|  col 1 is           |  left-aligned    |  $1600            |
|  col 2 is           |    centered      |  $12              |
|  zebra stripes      |                  |  are neat   $1    |
|                     |                  |  $hello           |
|  $2                 |                  |                   |
|  业务方向           |      线人        |  线人2            |
|  运营后台 - 销售    |   雪、鹏、丽     |  雪、             |
|  智能商业部         |    瑞mixed       |  雪、             |"""

        table = Table.format(raw_table, margin=2, padding=2,
            default_justify=Table.Justify.CENTER, convert_cjk=False)
        print_tables(table, expected_table_2_2)
        self.assertEqual(table, expected_table_2_2)


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
