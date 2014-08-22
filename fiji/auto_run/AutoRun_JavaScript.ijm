// run all the .js scripts provided in /plugins/Scripts/AutoRun/
autoRunDirectory = getDirectory("imagej") + "/plugins/Scripts/AutoRun/";
if (File.isDirectory(autoRunDirectory)) {
    list = getFileList(autoRunDirectory);
    // make sure startup order is consistent
    Array.sort(list);
    for (i = 0; i < list.length; i++) {
        if (endsWith(list[i], ".js")) {
            runMacro(autoRunDirectory + list[i]);
        }
    }
}

