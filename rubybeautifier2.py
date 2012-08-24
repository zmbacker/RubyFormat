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


class Beautifier:

    def __init__(self, opts = default_options() ):

        self.opts = opts
        self.blank_state()


    def blank_state(self):

        self.wanted_newline = False
        self.just_added_newline = False

        self.indent_string = self.opts.indent_char * self.opts.indent_size

        self.preindent_string = ''
        self.last_word = ''              # last TK_WORD seen
        self.last_type = 'TK_START_EXPR' # last token type
        self.last_text = ''              # last token text
        self.last_last_text = ''         # pre-last token text

        self.input = None
        self.output = []

        self.whitespace = ["\n", "\r", "\t", " "]
        self.wordchar = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
        self.digits = '0123456789'
        self.punct = '+ - * / % = += -= *= /= %= == === != !== > < >= <= << && &= | || ! !! , : ? ^ ^= |= ::'
        self.punct = self.punct.split(' ')


        global parser_pos
        parser_pos = 0



    def beautify(self, s, opts = None ):
        if opts != None:
            self.opts = opts

        self.blank_state()

        while s and s[0] in [' ', '\t']:
            self.preindent_string += s[0]
            s = s[1:]
        
        self.input = s

        parser_pos = 0
        while True:

            token_text, token_type = self.get_next_token()
            if token_type == 'TK_EOF':
                break

            handlers = {
                'TK_END_LINE': self.handle_end_line,
                # 'TK_START_EXPR': self.handle_start_expr,
                # 'TK_END_EXPR': self.handle_end_expr,
                # 'TK_START_BLOCK': self.handle_start_block,
                # 'TK_END_BLOCK': self.handle_end_block,
                # 'TK_WORD': self.handle_word,
                # 'TK_SEMICOLON': self.handle_semicolon,
                # 'TK_STRING': self.handle_string,
                # 'TK_EQUALS': self.handle_equals,
                # 'TK_OPERATOR': self.handle_operator,
                # 'TK_BLOCK_COMMENT': self.handle_block_comment,
                'TK_INLINE_COMMENT': self.handle_inline_comment,
                # 'TK_COMMENT': self.handle_comment,
                'TK_UNKNOWN': self.handle_unknown,
            }

            handlers[token_type](token_text)

            self.last_last_text = self.last_text
            self.last_type = token_type
            self.last_text = token_text

        sweet_code = self.preindent_string + re.sub('[\n ]+$', '', ''.join(self.output))
        return sweet_code


    def append( self, s ):

        self.output.append(s)


    def get_next_token( self ):
        global parser_pos

        if parser_pos >= len(self.input):
            return '', 'TK_EOF'

        c = self.input[parser_pos]
        parser_pos += 1

        if c == '\n' :
            return c, 'TK_END_LINE'

        # in line comment token: TK_INLINE_COMMENT
        if c == '#':
            while self.input[ parser_pos ] != '\n':
                c = c + self.input[ parser_pos ]
                parser_pos += 1
                if parser_pos == len( self.input ) :
                    break
            return c, 'TK_INLINE_COMMENT'

        # normal token: TK_UNKNOWN
        if c != "\n":
            while self.input[ parser_pos ] != "\n":
                c = c + self.input[ parser_pos ]
                parser_pos += 1
                if parser_pos == len( self.input ) :
                    break
            return c, 'TK_UNKNOWN'


    def handle_end_line( self, token_text ):
        self.append( token_text )

    def handle_unknown( self, token_text ):
        self.append( token_text )

    def handle_inline_comment( self, token_text ):
        self.append( token_text + '====' )