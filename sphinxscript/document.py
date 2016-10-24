'''
Create .rst documentation of scripts from header comments
'''

import os, re, shutil, argparse
import parsers


SourceFileTemplate = '''
{filename}
{line}

Header
~~~~~~

{header}


Raw Code
~~~~~~~~

.. literalinclude:: {filepath}
    :linenos:

'''

DirectoryIndexFileTemplate = '''
{path}
{line}

.. toctree::
{indent}:maxdepth: 2
'''


class SourceFile(object):

    TEMPLATE = SourceFileTemplate
    
    @classmethod
    def create_sourcefile_rst(cls, filepath):
        '''
        Fill keyword values in :py:attr:`TEMPLATE`

        Parameters
        ----------

        filepath : str
            Path to the script being documented

        Returns
        -------
        str
            Documentation rst page for script found at `filepath`

        '''

        p = parsers.Parser
        filename = os.path.basename(filepath)

        return cls.TEMPLATE.format(
            filename = filename,
            line = '-'*max(len(filename), 50),
            header = p.extract_comment_header_from_file(filepath),
            filepath = os.path.relpath(filepath, '.'))


class DirectoryIndexFile(object):
    def __init__(self, path):
        self.path = os.path.basename(path).replace(os.sep, '/')



def document_directory(base_dir, current_dir, output_dir, exclude_dirs, dir_title):
    
    #.rst file gen to map the subfolders
    dirindex_file = os.path.join(output_dir, dir_title + '.rst')
    if not os.path.isdir(os.path.dirname(dirindex_file)):
        os.makedirs(os.path.dirname(dirindex_file))

    #actual call to write the .rst files to mirror directory structure
    with open(dirindex_file, 'w+') as dirindex:
        path = os.path.basename(current_dir).replace(os.sep, '/')
        dirindex.write('{}\n'.format(path))
        dirindex.write('-'*max(40, len(path)) + '\n\n')
        dirindex.write('.. toctree:: \n')
        dirindex.write('    :maxdepth: 2\n\n')

        #recurse your directories, call document_codefile and write a .rst file where needed
        for path in os.listdir(current_dir):
            
            target_file = os.path.join(current_dir, path)
            rel_path = os.path.splitext(os.path.relpath(target_file, base_dir))[0]
            
            #check to see if target file is a file...
            if os.path.isfile(target_file):
                try:
                    document_codefile(base_dir, current_dir, output_dir, dir_title, target_file, rel_path, path)
                    dirindex.write('    {}\n'.format(rel_path.replace(os.sep, '/')))
                except ValueError, e:
                    print('Skipping {}'.format(path))

            #or a directory
            elif os.path.isdir(target_file):

                #if target_file is in list of excluded_directories keep moving
                if os.path.abspath(target_file) in map(os.path.abspath, exclude_dirs):
                    continue

                #otherwise create new directories and recurse till document_codefile basecase 
                dirindex.write('    {d}/{d}\n'.format(d=os.path.basename(path).replace(os.sep, '/')))
                document_directory(base_dir, target_file, os.path.join(output_dir, path), exclude_dirs, path)


s = SourceFile.create_sourcefile_rst(os.path.expanduser('~/Dropbox (Rhodium Group)/GCP/MORTALITY/analysis/agegrp_interaction_test.do'))
print(s)

# def document_codefile(base_dir, target_dir, output_dir, dir_title, target_file, rel_path, path):


#     #file path gen for .rst file
#     doc_path = os.path.join(output_dir, rel_path + '.rst')
    
#     #check to see if the directory exists
#     if not os.path.isdir(os.path.dirname(doc_path)):
#         #gen directory for .rst
#         os.makedirs(os.path.dirname(doc_path))
    
#     #gen the header and .rst file from the .do filepaths
#     rst, header = parse_codefile(os.path.join(target_dir, path), doc_path)
    
#     #write .rst file with contents from rst output from parse statafile
#     with open(doc_path, 'w+') as do_doc:
#         do_doc.write(rst)





# def create_code_sphinx(target_dir, output_dir, package_title, author):
#     ''' Create a sphinx webpage from a .do file directory '''


#     target_dir = os.path.abspath(os.path.expanduser(target_dir))
#     output_dir = os.path.abspath(os.path.expanduser(output_dir))

#     output_target = os.path.join(output_dir, package_title)
#     if os.path.isdir(output_target):
#         shutil.rmtree(output_target)

#     document_directory(
#         base_dir=target_dir, 
#         target_dir=target_dir, 
#         output_dir=output_target, 
#         exclude_dirs=[output_dir],
#         dir_title=package_title)


# def main(target_dir='../', output_dir='.'):
#     create_code_sphinx(
#         target_dir=target_dir,
#         output_dir=output_dir, 
#         package_title='{{cookiecutter.project_slug}}', 
#         author='`{{cookiecutter.full_name}} <https://climateimpactlab.slack.com/messages/{{cookiecutter.slack}}/>`_')

# if __name__ == '__main__':
#     main()
