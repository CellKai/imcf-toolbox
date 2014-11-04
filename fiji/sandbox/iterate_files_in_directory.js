importClass(Packages.java.io.File);

var foo = File('/tmp/');
dirlist = foo.list();

for (var i = 0; i < dirlist.length; i++) {
    print(dirlist[i]);
}
