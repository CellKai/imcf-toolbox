"""Region based average intensities calculation.

Create region based (rectangles) intensity heat-maps
for single-channel images.
"""

from ij.plugin import Duplicator
from ij.gui import GenericDialog


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


def get_options():
    """Ask user for input values."""
    gd = GenericDialog("Options for Boxed Heatmap")
    gd.addMessage("Boxed Heatmap settings")
    gd.addMessage("Specify box size:")
    gd.addNumericField("Width", 32, 0)
    gd.addNumericField("Height", 32, 0)
    gd.showDialog()
    if gd.wasCanceled():
        print "User canceled dialog!"
        return  None
    # Read out the options
    boxw = int(gd.getNextNumber())
    boxh = int(gd.getNextNumber())
    return boxw, boxh


def boxed_intensities(imp1, width, height):
    """Create a new image with averaged intensity regions.

    Parameters
    ----------
    imp1 : ImagePlus
    width, height : int
        The width and height of the rectangles.

    Returns
    -------
    imp2 : ImagePlus
        The resulting ImagePlus, same dimensions as imp1.
    """
    imp2 = Duplicator().run(imp1)
    imp2.setTitle('heatmap-' + imp1.getTitle())

    imw = imp1.getWidth()
    imh = imp1.getHeight()

    ip1 = imp1.getProcessor()
    ip2 = imp2.getProcessor()

    if (imw % boxw + imh % boxh) > 0:
        msg = "WARNING: image size (%dx%d) not dividable by box (%dx%d)!"
        print msg % (imw, imh, boxw, boxh)

    for box_y in range(0, imh / boxh):
        start_y = box_y * boxh
        for box_x in range(0, imw / boxw):
            start_x = box_x * boxw
            # print "%d %d" % (start_x, start_y)
            bavg = rect_avg(ip1, start_x, start_y, boxw, boxh)
            # print bavg
            rect_set(ip2, start_x, start_y, boxw, boxh, bavg)

    return imp2


def main():
    """Get options and create new image."""
    options = get_options()
    if options is not None:
        bwidth, bheight = options
        img_cur = WindowManager.getCurrentImage()
        img_new = boxed_intensities(img_cur, bwidth, bheight)
        img_new.show()


if __name__ == "__main__":
    main()
