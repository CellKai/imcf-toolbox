#!/bin/sh

echo "Updating generated Python code..."

for file in *.ui ; do
    echo " - $file"
    TGT=$(echo $file | sed 's,^generic_,, ; s,.ui$,.py,')
    pyuic4 $file -o ../../lib/python2.7/genui/$TGT
done

echo "Done."
