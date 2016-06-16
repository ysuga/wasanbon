import subprocess, sys, traceback, os, sys

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.git']

    def _print_alternatives(self, args):
        print 'run'

    @manifest
    def run(self, argv):
        """ Do Selfupdate  through pip
        """
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option
        force   = options.force_flag

        if not force:
            print '# Add Force flag (-f).'
            return -1

        #print '# This is test admin plugin'
        #cmd = ['pip', 'install', '-U', '--user', 'wasanbon']
        #return subprocess.call(cmd)

        cwd = os.getcwd()
        
        os.chdir(wasanbon.temp_path)

        if os.path.isdir(os.path.join(wasanbon.temp_path, 'wasanbon')):
            admin.git.git_command(['pull', 'origin', 'release'], verbose=True)
        else:
            url = 'https://github.com/sugarsweetrobotics/wasanbon.git'
            admin.git.git_command(['clone', url,  'origin', 'release'], verbose=True)
        
        command = ['python', 'setup.py', 'install']
        ret = subprocess.call(command)
        os.chdir(cwd)
        return ret

