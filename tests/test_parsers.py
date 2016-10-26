import tempfile, shutil, os, sys, subprocess, re, time
from cookiecutter.main import cookiecutter


def assert_build(target_dir):

    try:

        tmpdir = tempfile.mkdtemp()

        projname = os.path.basename(target_dir)
        projdir = os.path.join(tmpdir, projname)
        docsdest = os.path.join(projdir, 'docs')

        shutil.copytree(target_dir, projdir)

        proc = subprocess.Popen(
            ['make', 'html'], 
            cwd=os.path.join(docsdest), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        stdout, stderr = proc.communicate()


        if len(stderr) != 0:
            raise IOError('Errors encountered in make:\n{}'.format(stderr))

        with open(os.path.join(docsdest, 'index.rst')) as ind:
            assert re.search('sphinxscript', ind.read())


        with open(os.path.join(docsdest, 'sphinxscript.rst')) as ind:
            index = ind.read()

            # Make sure script documentation files ``sphinxscript/*.rst`` are 
            # included in ``[projname].rst``
            for f in os.listdir(target_dir):
                if not os.path.isfile(os.path.join(target_dir, f)):
                    continue

                innerscript_name = os.path.splitext(f)[0] + '_' + os.path.splitext(f)[1][1:]
                assert re.search('sphinxscript' + '/' + innerscript_name, index)
        

    finally:
        if os.path.isdir(tmpdir):
            shutil.rmtree(tmpdir)

def test_doc_creation():
    '''
    Create and build docs in a temporary directory and test output
    '''

    testbase = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_projects'))

    for testdir in os.listdir(testbase):
        
        if os.path.isfile(os.path.join(testbase, testdir)):
            continue

        assert_build(os.path.join(testbase, testdir))




def main():

    test_doc_creation()

if __name__ == '__main__':
    main()