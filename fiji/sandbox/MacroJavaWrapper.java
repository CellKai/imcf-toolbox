import ij.IJ;

import ij.plugin.PlugIn;

public class InteractiveROIManager implements PlugIn {
	public void run(String arg) {
		try {
			new CLI.Refresh_Macros().runScript(getClass()
				.getResource("InteractiveROIManager.ijm").openStream(), arg);
		} catch (Exception e) {
			IJ.handleException(e);
		}
	}
}
