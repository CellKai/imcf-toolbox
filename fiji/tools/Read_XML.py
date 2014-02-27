import xml.parsers.expat as xp
# import xml.etree.ElementTree as etree

def start_element(name, attrs):
    print 'Start element:', name, attrs

def end_element(name):
    print 'End element:', name

def char_data(data):
    print 'Character data:', repr(data) 

xml_file = '/scratch/imageproc/data/paolo/FluoView_stitching/sample_experiment/MATL_Mosaic.log'

xmlp = xp.ParserCreate()

xmlp.StartElementHandler = start_element
xmlp.EndElementHandler = end_element
xmlp.CharacterDataHandler = char_data

xmlp.ParseFile(open(xml_file, 'r'))