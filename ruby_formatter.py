import os.path
from os import popen

import sublime, sublime_plugin, re

s = sublime.load_settings("RubyFormat.sublime-settings")

class RubyFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settings = self.view.settings()

		# settings
		selection = self.view.sel()[0]
		nwsOffset = self.prev_non_whitespace()

		# do formatting and replacement
		replaceRegion = None
		formatSelection = False

		# formatting a selection/highlighted area
		if(len(selection) > 0):
			formatSelection = True
			replaceRegion = selection

		# formatting the entire file
		else:
			replaceRegion = sublime.Region(0, self.view.size())

		plugin_path = os.path.join(sublime.packages_path(), 'RubyFormat')
		temp_code_file = os.path.join(plugin_path,".tempcode")
		ruby_script = os.path.join(plugin_path, "lib", "beautiful.rb")

		tempFile = open(temp_code_file,"w")
		tempFile.write(self.view.substr(replaceRegion))
		tempFile.close()
		temp_code_file = temp_code_file.replace(" ","\ ")
		ruby_script = ruby_script.replace(" ","\ ")

		cmd = "cat " + temp_code_file + " | " + ruby_script + " -"
		print cmd
		
		res = os.popen(cmd).read() # "test ruby" #jsbeautifier.beautify(self.view.substr(replaceRegion), opts)
		if(not formatSelection and settings.get('ensure_newline_at_eof_on_save')):
			res = res + "\n"

		self.view.replace(edit, replaceRegion, res)

		# re-place cursor
		offset = self.get_nws_offset(nwsOffset, self.view.substr(sublime.Region(0, self.view.size())))
		rc = self.view.rowcol(offset)
		pt = self.view.text_point(rc[0], rc[1])
		sel = self.view.sel()
		sel.clear()
		self.view.sel().add(sublime.Region(pt))

		self.view.show_at_center(pt)


	def prev_non_whitespace(self):
		pos = self.view.sel()[0].a
		preTxt = self.view.substr(sublime.Region(0, pos));
		return len(re.findall('\S', preTxt))

	def get_nws_offset(self, nonWsChars, buff):
		nonWsSeen = 0
		offset = 0
		for i in range(0, len(buff)):
			offset += 1
			if not(buff[i].isspace()):
				nonWsSeen += 1

			if(nonWsSeen == nonWsChars):
				break

		return offset