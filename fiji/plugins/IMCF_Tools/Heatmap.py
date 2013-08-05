"""Region based average intensities calculation."""

from ij.plugin import Duplicator

def rect_avg(proc, startx, starty, dx, dy):
    """Calculate average intensity of a rectangular area.

    Parameters
    ----------
    proc : ImageProcessor
    startx, starty : int
        The starting coordinates of the rectangle.
    dx, dy : int
        The width and height of the rectangle.

    Returns
    -------
    avg : int
        The average intensity.
    """
    bsum = 0
    for y in range(starty, dy):
        for x in range(startx, dx):
            bsum += proc.getPixel(x, y)
            # print "[%d, %d] = %d" % (x, y, ip.getPixel(x, y))
    avg = bsum / (dx * dy)
    return avg

def rect_set(proc, startx, starty, dx, dy, val):
    """Paint a rectangular area with a given value.

    Parameters
    ----------
    proc : ImageProcessor
    startx, starty : int
        The starting coordinates of the rectangle.
    dx, dy : int
        The width and height of the rectangle.
    val : int
        The value to use for painting.
    """
    for y in range(starty, dy):
        for x in range(startx, dx):
            proc.putPixel(x, y, val)


imp1 = WindowManager.getCurrentImage()
imp2 = Duplicator().run(imp1)

imw = imp1.getWidth()
imh = imp1.getHeight()

boxw = 32
boxh = 32

ip1 = imp1.getProcessor()
ip2 = imp2.getProcessor()

bavg = rect_avg(ip1, 0, 0, boxw, boxh)
print bavg
rect_set(ip2, 0, 0, boxw, boxh, bavg)

imp2.show()
