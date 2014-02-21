import os
from java.lang.System import getProperty

print(os.getcwd())
 
print('Fiji dir: %s' % getProperty('fiji.dir'))
