# coding: utf-8

from core import pywikibot
from core import mwparserfromhell as mwparser
import core.scripts.category as category


class RemoveEntryError(Exception):
    def __init__(self, desc):
        self.desc = desc


class RemoveEntry:
    def __init__(self, template: mwparser.wikicode.Template):
        if template.has("category"):
            self.category = template.get("category")
        else:
            raise RemoveEntryError("Lacks category to be removed.")
        if template.has("summary"):
            self.summary = template.get("summary")
        else:
            raise RemoveEntryError("Lacks summary the bot uses.")
        if template.has("admin_name"):
            self.admin_name = template.get("admin_name")
        else:
            raise RemoveEntryError("Lacks admin_name who requested the removal.")

    def remove_setup(self):
        # setup parameters with which category.py is called.
        pass


class TargetList:
    def __init__(self, page: pywikibot.Page):
        self.page = page
        self.entries = list()

    def parse(self):
        text = self.page.text()
        parsed = mwparser.parse(text)
        entries = list()
        for template in parsed.filter_templates():
            if template.name.matches("User:Akasenbot/Entry"):
                entries.append(template)

        temp_entries = list()
        for entry in entries:
            try:
                temp_entries.append(RemoveEntry(entry))
            except RemoveEntryError as e:
                print(e.desc)

        self.entries = temp_entries


def main(site):
    target_list = TargetList(pywikibot.Page(site, "User:Akasenbot/category_removal_requests"))
    target_list.parse()
    entries = target_list.entries
    for entry in entries:
        entry.remove_setup()

if __name__ == "__main__":
    site = pywikibot.Site()
    main(site)

