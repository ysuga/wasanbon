import os, sys
import urllib
import wasanbon

class DownloadReport(object):
    def __init__(self, verbose=True):
        self.verbose = verbose
        pass

    def __call__(self, read_blocks, block_size, total_bytes):
        if not self.verbose:
            return
        end = read_blocks * block_size / float(total_bytes) * 100.0
        if end > 100.0:
            end = 100.0
        sys.stdout.write('\r - Progress %3.2f [percent] ended' % end)
        sys.stdout.flush()

def download(url, dist="", force=False, verbose=False):

    if len(dist) == 0:
        dist = os.path.basename(url)
    if force and os.path.isfile(dist):
        os.remove(dist)
    if os.path.isfile(dist):
        if verbose:
            sys.stdout.write(' - file : %s is already downloaded.\n' % dist)
            pass
    else:
        if os.path.isfile(dist + '.part'):
            os.remove(dist+'.part')
        if verbose:
            sys.stdout.write("    - Downloading from URL: %s\n" % url)
        try:
            urllib.urlretrieve(url, dist+'.part', DownloadReport(verbose=verbose))
            os.rename(dist+'.part', dist)
            sys.stdout.write('\r - Progress 100.00 [percent] ended\n')
            sys.stdout.flush()
        except IOError, e:
            sys.stdout.write('     @ Failed to Download from %s\n' % url)
            raise wasanbon.DownloadFailedException()
        if verbose:
            sys.stdout.write("    - Saved in Directory  :%s\n" % dist)
    return True

