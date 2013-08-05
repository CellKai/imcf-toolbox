"""Region based average intensities calculation.

Create intensity heat-maps for single-channel images."""

from ij.plugin import Duplicator

def rect_avg(proc, start_x, start_y, dx, dy):
    """Calculate average intensity of a rectangular area.

    Parameters
    ----------
    proc : ImageProcessor
    start_x, start_y : int
        The starting coordinates of the rectangle.
    dx, dy : int
        The width and height of the rectangle.

    Returns
    -------
    avg : int
        The average intensity.
    """
    bsum = 0
    for y in range(start_y, start_y + dy):
        for x in range(start_x, start_x + dx):
            bsum += proc.getPixel(x, y)
            # print "[%d, %d] = %d" % (x, y, proc.getPixel(x, y))
    avg = bsum / (dx * dy)
    return avg

def rect_set(proc, start_x, start_y, dx, dy, val):
    """Paint a rectangular area with a given value.

    Parameters
    ----------
    proc : ImageProcessor
    start_x, start_y : int
        The starting coordinates of the rectangle.
    dx, dy : int
        The width and height of the rectangle.
    val : int
        The value to use for painting.
    """
    for y in range(start_y, start_y + dy):
        for x in range(start_x, start_x + dx):
            proc.putPixel(x, y, val)


imp1 = WindowManager.getCurrentImage()
imp2 = Duplicator().run(imp1)
imp2.setTitle('heatmap-' + imp1.getTitle())

imw = imp1.getWidth()
imh = imp1.getHeight()

boxw = 32
boxh = 32

ip1 = imp1.getProcessor()
ip2 = imp2.getProcessor()

if (imw % boxw + imh % boxh) > 0:
    msg = "WARNING: image size (%dx%d) is not a multiple of box size (%dx%d)!"
    print msg % (imw, imh, boxw, boxh)

for box_y in range(0, imh / boxh):
    start_y = box_y * boxh
    for box_x in range(0, imw / boxw):
        start_x = box_x * boxw
        # print "%d %d" % (start_x, start_y)
        bavg = rect_avg(ip1, start_x, start_y, boxw, boxh)
        # print bavg
        rect_set(ip2, start_x, start_y, boxw, boxh, bavg)

imp2.show()
