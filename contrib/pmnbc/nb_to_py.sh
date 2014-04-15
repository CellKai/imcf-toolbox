#!/bin/bash
#
# Poor Man's Netbeans Converter

cat - << EOF
import javax.swing

jFrame = javax.swing.JFrame()
getContentPane = jFrame.getContentPane
pack = jFrame.pack

EOF

sed 's,^        ,, ;
    s,;,, ;
    s,^[a-zA-Z0-9\.]\+ \([a-zA-Z0-9\.]\+ =\) new ,\1 , ;
    s, new , , '
