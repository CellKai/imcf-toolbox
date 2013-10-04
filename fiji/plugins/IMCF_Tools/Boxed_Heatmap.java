import ij.IJ;

import ij.plugin.PlugIn;

public class Boxed_Heatmap implements PlugIn {
	public void run(String arg) {
		try {
			new Jython.Refresh_Jython_Scripts().runScript(getClass()
				.getResource("Boxed_Heatmap.py").openStream());
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
