"""Region based average intensities calculation."""

from ij.plugin import Duplicator

imp1 = WindowManager.getCurrentImage()
imp2 = Duplicator().run(imp1)

imw = imp1.getWidth()
imh = imp1.getHeight()

boxw = 32
boxh = 32

ip1 = imp1.getProcessor()
ip2 = imp2.getProcessor()

bsum = 0
for y in range(0, boxh):
    for x in range(0, boxw):
        bsum += ip1.getPixel(x, y)
        # print "[%d, %d] = %d" % (x, y, ip.getPixel(x, y))
bavg = bsum / (boxh * boxw)
print bavg
for y in range(0, boxh):
    for x in range(0, boxw):
        ip2.putPixel(x, y, bavg)

imp2.show()
