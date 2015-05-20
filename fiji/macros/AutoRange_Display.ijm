LUTs = newArray("Red", "Green", "Blue", "Cyan", "Magenta", "Yellow");

/*
getMinAndMax(min, max);
print("min: " + min);
print("max: " + max);
*/

getDimensions(width, height, channels, slices, frames);

Stack.setSlice(slices/2);
for (c=1; c<=channels; c++) {
	Stack.setChannel(c);
	run(LUTs[c-1]);
	run("Enhance Contrast", "saturated=0.35");
}

Stack.setDisplayMode("composite");

/*
getMinAndMax(min, max);
print("min: " + min);
print("max: " + max);
*/
