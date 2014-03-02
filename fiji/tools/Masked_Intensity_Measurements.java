import ij.IJ;

import ij.plugin.PlugIn;

public class Masked_Intensity_Measurements implements PlugIn {
	public void run(String arg) {
		try {
			new CLI.Refresh_Macros().runScript(getClass()
				.getResource("Masked_Intensity_Measurements.ijm").openStream());
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
