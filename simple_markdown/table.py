import re

def find_all(text):
    tables = []
    offset = 0
    while True:
        group = re.search(".*\|.*\n[\s\t]*\|?(?::?[-]+:?\|)+(\n.*\|.*)+",
                          text[offset:], re.MULTILINE)
        if group is None:
            return tables
        tables.append((group.start() + offset, group.end() + offset))
        offset = offset + group.end()
    return tables

def format(raw_table):
    rows = raw_table.splitlines()
    # normalize markdown table, add missing leading/trailing '|'
    for idx, row in enumerate(rows):
        if re.match("^[\s\t]*\|", row) is None:
            rows[idx] = "|" + rows[idx]
        if re.match(".*\|[\s\t]*\n?$", row) is None:
            rows[idx] = rows[idx] + "|"

    matrix = [[col.strip() for col in row.split("|")] for row in rows]

    # remove first and last empties column
    matrix[:] = [row[1:] for row in matrix]
    matrix[:] = [row[:-1] for row in matrix]

    # ensure there's same column number for each row or add missings
    cols = max([len(row) for row in matrix])
    matrix[:] = \
      [row if len(row) == cols else row+[""]*(cols-len(row)) for row in matrix]

    # merge the multiple "-" of the 2nd line
    matrix[1] = [re.sub("[- ]+","-", col) for col in matrix[1]]

    # determine each column size
    widths = [[len(col) for col in row] for row in matrix]
    max_widths = [max(item) for item in zip(*widths)]

    # construct a clean markdown table without separation row
    table = []
    for row_idx, row in enumerate(matrix):
        line = ["|"]
        # keep separation row for later...
        if row_idx == 1:
            continue
        for col_idx, col in enumerate(row):
            line.append(" " + col.ljust(max_widths[col_idx]) + " |")
        table.append("".join(line))

    # construct separation row
    sep_row = []
    for col_idx, col in enumerate(matrix[1]):
        line = list("-" * (max_widths[col_idx] + 2))
        if col.startswith(":"):
            line[0] = ":"
        if col.endswith(":"):
            line[-1] = ":"
        else:
            line[0] = ":"
        sep_row.append("".join(line))
    table.insert(1, "|" + "|".join(sep_row) + "|")
    return "\n".join(table)

