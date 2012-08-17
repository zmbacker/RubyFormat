import os.path
from os import popen
import codecs
import sublime, sublime_plugin, re
import rubybeautifier

s = sublime.load_settings("RubyFormat.sublime-settings")

class RubyFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime_settings = self.view.settings()

		# indent settings
		opts = rubybeautifier.default_options()
		opts.indent_char = " " if sublime_settings.get("translate_tabs_to_spaces") else "\t"
		opts.indent_size = int(sublime_settings.get("tab_size")) if opts.indent_char == " " else 1


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

		res = rubybeautifier.beautify(self.view.substr(replaceRegion),opts)

		if(not formatSelection and sublime_settings.get('ensure_newline_at_eof_on_save')):
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
