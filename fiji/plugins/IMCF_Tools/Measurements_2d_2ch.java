import ij.IJ;

import ij.plugin.PlugIn;

public class Measurements_2d_2ch implements PlugIn {
	public void run(String arg) {
		try {
			new CLI.Refresh_Macros().runScript(getClass()
				.getResource("Measurements_2d_2ch.ijm").openStream());
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
