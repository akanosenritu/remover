# coding: utf-8
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/core')

from core import pywikibot as pwbot
import core.mwparserfromhell as mwparser
import core.scripts.category as category


class RemoveEntryError(Exception):
    def __init__(self, desc):
        self.desc = desc


class RemoveEntry:
    def __init__(self, template: mwparser.wikicode.Template):
        self.template = template
        self.parameters = None
        if template.has("from_category"):
            self.from_category = template.get("from_category")
        else:
            raise RemoveEntryError("Lacks category to be removed.")
        if template.has("summary"):
            self.summary = template.get("summary")
        else:
            raise RemoveEntryError("Lacks summary the bot uses.")
        if template.has("admin"):
            self.admin_name = template.get("admin")
        else:
            raise RemoveEntryError("Lacks admin_name who requested the removal.")

    def remove_setup(self):
        # setup parameters with which category.py is called.
        parameters = ["remove", "-from:"+str(self.template.get("from_category").value), "-summary:"+str(self.template.get("summary").value)]
        self.parameters = parameters

    def call_category_py(self):
        category.main(self.parameters)


class TargetList:
    def __init__(self, page: pwbot.Page):
        self.page = page
        self.entries = list()

    def parse(self):
        text = self.page.text
        parsed = mwparser.parse(text)
        entries = list()
        for template in parsed.filter_templates():
            if template.name.matches("User:Akasenbot/remover/category/entry"):
                entries.append(template)

        temp_entries = list()
        for entry in entries:
            try:
                temp_entries.append(RemoveEntry(entry))
            except RemoveEntryError as e:
                print(e.desc)

        self.entries = temp_entries


def main(site):
    target_list = TargetList(pwbot.Page(site, "User:Akasenbot/remover/category"))
    target_list.parse()
    entries = target_list.entries
    for entry in entries:
        entry.remove_setup()
        print(entry.parameters)

if __name__ == "__main__":
    site = pwbot.Site()
    main(site)

