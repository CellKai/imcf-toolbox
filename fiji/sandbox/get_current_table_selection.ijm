// String.paste requires 1.48j
requires("1.48j");

selectWindow("Results");

String.copyResults();
str = String.paste();
fields = split(str, "\t");

for (n=0; n < fields.length; n+=1)
     print(fields[n]);
