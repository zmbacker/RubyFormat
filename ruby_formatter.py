import os.path
from os import popen
import codecs
import sublime, sublime_plugin, re
import rubybeautifier

l_settings = sublime.load_settings("RubyFormat.sublime-settings")

class RubyFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime_settings = self.view.settings()

		selection = self.view.sel()[0]
		nwsOffset = self.prev_non_whitespace()

		# do formatting and replacement
		replaceRegion = None
		formatSelection = False

		# formatting a selection/highlighted area
		if(len(selection) > 0):
			formatSelection = True
			replaceRegion = self.get_formatting_region( selection )

		# formatting the entire file
		else:
			replaceRegion = sublime.Region(0, self.view.size())

		# indent settings
		opts = rubybeautifier.default_options()
		opts.indent_char = " " if sublime_settings.get("translate_tabs_to_spaces") else "\t"
		opts.indent_size = int(sublime_settings.get("tab_size")) if opts.indent_char == " " else 1


		if formatSelection :
			opts.indent_base = rubybeautifier.indent_base( self.get_prev_line(replaceRegion) ,opts)
		
		res = rubybeautifier.beautify(self.view.substr(replaceRegion),opts)
		if(not formatSelection and sublime_settings.get('ensure_newline_at_eof_on_save')):
			res = res + "\n"

		self.view.replace(edit, replaceRegion, res)

		# re-place cursor
		offset = self.get_nws_offset(nwsOffset, self.view.substr(sublime.Region(0, self.view.size())))
		pt = offset
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

	# get prev line with real contents
	def get_prev_line(self, selected_region):
		current_line = self.view.line( selected_region.begin() )
		got_line = False
		first_line = False
		while not ( got_line or first_line ) :
			prev_line_point = current_line.begin() - 1
			if prev_line_point < 0 :
				first_line = True
				return ""
				break
			current_line = self.view.line( prev_line_point )
			current_line_str = self.view.substr(current_line)
			if len( current_line_str.strip() ) > 0 :
				got_line = True
				return current_line_str
				break

	# make sure that the formated text are from the begin of a line to the end of another line.
	def get_formatting_region( self, selection ):
		begin_point = self.view.line( selection.begin() ).begin()
		end_point = self.view.line( selection.end() ).end()
		if selection.a < selection.b :
			return sublime.Region( end_point, begin_point )
		else:
			return sublime.Region( begin_point, end_point )






