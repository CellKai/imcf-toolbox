import ij.IJ;

import ij.plugin.PlugIn;

public class Segmentation_3ch_ZVI implements PlugIn {
	public void run(String arg) {
		try {
			new CLI.Refresh_Macros().runScript(getClass()
				.getResource("Segmentation_3ch_ZVI.ijm").openStream());
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
