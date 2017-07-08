#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import table


def parse_args():
    parser = argparse.ArgumentParser(description="Format markdown tables")

    # TODO:  --in-place[=SUFFIX] => makes backup if SUFFIX supplied
    parser.add_argument("-i", "--in-place", action="store_true",
                        help="edit files in place")
    parser.add_argument("-m", "--margin", type=int, default=1,
                        help="set margin")
    parser.add_argument("-p", "--padding", type=int, default=0,
                        help="set padding")
    parser.add_argument("-j", "--justify", choices=["left", "center", "right"],
                        default="left", help="set default justification")
    parser.add_argument("-c", "--convert-cjk", action="store_true",
                        help="Convert all characters to CJK if any is found")
    parser.add_argument("-e", "--encoding", default="utf-8",
                        help="set encoding")
    parser.add_argument("input_file", nargs="+", help="input file to format")
    return parser.parse_args()


def pretty_format(raw_content, margin, padding, default_justify, convert_cjk):
    pretty_content = raw_content

    raw_offsets = table.find_all(raw_content)
    pretty_offset = 0
    for raw_start, raw_end in raw_offsets:
        raw_table = raw_content[raw_start:raw_end]
        pretty_table = table.format(raw_table, margin, padding, default_justify,
                                    convert_cjk)

        # as table length will likely change after being formatted an
        # offset is required to keep positions consistent
        cut_start = raw_start + pretty_offset
        cut_end = cut_start + len(raw_table)
        pretty_content = pretty_content[:cut_start] + pretty_table + \
            pretty_content[cut_end:]
        
        pretty_offset = pretty_offset + len(pretty_table) - len(raw_table)

    return pretty_content


def main():
    args = parse_args()

    justify = table.Justify.from_string[args.justify.upper()]

    for file in args.input_file:
        with open(file, "rt", encoding=args.encoding) as f_in:
            raw_content = f_in.read()
        pretty_content = pretty_format(raw_content, args.margin, args.padding,
                                       justify, args.convert_cjk)

        if args.in_place:
            with open(file, "wt", encoding=args.encoding) as f_out:
                f_out.write(pretty_content)
            continue
        else:
            print(pretty_content)


if __name__ == "__main__":
    main()
