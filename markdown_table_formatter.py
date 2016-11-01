# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

import logging

from . import simple_markdown as markdown
from .simple_markdown import table

log = logging.getLogger(__name__)


class MarkdownTableFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit, format_all=False):
        logging.basicConfig(level=logging.DEBUG)
        settings = \
            sublime.load_settings("MarkdownTableFormatter.sublime-settings")
        verbose = settings.get("verbose")
        margin = settings.get("margin")
        padding = settings.get("padding")
        justify = settings.get("default_justification")
        justify = markdown.table.Justify.from_string[justify]

        if verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

        # format selected regions or all file with no selection
        has_selection = len(self.view.sel()) and self.view.sel()[0].size()
        if not format_all and has_selection:
            regions = self.view.sel()
        else:
            regions = [sublime.Region(0, self.view.size())]

        table_new_regions = []
        for region in regions:
            text = self.view.substr(region)
            # get all tables positions as (start,end) list
            positions = markdown.table.find_all(text)
            offset = 0
            for start, end in positions:
                prev_table = text[start:end]
                log.debug("table found:\n" + prev_table)
                new_table = markdown.table.format(prev_table, margin, padding,
                                                  justify)
                log.debug("formatted output:\n" + new_table)

                # absolute original table position after some insertion/removal
                table_prev_begin = region.begin() + start + offset
                table_prev_end = region.begin() + end + offset
                table_prev_region = \
                    sublime.Region(table_prev_begin, table_prev_end)

                # future table position after some insertion/removal
                table_new_begin = table_prev_begin
                table_new_end = \
                    region.begin() + start + offset + len(new_table)
                table_new_region = \
                    sublime.Region(table_new_begin, table_new_end)

                self.view.replace(edit, table_prev_region, new_table)
                # stack new regions to update selection
                table_new_regions.append(table_new_region)

                # as table length will likely change after being formatted an
                # offset is required to keep positions consistent
                offset = offset + len(new_table) - len(prev_table)

        if table_new_regions and not format_all:
            had_multiple_regions = has_selection and len(self.view.sel()) > 1
            self.view.sel().clear()

            # I don't like having to hit 'esc' to get only one cursor back
            # after having formatted more than one table using one selection
            if had_multiple_regions or len(table_new_regions) == 1:
                log.debug("MULTIPLE REGION")
                self.view.sel().add_all(table_new_regions)
            else:
                cursor = sublime.Region(table_new_regions[0].a)
                self.view.sel().add(cursor)


class MarkdownTableFormatterListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        # restrict to markdown files
        if view.score_selector(0, "text.html.markdown") == 0:
            return

        settings = \
            sublime.load_settings("MarkdownTableFormatter.sublime-settings")
        if not settings.get("autoformat_on_save"):
            return
        view.run_command("markdown_table_format", {"format_all": True})
