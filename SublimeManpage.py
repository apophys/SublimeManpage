# -*- coding: utf-8 –*–

import locale
import logging
import re
import threading
import webbrowser

from subprocess import Popen, PIPE
from urllib2 import urlopen, HTTPError


import sublime
import sublime_plugin

def manpage_api_factory(window, word):
    """Generate manpage api object"""

    if sublime.platform() in ["osx", "linux"]:
        return ManpageApiCall(window, word)
    else:
        return ManpageWebCall(window, word)


class ExactMatchSettings(sublime_plugin.WindowCommand):
    """ This writes changes to User Settings """
    def run(self, mode=False):
        settings = sublime.load_settings("SublimeManpage.sublime-settings")
        if type(mode) is bool:
            settings.set("exact_match", mode)
            sublime.save_settings("SublimeManpage.sublime-settings")
        else:
            sublime.status_message("Unexpected parameter type.")


class ManpageCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Type function name or command:", "",
                                     self.on_done, None, None)

    def on_done(self, line):
        command = manpage_api_factory(self.window, line)
        command.start()


class FindManpageFromSelectionCommand(sublime_plugin.WindowCommand):
    def run(self):
        currentView = self.window.active_view()

        wordEnd = currentView.sel()[0].end()
        if currentView.sel()[0].empty():
            word = currentView.substr(currentView.word(wordEnd)).lower()
        else:
            word = currentView.substr(currentView.sel()[0]).lower()
        if word is None or len(word) <= 1:
            sublime.status_message('No word selected')
            return
        sublime.status_message("Selected word is: " + word)

        command = manpage_api_factory(self.window, word)
        command.start()


class ManpageApiCall(threading.Thread):
    def __init__(self, window, func):
        WHATIS_RE = "^(?P<func>[\w-]+)\s*\((?P<sect>[^\)+])\)\s+-\s+(?P<desc>.*)$"
        self.window = window
        self.req_function = func
        self.function_list = []
        self.settings = sublime.load_settings("SublimeManpage.sublime-settings")
        self.whatis_re = re.compile(WHATIS_RE)
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

        logging.debug("[sublime_manpage:on_done] (%d, %d)"
                      % (len(self.function_list), picked))

        manpage, title = self._call_man(self.function_list[picked])
        self._render_manpage(manpage, title)

    def _get_function_list(self):
        def split_whatis(lines):
            splited = []

            for line in lines:
                if ',' in line:
                    func_lst, desc = line.split('-', 1)

                    for f in func_lst.split(','):
                        splited.append("%s - %s" % (f.strip(), desc))
                else:
                    splited.append(line)

            return splited

        whatis = Popen(["whatis", self.req_function], stdin=None,
                       stdout=PIPE, stderr=PIPE)

        whatis_output = whatis.communicate()[0]
        function_descriptions = whatis_output.rstrip().split('\n')
        function_descriptions = split_whatis(function_descriptions)

        sections = self.settings.get("sections", ["2", "3"])
        exact_match = self.settings.get("exact_match", False)

        if len(function_descriptions) is 1 and not function_descriptions[0]:
            sublime.status_message("Manpage: Function '%s' not found"
                                   % self.req_function)
            return []

        for item in function_descriptions:
            match = re.search(self.whatis_re, item)
            if match:
                dct = match.groupdict()
                func_found = dct["func"].find(self.req_function) != -1
                if dct["sect"] in sections and func_found:
                    func_desc = "(%s) - %s" % (dct["sect"], dct["desc"],)
                    entry = [dct["func"], func_desc]
                    logging.debug("[sublime_manpage] Exact match: [%s]; \
                                  searched function: [%s]; \
                                  parsed function: [%s]"
                                  % (exact_match, self.req_function, dct["func"]))

                    if exact_match and dct["func"] == self.req_function:
                        # Returning *first* exact match.
                        logging.debug("[sublime_manpage] Match for [%s]"
                                      % dct["func"])
                        self.function_list = [entry]
                        return self.function_list
                    else:
                        self.function_list.append(entry)
                elif func_found:
                    msg = "Manpage: function %s found but section %s is not in configuration file."
                    sublime.status_message(msg % (self.req_function, dct["sect"]))
                    return []
            elif len(function_descriptions) is 1:
                # temporary hack: better detect in some more clever way
                sublime.status_message("Function %s not found in whatis database."
                                       % self.req_function)

        return self.function_list

    def _call_man(self, function):
        """ function = ['func', '(sect) - desc']"""
        # screw it!
        section = function[1].split('-')[0].strip(" ()")

        logging.debug("[sublime_manpage] Calling man for [%s] in section [%s]" %
                      (function[0], section))
        cmd_man = ["man", section, function[0]]
        cmd_col = ["col", "-b"]

        man = Popen(cmd_man, stdin=None, stdout=PIPE, stderr=PIPE)
        col = Popen(cmd_col, stdin=man.stdout, stdout=PIPE, stderr=PIPE)

        result = col.communicate()[0]

        return (result, {"func": function[0], "sect": section})

    def _render_manpage(self, manpage, desc):
        view = self.window.new_file()

        view.set_name("%s (%s)" % (desc["func"], desc["sect"]))
        view.set_scratch(True)

        if sublime.platform() == "linux":
            loc = locale.getdefaultlocale()[-1]
            data = manpage.decode(loc)
        else:
            # python bundled with Sublime Text raises ValueError for UTF-8
            # on OS X
            data = manpage

        edit = view.begin_edit()

        view.insert(edit, 0, data)
        view.end_edit(edit)
        view.set_read_only(True)


class ManpageWebCall(threading.Thread):

    URL = "http://www.linuxmanpages.com/man%(section)s/%(function)s.%(section)s.php"

    def __init__(self, window, func):
        self.window = window # TODO: refactor
        self.function = func
        self.settings = sublime.load_settings("SublimeManpage.sublime-settings")
        threading.Thread.__init__(self)

    def run(self):
        def get_manpage_url(url_data):
            for item in url_data:
                try:
                    url = ManpageWebCall.URL % item
                    f = urlopen(url)
                    f.close()
                    if f.getcode() is 200:
                        return url
                    else:
                        pass # potentially ignoring redirects
                except HTTPError, e:
                    pass
            else:
                return None

        sections = self.settings.get("sections", ["2", "3"])
        url_data = ({ "function" : self.function, "section" : s} for s in sections)

        url = get_manpage_url(url_data)

        if url:
            webbrowser.open(url)
        else:
            sublime.error_message("Manpage for '%s' not found in sections [%s]."
                                  % (self.function, ', '.join(sections)))
