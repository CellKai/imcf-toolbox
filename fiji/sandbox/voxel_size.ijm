getDimensions(width, height, channels, slices, frames);

for (c=0; c<channels; c++) {
	setSlice((slices*channels)/2 + c);
	wait(500);
}
