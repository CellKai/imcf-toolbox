function update_focus_close_old(title) {
    print("attempting to close " + title);
    curfocus = getTitle();
    selectWindow(title);
    close();
    print("attempting to re-focus " + curfocus);
    selectWindow(curfocus);
    return curfocus;
}

print("******************");

getDimensions(im_width, im_height, im_channels, im_slices, im_frames);

focused = getTitle();
print("inital window " + getTitle());
run("Z Project...", "projection=[Max Intensity] all");
print("created window " + getTitle());
focused = update_focus_close_old(focused);
/*
winnew = getTitle();
print(winnew);
selectWindow(winold);
close()
print(getTitle());
selectWindow(winnew);
print(getTitle());
*/

for (c=1; c<=im_channels; c++) {
        Stack.setChannel(c);
        run("Enhance Contrast", "saturated=0.35");
}
