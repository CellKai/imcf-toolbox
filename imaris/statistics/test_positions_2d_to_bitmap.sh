INFILE="TESTDATA/spots_distances/spots_nocorners_ws-all.xml"
PREFIX="TESTDATA/spots_distances/spots_nocorners_bitmap"
./positions_2d_to_bitmap.py --size 256 -i $INFILE -o ${PREFIX}-cropped.csv --crop
./positions_2d_to_bitmap.py --size 256 -i $INFILE -o ${PREFIX}-uncropped.csv 

INFILE="TESTDATA/spots_distances/spots_allcorners_ws-all.xml"
PREFIX="TESTDATA/spots_distances/spots_allcorners_bitmap"
./positions_2d_to_bitmap.py --size 256 -i $INFILE -o ${PREFIX}-cropped.csv --crop
./positions_2d_to_bitmap.py --size 256 -i $INFILE -o ${PREFIX}-uncropped.csv 
