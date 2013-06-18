#!/bin/sh

echo "Updating generated Python code..."

for file in *.ui ; do
    echo " - $file"
    TGT="ui_$(echo $file | sed 's,.ui$,.py,')"
    pyuic4 $file -o ../../lib/python2.7/$TGT
done

echo "Done."
