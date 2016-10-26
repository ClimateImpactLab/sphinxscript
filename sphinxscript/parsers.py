'''
Tools for parsing filenames and extracting comment headers from files
'''

import os, re, shutil, argparse

class Parser(object):
    
    @classmethod
    def parse(cls, filepath, relpath=None, package=None):
        raise NotImplementedError

class SimpleParser(Parser):
    documentation = '''

Header
~~~~~~

{header}


Raw Code
~~~~~~~~

.. literalinclude:: {filepath}
    :linenos:
'''

    @classmethod
    def extract_comment_header_from_file(cls, doc):
        '''
        Extract the comment header from a file
    
        Parameters
        ----------
        doc : str
            document from which to extract the header

        block_patterns : list
            list of regular expressions whcih match block comments. These 
            expressions should return a 'comment' group if matched.
        
        start_patterns : list
            list of tuples. Each tuple contains a regular expression which 
            matches start-of-line comments and a regular expression which can be 
            used to strip the comment characters.

        Returns

        header : str
            Comment header

        '''

        # Search for block patterns first
        # If these show up at the top of a file, parse the block pattern 
        # and then return the result
        for pattern in cls.block_patterns:
            search = re.match(pattern, doc)
            if search:
                header = search.group('comment')

        # If no block patterns match, search for start of line comments
        # This is to get around julia syntax issue where the block comment 
        # ``#= ... =#`` could be misread as a line comment.
        for pattern, sub_pattern in cls.start_patterns:
            comment_search = re.match(pattern, doc)
            if comment_search:
                comment_lines = map(lambda l: re.sub(sub_pattern, '', l), comment_search.group('comment').split('\n'))

                # Find the minimum number of whitespace characters on the left 
                # of each line
                min_whitespace = min([len(l) - len(l.lstrip()) for l in comment_lines if len(l) > 0])

                # strip min_whitespace whitespace characters from the left side
                comment_lines = map(lambda l: l if len(l) < min_whitespace else l[min_whitespace:], comment_lines)
                
                # join comment lines into a comment block
                header = '\n'.join(comment_lines)
            
        return ''

    @classmethod
    def parse(cls, filepath, relpath=None, package=None):
        if relpath is None:
            relpath = filepath

        with open(filepath, 'r') as doc:
            return cls.documentation.format(
                header = cls.extract_comment_header_from_file(doc.read()),
                filepath = relpath.replace('\\', '/'))


class RParser(SimpleParser):

    ''' block patterns can be defined with a multiline quoted block '''
    block_patterns = [
        
        # a "multiline quoted block"
        r'(\s*\n)*\s*\'(?P<comment>[^\']*)\'', 

        # a 'multiline quoted block'
        r'(\s*\n)*\s*\"(?P<comment>[^\"]*)\"']

    ''' start-of-line patterns can be defined with a '''
    start_patterns = [

        # a start-of-line #
        (r'(\s*\n)*(?P<comment>([\ \t]*#[^\n]*(\n|/Z))+)', r'^\s*#+')]


class MatlabParser(SimpleParser):

    ''' block patterns can be defined with quotes or a %{ comment block %}'''
    block_patterns = [
        
        # a "multiline quoted block"
        r'(\s*\n)*\s*\'(?P<comment>[^\']*)\'', 
        
        # a 'multiline quoted block'
        r'(\s*\n)*\s*\"(?P<comment>[^\"]*)\"', 

        # a %{ multiline comment block %}
        r'(\s*\n)*\s*\%\{(?P<comment>[^\']*)\%\}']

    ''' start-of-line patterns can be defined with a %'''
    start_patterns = [

        # a start-of-line %
        (r'(\s*\n)*(?P<comment>([\ \t]*\%+[^\n]*(\n|/Z))+)', r'^\s*\%+')]
    

class StataParser(SimpleParser):

    ''' block patterns can be defined with a /* multiline */ '''
    block_patterns = [r'(\s*\n)*\s*\/\*(?P<comment>[^\']*)\*\/']

    ''' start patterns can be defined with a * or //'''
    start_patterns = [

        # a start-of-line *
        (r'(\s*\n)*(?P<comment>([\ \t]*\*[^\n]*(\n|/Z))+)', r'^\s*\*+'),

        # a start-of-line // (don't allow end-of-line comments for header)
        (r'(\s*\n)*(?P<comment>([\ \t]*\/\/[^\n]*(\n|/Z))+)', r'^\s*\/\/')]

class JuliaParser(SimpleParser):

    ''' block patterns can be defined with #= comment blocks =# '''
    block_patterns = [

        # a ''' multiline quoted block '''
        r'(\s*\n)*\s*\#\=(?P<comment>([^\'](\'{,2}(?!=\')))*)\=\#']


    ''' start patterns can be defined with # '''
    start_patterns = [
    
        # a start-of-line #
        (r'(\s*\n)*(?P<comment>([\ \t]*#[^\n]*(\n|/Z))+)', r'^\s*#+')]
    

class PythonParser(Parser):
    
    ''' block patterns can be defined with a quoted block '''
    block_patterns = [

        # a ''' multiline quoted block '''
        r'(\s*\n)*\s*\'\'\'(?P<comment>([^\'](\'{,2}(?!=\')))*)\'\'\'',

        # a """ multiline quoted block """
        r'(\s*\n)*\s*\"\"\"(?P<comment>([^\"](\"{,2}(?!=\")))*)\"\"\"']

    ''' start patterns can be defined with a # '''
    start_patterns = [
    
        # a start-of-line #
        (r'(\s*\n)*(?P<comment>([\ \t]*#[^\n]*(\n|/Z))+)', r'^\s*#+')]

    @classmethod
    def parse(cls, filepath, relpath=None, package=None):
        return '''

.. automodule:: {modpath}
    :members:
    :undoc-members:
    :show-inheritance:

'''.format(modpath='.'.join(os.path.relpath(filepath, package).split(os.sep)))


'''
PARSERS defines the set of regular expressions for each available syntax

Each syntax has the following three entries:

:regex: list of regular expressions which match valid filenames for each 
    syntax
:block_patterns: list of regular expressions whcih match block comments. 
    These expressions should return a 'comment' group if matched.
:start_patterns: list of tuples. Each tuple contains a regular expression 
    which matches start-of-line comments and a regular expression which can 
    be used to strip the comment characters.
'''
PARSERS = {

    RParser: [
        # Files can end in .r or .rscript
        r'\.(r|rscript)$'
    ],

    MatlabParser: [
        # Files can end in .m
        r'\.m$'
    ],

    StataParser: [
        # Files can end in .do
        r'\.do$'
    ],

    PythonParser: [
        # Files can end in .py, .pyc, .pyb, etc.
        r'\.py\w*$'
    ],


    JuliaParser: [
        # Files can end in .jl or .julia
        r'\.(jl|julia)$'
    ],
}




def get_parser_from_filename(filepath):
    '''
    Determine the programming language from a filename or filepath

    Parameters
    ----------
    filepath : str
        filename or filepath from which to determine syntax

    Returns
    -------
    parser : object
        parser object indicated by filepath

    '''

    for parser, patterns in PARSERS.items():
        for patt in patterns:
            if re.search(patt, filepath, re.I):
                return parser
    
    raise ValueError('Cannot determine filetype. Extension unknown.')

