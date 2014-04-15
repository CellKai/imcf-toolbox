#!/bin/bash
#
# Poor Man's Netbeans Converter

sed 's,^        ,, ;
    s,;,, ;
    s,^[a-zA-Z0-9\.]\+ \([a-zA-Z0-9\.]\+ =\) new ,\1 , ;
    s, new , , '
