import os
from java.lang.System import getProperty
from os.path import join
import sys.path

libs = join(getProperty('fiji.dir'), join('plugins', join('IMCF', 'libs')))
sys.path.append(libs)

print(sys.path)

import fluoview
import log

print fluoview.__file__
print log.__file__
