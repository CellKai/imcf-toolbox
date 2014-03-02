import ij.IJ;

import ij.plugin.PlugIn;

public class Stitch_directory_with_LSMs implements PlugIn {
	public void run(String arg) {
		try {
			new CLI.Refresh_Macros().runScript(getClass()
				.getResource("Stitch_directory_with_LSMs.ijm").openStream());
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
