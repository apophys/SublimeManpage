# -*- coding: utf-8 –*–

import threading
import re
from subprocess import Popen, PIPE

import sublime
import sublime_plugin

WHATIS_RE = "^(?P<func>\w+[^\(])\s*\((?P<sect>\dp?m?)\)\s+-\s+(?P<desc>.*)$"
# FIXME: section part allows 2m which is not acceptable

class ManpageCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.platform() not in ["osx", "linux"]:
            sublime.error_message("Manpage: Platform %s is not supported."
                                  % sublime.platform())
            return

        self.window.show_input_panel("Type function name:", "",
                                     self.on_done, None, None)

    def on_done(self, line):
        ManpageApiCall(self.window, line).start()


class ManpageApiCall(threading.Thread):
    def __init__(self, window, func):
        self.window = window
        self.req_function = func
        self.function_list = list()
        self.settings = sublime.load_settings("Preferences.sublime-settings")
        threading.Thread.__init__(self)

    def run(self):
        def show_panel():
            if not self.req_function:
                return

            func_list = self._get_function_list()
            if not func_list:
                return

            if len(func_list) is not 1:
                self.window.show_quick_panel(func_list, self.on_done)
            else:
                self.on_done(0)

        sublime.set_timeout(show_panel, 10)

    def on_done(self, picked):
        if picked == -1:
            return

        manpage, title = self._call_man(self.function_list[picked])
        self._render_manpage(manpage, title)

    def _get_function_list(self):
        def split_whatis(lines):
            splited = list()

            for line in lines:
                if ',' in line:
                    # simple str.split() crashes on multiple '-' in description
                    pattern = "(?P<func_lst>[^-]+)-(?P<desc>.*)"
                    splited_line = re.match(pattern, line)
                    splited_line = splited_line.groupdict()
                    func_lst, desc = splited_line["func_lst"], splited_line["desc"]

                    for f in func_lst.split(','):
                        splited.append("%s - %s" % (f.strip(), desc))
                else:
                    splited.append(line)

            return splited


        whatis = Popen(["whatis", self.req_function], stdin=PIPE,
                       stdout=PIPE, stderr=PIPE)

        function_descriptions = whatis.communicate()[0]
        function_descriptions = function_descriptions.rstrip().split('\n')
        function_descriptions = split_whatis(function_descriptions)

        filtered_functions = list()

        sections = self.settings.get("sections", ["2", "3"])

        for item in function_descriptions:
            match = re.search(WHATIS_RE, item)
            if match:
                dct = match.groupdict()
                if dct["sect"] in sections and dct["func"].find(self.req_function) != -1:
                    func_desc = "(%s) - %s" % (dct["sect"], dct["desc"],)
                    self.function_list.append([dct["func"], func_desc])
            elif len(function_descriptions) is 1:
                # temporary hack: better detect in some more clever way
                sublime.status_message(item)
                return list()

        return self.function_list

    def _call_man(self, function):
        """ function = ['func', '(sect) - desc']"""
        # screw it!
        section = function[1].split('-')[0].strip(" ()")

        cmd_man = ["man", section, function[0]]
        cmd_col = ["col", "-b"]

        man = Popen(cmd_man, stdin=None, stdout=PIPE, stderr=PIPE)
        col = Popen(cmd_col, stdin=man.stdout, stdout=PIPE, stderr=PIPE)

        result = col.communicate()[0]

        return (result, { "func" : function[0], "sect" : section})

    def _render_manpage(self, manpage, desc):
        view = self.window.new_file()

        view.set_name("%s (%s)" % (desc["func"], desc["sect"]))
        view.set_scratch(True)

        edit = view.begin_edit()

        view.insert(edit, 0, manpage)
        view.end_edit(edit)
        view.set_read_only(True)
