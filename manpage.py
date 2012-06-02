import sublime
import sublime_plugin
import threading
import re
from subprocess import Popen, PIPE

WHATIS_RE = "(?P<func>\w+[^\(]+),?\s*\((?P<sect>\dp?m?)\)\s+-\s+(?P<desc>.*)$"

class ManpageCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.platform() not in ["osx", "linux"]:
            sublime.error_message("Manpage: Platform %s is not supported."
                                  % sublime.platform())
            return

        self.window.show_input_panel("Type function name:", "",
                                     self.on_done, None, None)

    def on_done(self, line):
        ManpageThread(self.window, line).start()


class ManpageThread(threading.Thread):
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

            self.window.show_quick_panel(self._get_function_list(),
                                         self.on_done)
            # provisional

        sublime.set_timeout(show_panel, 10)

    def on_done(self, picked):
        if picked == -1:
            return

        sublime.error_message("You have picked option: %s"
                              % self.function_list[picked])

    def _get_function_list(self):
        # temporary
        self.function_list.append(self.req_function)

        def split_whatis(lines):
            splited = list()

            for line in lines:
                if ',' in line:
                    func_lst, desc = line.split('-')
                    for f in func_lst.split(','):
                        splited.append("%s - %s" % (f, desc))
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
            mtch = re.search(WHATIS_RE, item)
            if mtch:
                dct = mtch.groupdict()
                if dct["sect"] in sections:
                    print "Matches: [name:%s] [section:%s]" % (dct["func"], dct["sect"],)

        return self.function_list
