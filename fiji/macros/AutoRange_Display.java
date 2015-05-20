import ij.IJ;

import ij.plugin.PlugIn;

public class AutoRange_Display implements PlugIn {
	public void run(String arg) {
		try {
			new CLI.Refresh_Macros().runScript(getClass()
				.getResource("AutoRange_Display.ijm").openStream());
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
