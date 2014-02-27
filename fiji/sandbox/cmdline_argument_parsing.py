import sys
from optparse import OptionParser

# the Fiji launcher consumes commandline arguments that it actually knows
# about and that start with '--', so we work around this by using three
# dashes instead and reduce them for optparse again:
for (i, arg) in enumerate(sys.argv):
    sys.argv[i] = arg.replace('---', '--')

parser = OptionParser()
parser.add_option("--file", dest="filename",
                  help="write report to FILE", metavar="FILE")
parser.add_option("--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(opts, args) = parser.parse_args()

#for item in options:
#	print item

for item in args:
	print item

print('file: %s' % opts.filename)
print('verbose: %s' % opts.verbose)