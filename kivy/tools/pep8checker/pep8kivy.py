import sys
import os
from os.path import isdir, join
import pep8
import time

htmlmode = False

class KivyStyleChecker(pep8.Checker):
    def __init__(self, filename):
        pep8.Checker.__init__(self, filename)

    def report_error(self, line_number, offset, text, check):
        if htmlmode is False:
            return pep8.Checker.report_error(self,
                line_number, offset, text, check)

        # html generation
        print '<tr><td>%d</td><td>%s</td></tr>' % (line_number, text)


if __name__ == '__main__':

    def usage():
        print 'Usage: python pep8kivy.py [-html] <file_or_folder_to_check>*'
        print 'Folders will be checked recursively.'
        sys.exit(1)

    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-html':
        if len(sys.argv) < 3:
            usage()
        else:
            htmlmode = True
            targets = sys.argv[-1].split()
    elif sys.argv == 2:
        targets = sys.argv[-1]
    else:
        targets = sys.argv[-1].split()

    errors = 0
    pep8.process_options([''])
    exclude_dirs = ['/lib', '/coverage', '/pep8']
    exclude_files = ['kivy/gesture.py', 'osx/build.py', 'win32/build.py']
    for target in targets:
        if os.path.isdir(target):
            if htmlmode:
                print open(join(abspath(__file__), 'pep8base.html'), 'r').read()
                print '''<p>Generated: %s</p><table>''' % (time.strftime('%c'))

            for dirpath, dirnames, filenames in os.walk(target):
                cont = False
                for pat in exclude_dirs:
                    if pat in dirpath:
                        cont = True
                        break
                if cont:
                    continue
                for filename in filenames:
                    if not filename.endswith('.py'):
                        continue
                    cont = False
                    complete_filename = os.path.join(dirpath, filename)
                    for pat in exclude_files:
                        if complete_filename.endswith(pat):
                            cont = True
                    if cont:
                        continue

                    if htmlmode:
                        print '<tr><th colspan="2">%s</td></tr>' % complete_filename
                    checker = KivyStyleChecker(complete_filename)
                    errors += checker.check_all()

            if htmlmode:
                print '</div></div></table></body></html>'

        else:
            # Got a single file to check
            for pat in exclude_dirs + exclude_files:
                if pat in target:
                    continue
            if target.endswith('.py'):
                checker = KivyStyleChecker(target)
                errors += checker.check_all()

    # If errors is 0 we return with 0. That's just fine.
    sys.exit(errors)