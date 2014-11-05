import ij.IJ;

import ij.plugin.PlugIn;

public class FluoView_OIF_OIB_Stitcher implements PlugIn {
	public void run(String arg) {
		try {
			new Jython.Refresh_Jython_Scripts().runScript(getClass()
				.getResource("FluoView_OIF_OIB_Stitcher.py").openStream());
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
