import sublime
import sublime_plugin

import logging

from . import simple_markdown as markdown
from .simple_markdown import table

log = logging.getLogger(__name__)

class MarkdownTableFormatterFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        logging.basicConfig(level=logging.DEBUG)
        for region in self.view.sel():
            text = self.view.substr(region)
            # get all tables positions as (start,end) list
            positions = markdown.table.find_all(text)
            offset = 0
            for start, end in positions:
                raw_table = text[start:end]
                log.debug("table found:\n" + raw_table)
                table = markdown.table.format(raw_table)
                log.debug("formatted output:\n" + table)

                # replace the raw table with the formetted one
                table_region = sublime.Region(region.begin() + start + offset,
                                              region.begin() + end + offset)
                self.view.replace(edit, table_region, table)

                # as table length will likely change, an offset is required to
                # keep the modified region consistent
                offset = offset + len(table) - (end - start)
