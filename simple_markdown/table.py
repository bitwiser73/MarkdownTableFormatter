import re


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    from_string = dict((key, value) for key, value in enums.items())
    from_int = dict((value, key) for key, value in enums.items())
    enums['from_string'] = from_string
    enums['from_int'] = from_int
    return type('Enum', (), enums)

Justify = enum("LEFT", "CENTER", "RIGHT")


def find_all(text):
    tables = []
    offset = 0
    while True:
        pattern = ".*\|.*\r?\n[\s\t]*\|?(?::?-+:?\|:?-+:?\|?)+(?:\r?\n.*\|.*)+"
        grp = re.search(pattern, text[offset:], re.MULTILINE)
        if grp is None:
            return tables
        tables.append((grp.start() + offset, grp.end() + offset))
        offset = offset + grp.end()
    return tables


def format(raw_table, margin=1, padding=0, default_justify=Justify.LEFT):
    rows = raw_table.splitlines()
    # normalize markdown table, add missing leading/trailing '|'
    for idx, row in enumerate(rows):
        if re.match("^[\s\t]*\|", row) is None:
            rows[idx] = "|" + rows[idx]
        if re.match(".*\|[\s\t]*\r?\n?$", row) is None:
            rows[idx] = rows[idx] + "|"

    matrix = [[col.strip() for col in parse_row_to_cols(row)] for row in rows]

    # ensure there's same column number for each row or add missings
    col_cnt = max([len(row) for row in matrix])
    matrix[:] = \
        [r if len(r) == col_cnt else r + [""]*(col_cnt-len(r)) for r in matrix]

    # merge the multiple "-" of the 2nd line
    matrix[1] = [re.sub("[-. ]+","-", col) for col in matrix[1]]

    # determine each cell text size
    text_width = [[len(col) for col in row] for row in matrix]
    # determine column width (including space padding/margin)
    col_width = [max(size) + margin*2 + padding for size in zip(*text_width)]

    # get each column justification or apply default
    justify = []
    for col_idx, col in enumerate(matrix[1]):
        if col.startswith(":") and col.endswith(":"):
            justify.append(Justify.CENTER)
        elif col.endswith(":"):
            justify.append(Justify.RIGHT)
        elif col.startswith(":"):
            justify.append(Justify.LEFT)
        else:
            justify.append(default_justify)

    # construct a clean markdown table without separation row
    table = []
    for row_idx, row in enumerate(matrix):
        line = ["|"]
        # separation row is processed after
        if row_idx == 1:
            continue
        for col_idx, col in enumerate(row):
            if justify[col_idx] == Justify.CENTER:
                div, mod = divmod(col_width[col_idx] - len(col), 2)
                text = " "*div + col + " "*(div+mod)
                line.append(text + "|")
                continue
            if justify[col_idx] == Justify.RIGHT:
                text = col.rjust(col_width[col_idx] - margin*2)
            elif justify[col_idx] == Justify.LEFT:
                text = col.ljust(col_width[col_idx] - margin*2)
            line.append(" "*margin + text + " "*margin + "|")
        table.append("".join(line))

    # construct separation row
    sep_row = []
    for col_idx, col in enumerate(matrix[1]):
        line = list("-" * (col_width[col_idx]))
        if justify[col_idx] == Justify.LEFT:
            line[0] = ":"
        elif justify[col_idx] == Justify.CENTER:
            line[0] = ":"
            line[-1] = ":"
        elif justify[col_idx] == Justify.RIGHT:
            line[-1] = ":"
        sep_row.append("".join(line))

    table.insert(1, "|" + "|".join(sep_row) + "|")
    return "\n".join(table)


def parse_row_to_cols(row):
    state = []
    cols = []
    col = ""
    i = -1
    while (i + 1 < len(row)):
        # consume next char
        i += 1
        ch = row[i]
        col += ch

        if len(state) == 0:
            # global state
            if ch == '|':
                cols.append(col[:-1] if len(col) > 0 else '')
                col = ''
            elif ch == '\\':
                state.append('\\')
            elif ch == '`':
                state.append('`')
            elif ch == '*' and peek(i, row) == '*':
                # consume next char
                i += 1
                ch = row[i]
                col += ch

                state.append('**')
            elif ch == '*':
                state.append('*')
            else:
                pass
        elif state[-1] == '\\':
            # escaped
            state.pop()
        elif state[-1] == '`':
            # code
            if ch == '`':
                state.pop()
            elif ch == '\\':
                state.append('\\')
            else:
                pass
        elif state[-1] == '*':
            # emphasis *
            if ch == '\\':
                state.append('\\')
            elif ch == '`':
                state.append('`')
            elif ch == '*':
                if peek(i, row) == '*' and '**' not in state:
                    # consume next char
                    i += 1
                    ch = row[i]
                    col += ch

                    state.append('**')
                else:
                    state.pop()
        elif state[-1] == '**':
            # emphasis **
            if ch == '\\':
                state.append('\\')
            elif ch == '`':
                state.append('`')
            elif ch == '*':
                if peek(i, row) == '*':
                    # consume next char
                    i += 1
                    ch = row[i]
                    col += ch

                    state.pop()
                elif '*' not in state:
                    state.append('*')
                else:
                    pass
        else:
            pass
    return cols[1:]


def peek(pos, text, deep=1):
    if pos + deep < len(text):
        return text[pos + deep]
    else:
        None
