import ij.IJ;

import ij.plugin.PlugIn;

public class Overview_movie implements PlugIn {
	public void run(String arg) {
		try {
			new CLI.Refresh_Macros().runScript(getClass()
				.getResource("Overview_movie.ijm").openStream());
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
