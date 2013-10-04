import ij.IJ;

import ij.plugin.PlugIn;

public class Save_all_images implements PlugIn {
	public void run(String arg) {
		try {
			new Jython.Refresh_Jython_Scripts().runScript(getClass()
				.getResource("Save_all_images.py").openStream());
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
