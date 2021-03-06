# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff CLI record formatter."""
__author__ = """Lance Finn Helsten <lanhel@zeff.ai>"""
__copyright__ = """Copyright © 2019, Ziff, Inc. — All Rights Reserved"""
__license__ = """
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


import sys
import itertools
import textwrap


def format_record_restructuredtext(
    record,
    out=sys.stdout,
    structured_sort=lambda k: k.name,
    unstructured_sort=lambda k: k.group_by if k.group_by is not None else "",
):
    """Convert a record to a reStructuedText document.

    :param record: Record to format.

    :param out: A file type object to write the record in. Default `stdout`.

    :param structured_sort: A function of one argument that will be
        used to sort the structured data items. The default is to
        sort by the name of the item.

    :param unstructured_sort: A function of one argument that will be
        used to sort the unstructured data items. The default is to
        sort on `group_by`.
    """

    def print_table_header(columns):
        for name, width in columns:
            print(f"+-{'-'*width}-", end="", file=out)
        print("+", file=out)

        for name, width in columns:
            print(f"| {name}{' '*(width-len(name))} ", end="", file=out)
        print("|", file=out)

        for name, width in columns:
            print(f"+={'='*width}=", end="", file=out)
        print("+", file=out)

    def print_table_entry(data, columns):
        cstrs = [(str(d), w) for d, (n, w) in zip(data, columns)]
        cstrs = [textwrap.wrap(s, w) for s, w in cstrs]
        for rstrs in itertools.zip_longest(*cstrs):
            for index, vstr in enumerate(rstrs):
                width = columns[index][1]
                if vstr is None:
                    print(f"| {' '*width} ", end="", file=out)
                else:
                    print(f"| {vstr:<{width}} ", end="", file=out)
            print("|", file=out)
        for _, width in columns:
            print(f"+-{'-'*width}-", end="", file=out)
        print("+", file=out)

    def print_structured_item_table(record):
        columns = compute_column_widths(
            record.structured_data,
            ["name", "data_type", "target", "value"],
            [16, 8, 6, 32],
        )
        print_table_header(columns)

        data_items = list(record.structured_data)
        data_items.sort(key=structured_sort)
        for sdi in data_items:
            data = [sdi.name, sdi.data_type.name, sdi.target.name, sdi.value]
            print_table_entry(data, columns)

    def print_unstructured_item_table(record):
        columns = compute_column_widths(
            record.unstructured_data,
            ["file_type", "group_by", "data_uri", "accessible"],
            [8, 8, 8, 16],
        )
        print_table_header(columns)

        data_items = list(record.unstructured_data)
        data_items.sort(key=unstructured_sort)
        for udi in data_items:
            data = [udi.file_type, udi.group_by, udi.data_uri, udi.accessible]
            print_table_entry(data, columns)

    def compute_column_widths(items, names, mins):
        widths = list(mins)
        for item in items:
            for index, width in enumerate(widths):
                value = getattr(item, names[index])
                width = max(len(str(value)), width)
                widths[index] = width
        if sum(widths) + len(widths) * 3 + 1 > 132:
            reduce = sum(widths) + len(widths) * 3 + 1 - 132
            maxcol = max(widths)
            widths[widths.index(maxcol)] = maxcol - reduce
        return list(zip(names, widths))

    print("=" * len(str(record)))
    print(record)
    print("=" * len(str(record)))

    print()
    print("Structured Data")
    print("===============")
    print_structured_item_table(record)

    print(file=out)
    print("Unstructured Data", file=out)
    print("=================", file=out)
    print_unstructured_item_table(record)
