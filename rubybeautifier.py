# import sys
# import getopt
import re
# import string

#
# Written by Lester Zhao, zm.backer@gmail.com,
# MIT licence, enjoy.
# I am a ruby programmer.
# Python is not my native language, but it can work for you.


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

def indent_base( prev_line, opts = default_options() ):
    b = Beautifier()
    return b.get_base_indent( prev_line, opts )


class Beautifier:

    def __init__(self, opts = default_options() ):

        self.opts = opts
        self.indent_exp = [
            re.compile(r'^module\b'),
            re.compile(r'^class\b'),
            re.compile(r'^if\b'),
            re.compile(r'(=\s*|^)until\b'),
            re.compile(r'(=\s*|^)for\b'),
            re.compile(r'^unless\b'),
            re.compile(r'(=\s*|^)while\b'),
            re.compile(r'(=\s*|^)begin\b'),
            re.compile(r'(^| )case\b'),
            re.compile(r'\bthen\b'),
            re.compile(r'^rescue\b'),
            re.compile(r'^def\b'),
            re.compile(r'\bdo\b'),
            re.compile(r'^else\b'),
            re.compile(r'^elsif\b'),
            re.compile(r'^ensure\b'),
            re.compile(r'\bwhen\b'),
            re.compile(r'\{[^\}]*$'),
            re.compile(r'\[[^\]]*$'),
            # re.compile(r'\([^\)]*$'),
            # re.compile(r'\(\s*\{.*(?!\}\s*\)$).*$')
        ]
        self.outdent_exp = [
            re.compile(r'^rescue\b'),
            re.compile(r'^ensure\b'),
            re.compile(r'^elsif\b'),
            re.compile(r'^end\b'),
            re.compile(r'^else\b'),
            re.compile(r'\bwhen\b'),
            re.compile(r'^[^\{]*\}'),
            re.compile(r'^[^\[]*\]'),
            # re.compile(r'^\).*$'),
            # re.compile(r'^\}\s*\).*$')
        ]
        self.debtdent_exp = [
            # re.compile(r'.+\).*$')
        ]
        self.confusion_exp = [
            re.compile(r'\{[^\{]*?\}'),
            re.compile(r'\[[^\[]*?\]'),
            re.compile(r'\'.*?\''),
            re.compile(r'".*?"'),
            re.compile(r'\`.*?\`'),
            re.compile(r'\([^\(]*?\)'),
            re.compile(r'\/.*?\/'),
            re.compile(r'\%r(.).*?\1'),
        ]


    def make_tab(self, tab ):
        if(tab < 0):
            tab_str = ''
        else:
            tab_str = self.opts.indent_char * self.opts.indent_size * tab
        return self.opts.indent_base + tab_str


    def add_line( self, line, tab ):
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
        debt_tab = 0
        output = []
        line_point = 0
        lines = s.split("\n")

        for line in lines:
            line = line.rstrip()
            if( not program_end ):
                # detect program end mark
                if( line_point >= len(lines) ):
                    program_end = True
                else:
                    #combine continuing lines
                    if( (not re.search(r'^\s*#',line)) and re.search(r'[^\\]\\\s*$',line) ):
                        multiline_array.append( line )
                        multiline_str += re.sub(r'^(.*)\\\s*$', r'\1', line)
                        continue

                    #add final line
                    if( len(multiline_str) > 0 ):
                        multiline_array.append( line )
                        multiline_str += re.sub( r'^(.*)\\\s*$', r'\1',line)
                    if len(multiline_str) > 0:
                        tline = multiline_str.strip()
                    else:
                        tline = line.strip()
                    
                    if re.search(r'^=begin',tline):
                        comment_block = True
                    if in_here_doc:
                        if re.search(r'\s*%s\s*'%(here_doc_term),tline): in_here_doc = False
                    else:
                        if re.search( r'=\s*<<' , tline ):
                            here_doc_term = re.sub( r'.*=\s*<<-?\s*([_|\w]+).*' , r'\1', tline )
                            in_here_doc = len( here_doc_term ) > 0
            if comment_block or program_end or in_here_doc :
                output.append( line )
            else:
                comment_line = re.search( r'^#' ,tline )
                if not comment_line:
                    for ce in self.confusion_exp :
                        while ce.search(tline):
                            tline = ce.sub( '', tline )
                    # delete end-of-line comments
                    tline = re.sub(r'#[^\"]+$','',tline,1) 
                    # convert quotes
                    tline = re.sub(r'\\\"', "'", tline )

                    for oe in self.outdent_exp:
                        if oe.search( tline ):
                            tab -= 1
                            break
                    for de in self.debtdent_exp: #by lester
                        if de.search( tline ):
                            debt_tab += 1
                            break

                    
                if len( multiline_array ) > 0 :
                    for ml in multiline_array:
                        output.append( self.add_line(ml,tab) )
                    multiline_array = []
                    multiline_str = ""
                else:
                    output.append( self.add_line( line, tab ) )
                if not comment_line :
                    for ie in self.indent_exp :
                        if ie.search( tline ) and ( not re.search( r'\s+end[\s\.]*.*$',tline )  ):
                            tab += 1
                            break
                    if debt_tab > 0: # by lester
                        tab -= debt_tab
                        debt_tab = 0

            if re.search( r'^=end', tline ):
                comment_block = False
            line_point += 1
            # print line
        error = ( tab != 0)
        if error :
            print "Error: indent/outdent mismatch: %d."%(tab)
        return "\n".join( output )

    def format_line( self, line):
        
        pass

    def get_base_indent( self, prev_line, opts = None):
        if opts != None:
            self.opts = opts
        base_str = re.search( r'^\s*', prev_line ).group()
        # base_re = re.compile(r'^\s*')
        # base_re.search()

        for ie in self.indent_exp :
            if ie.search( prev_line.strip() ) :
                return base_str + self.make_tab(1)
                break
        return base_str









