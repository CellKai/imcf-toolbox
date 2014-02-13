from ij.io import DirectoryChooser, OpenDialog
from fiji.scripting import Script_Editor

# Choose a directory with lots of tif stacks
# dc = DirectoryChooser("Choose directory with stacks")
# srcDir = dc.getDirectory()

# fc = OpenDialog("asdffdsa")

#print(fc.getDirectory())
#print(fc.getFileName())

se = Script_Editor()
te = se.getInstance()
textarea = te.getTextArea()
te.append(textarea, 'asdfasdfasdf\n')