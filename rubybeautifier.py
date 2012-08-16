# import sys
# import getopt
# import re
# import string

#
# Originally written by Lester Zhao,
# Conversion to python by Lester Zhao, zm.backer@gmail.com,
# MIT licence, enjoy.
#
# Python is not my native language, feel free to push things around.


# Options Class
class BeautifierOptions:
    def __init__(self):
        self.indent_size = 2
        self.indent_char = ' '
        self.indent_base = ''


# module method

def default_options():
    return BeautifierOptions()


def beautify(string, opts = default_options() ):
    b = Beautifier()
    return b.beautify(string, opts)




class Beautifier:

    def __init__(self, opts = default_options() ):

        self.opts = opts
        self.indent_exp = [
            '^module\b',
            '^class\b',
            '^if\b',
            '(=\s*|^)until\b',
            '(=\s*|^)for\b',
            '^unless\b',
            '(=\s*|^)while\b',
            '(=\s*|^)begin\b',
            '(^| )case\b',
            '\bthen\b',
            '^rescue\b',
            '^def\b',
            '\bdo\b',
            '^else\b',
            '^elsif\b',
            '^ensure\b',
            '\bwhen\b',
            '\{[^\}]*$',
            '\[[^\]]*$'
        ]
        self.outdent_exp = [
            '^rescue\b',
            '^ensure\b',
            '^elsif\b',
            '^end\b',
            '^else\b',
            '\bwhen\b',
            '^[^\{]*\}',
            '^[^\[]*\]'
        ]


    def make_tab( tab ):
        if(tab < 0):
            tab_str = ''
        else:
            tab_str = self.opts.indent_char * self.opts.indent_size * tab
        return tab_str


    def add_line( line, tab ):
        line = line.strip()
        if len( line ) > 0:
            line = self.make_tab( tab ) + line
        return line

    def beautify(self, s, opts = None ):
        if opts != None:
            self.opts = opts

        comment_block = False
        in_here_doc = False
        here_doc_term = ""
        program_end = False
        multiline_array = []
        multiline_str = ""
        tab = 0
        output = []
        for line in s.split("\n"):
            line = line.rstrip()
            print line















