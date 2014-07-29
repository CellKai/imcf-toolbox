/* Javascript to test JFreeChart functionality */

importPackage(Packages.ij);
 
importPackage(Packages.org.jfree.chart);
importPackage(Packages.org.jfree.chart.plot);
importPackage(Packages.org.jfree.chart.axis);
importPackage(Packages.org.jfree.chart.encoders);
importPackage(Packages.org.jfree.chart.renderer.category);
 
importPackage(Packages.java.awt);
importPackage(Packages.java.awt.geom);
importPackage(Packages.java.io);
 
importPackage(Packages.org.jfree.ui);
importPackage(Packages.org.jfree.data.category);
importPackage(Packages.org.jfree.data.statistics);
 
importPackage(Packages.org.apache.batik.dom);
importPackage(Packages.org.apache.batik.svggen);
 
var dataset = new DefaultStatisticalCategoryDataset();
 
// dataset.add(Mean, StdDev, "Series", "Condition")
dataset.add(15.0, 2.4, "Row 1", "Column 1");
dataset.add(15.0, 4.4, "Row 1", "Column 2");
dataset.add(13.0, 2.1, "Row 1", "Column 3");
dataset.add(7.0, 1.3, "Row 1", "Column 4");
dataset.add(2.0, 2.4, "Row 2", "Column 1");
dataset.add(18.0, 4.4, "Row 2", "Column 2");
dataset.add(28.0, 2.1, "Row 2", "Column 3");
dataset.add(17.0, 1.3, "Row 2", "Column 4");
 
var chart = ChartFactory.createLineChart(
    null,                   // chart title
    "Treatment",                // domain axis label
    "Measurement",              // range axis label
    dataset,                // data
    PlotOrientation.VERTICAL,       // orientation
    false,                  // include legend
    true,                   // tooltips
    false                   // urls
);
 
// set the background color for the chart...
chart.setBackgroundPaint(Color.white);
 
var plot = chart.getPlot();
plot.setBackgroundPaint(Color.white);
plot.setRangeGridlinesVisible(false);
plot.setAxisOffset(RectangleInsets.ZERO_INSETS);
 
// customise the range axis...
var rangeAxis = plot.getRangeAxis();
rangeAxis.setStandardTickUnits(NumberAxis.createIntegerTickUnits());
rangeAxis.setAutoRangeIncludesZero(true);
rangeAxis.setRange(0, 40);
 
// customise the renderer...
var renderer = new StatisticalBarRenderer();
renderer.setErrorIndicatorPaint(Color.black);
renderer.setSeriesOutlinePaint(0,Color.black);
renderer.setSeriesOutlinePaint(1,Color.black);
renderer.setSeriesPaint(0,Color.black);
renderer.setSeriesPaint(1,Color.white);
renderer.setItemMargin(0.0);
plot.setRenderer(0,renderer);
 
renderer.setDrawBarOutline(true);
 
bi = chart.createBufferedImage(600, 400);
 
imp = new ImagePlus("Chart Test", bi);
imp.show();
 
// Create SVG image
// Get a DOMImplementation and create an XML document
var domImpl = GenericDOMImplementation.getDOMImplementation();
var document = domImpl.createDocument(null, "svg", null);
 
// Create an instance of the SVG Generator
var svgGenerator = new SVGGraphics2D(document);
 
// draw the chart in the SVG generator
var bounds = new Rectangle(600, 400);
chart.draw(svgGenerator, bounds);
 
var dir = IJ.getDirectory("Where should the svg file be saved?");
// Write svg file
var svgFile = new File(dir + "test.svg");
var outputStream = new FileOutputStream(svgFile);
var out = new OutputStreamWriter(outputStream, "UTF-8");
svgGenerator.stream(out, true /* use css */);
outputStream.flush();
outputStream.close();
