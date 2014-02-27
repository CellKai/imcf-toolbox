import ij.IJ;

import ij.plugin.PlugIn;

public class Stitch_all_files_in_directory implements PlugIn {
	public void run(String arg) {
		try {
			new CLI.Refresh_Macros().runScript(getClass()
				.getResource("Stitch_all_files_in_directory.ijm").openStream());
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
