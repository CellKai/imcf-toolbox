import os
from timeit import default_timer as timer
from trainableSegmentation import WekaSegmentation
from ij import IJ

indir = "/scratch/data/__TESTFILES/weka"
modelfile = os.path.join(indir, "tissue_fibrotic_bg.model")

segmentator = WekaSegmentation()
segmentator.loadClassifier(modelfile)
### Field of view: max sigma = 16.0, min sigma = 0.0
### Membrane thickness: 1, patch size: 19
### Read class name: tissue
### Read class name: fibrotic
### Read class name: bg
### Error while adjusting data!

segmentator.enabledFeatures
### array('z', [True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False])

segmentator.getClassLabel(0)
### u'tissue'

segmentator.getClassLabel(1)
### u'fibrotic'

segmentator.getClassLabel(2)
### u'bg'

infile = os.path.join(indir, "1462_mko_ctx_1.tif")
input_image = IJ.openImage(infile)
result = segmentator.applyClassifier(input_image, 0, True)
### Traceback (most recent call last):
###   File "<string>", line 1, in <module>
###     at trainableSegmentation.WekaSegmentation.applyClassifier(WekaSegmentation.java:4408)
###     at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
###     at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:39)
###     at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25)
###     at java.lang.reflect.Method.invoke(Method.java:597)
### 
### java.lang.NullPointerException: java.lang.NullPointerException
### 
###     at org.python.core.PyException.fillInStackTrace(PyException.java:70)
###     at java.lang.Throwable.<init>(Throwable.java:181)
###     at java.lang.Exception.<init>(Exception.java:29)
###     at java.lang.RuntimeException.<init>(RuntimeException.java:32)
###     at org.python.core.PyException.<init>(PyException.java:46)
###     at org.python.core.PyException.<init>(PyException.java:43)
###     at org.python.core.Py.JavaError(Py.java:512)
###     at org.python.core.Py.JavaError(Py.java:505)
###     at org.python.core.PyReflectedFunction.__call__(PyReflectedFunction.java:188)
###     at org.python.core.PyReflectedFunction.__call__(PyReflectedFunction.java:204)
###     at org.python.core.PyObject.__call__(PyObject.java:457)
###     at org.python.core.PyObject.__call__(PyObject.java:463)
###     at org.python.core.PyMethod.__call__(PyMethod.java:166)
###     at org.python.pycode._pyx17.f$0(<string>:1)
###     at org.python.pycode._pyx17.call_function(<string>)
###     at org.python.core.PyTableCode.call(PyTableCode.java:165)
###     at org.python.core.PyCode.call(PyCode.java:18)
###     at org.python.core.Py.runCode(Py.java:1302)
###     at org.python.core.__builtin__.eval(__builtin__.java:480)
###     at org.python.core.__builtin__.eval(__builtin__.java:484)
###     at org.python.util.PythonInterpreter.eval(PythonInterpreter.java:198)
###     at Jython.Jython_Interpreter.eval(Jython_Interpreter.java:119)
###     at common.AbstractInterpreter.execute(AbstractInterpreter.java:659)
###     at common.AbstractInterpreter$ExecuteCode.run(AbstractInterpreter.java:559)
### Caused by: java.lang.NullPointerException
###     at trainableSegmentation.WekaSegmentation.applyClassifier(WekaSegmentation.java:4408)
###     at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
###     at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:39)
###     at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25)
###     at java.lang.reflect.Method.invoke(Method.java:597)
###     at org.python.core.PyReflectedFunction.__call__(PyReflectedFunction.java:186)
###     ... 15 more
