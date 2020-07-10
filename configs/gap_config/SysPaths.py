from __future__ import print_function
from __future__ import absolute_import

from six import string_types
import os, sys

config_path = os.path.dirname(os.path.abspath(__file__))
config_root = os.path.dirname(config_path)

class PathSearchFunc(object):
    _sys_paths = None
    environment_variable = 'M5_PATH'

    def __init__(self, subdirs, sys_paths=None):
        if isinstance(subdirs, string_types):
            subdirs = [subdirs]
        self._subdir = os.path.join(*subdirs)
        if sys_paths:
            self._sys_paths = sys_paths

    def __call__(self, filename):
        if os.sep in filename:
            return filename
        else:
            if self._sys_paths is None:
                try:
                    paths = os.environ[self.environment_variable].split(':')
                except KeyError:
                    paths = [ '/dist/m5/system', '/n/poolfs/z/dist/m5/system' ]

                # expand '~' and '~user' in paths
                paths = map(os.path.expanduser, paths)

                # filter out non-existent directories
                paths = filter(os.path.isdir, paths)

                if not paths:
                    raise IOError(
                        "Can't find system files directory, "
                        "check your {} environment variable"
                        .format(self.environment_variable))

                self._sys_paths = list(paths)

            filepath = os.path.join(self._subdir, filename)
            paths = (os.path.join(p, filepath) for p in self._sys_paths)
            try:
                return next(p for p in paths if os.path.exists(p))
            except StopIteration:
                raise IOError("Can't find file '{}' on {}."
                        .format(filename, self.environment_variable))

disk = PathSearchFunc('disks')
binary = PathSearchFunc('binaries')
script = PathSearchFunc('boot', sys_paths=[config_root])
