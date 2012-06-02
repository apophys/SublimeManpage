import sublime
import sublime_plugin
import threading
import subprocess


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
        threading.Thread.__init__(self)


    def run(self):
        def show_panel():
        	if not self.req_function:
        		return

        	self.window.show_quick_panel(self._get_function_list(), self.on_done)
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

        return self.function_list

