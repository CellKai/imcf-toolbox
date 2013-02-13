%
%  Filaments Exporter for Imaris 7 by Niko Ehrenfeuchter
%
%  Requirements:
%    - IceImarisConnector (https://github.com/aarpon/IceImarisConnector)
%

function IceXTFilamentsExporter(mImarisApplication)
    % internal version number
    ver = 29;

    if nargin == 1
        conn = IceImarisConnector(mImarisApplication);
    else
        % start Imaris and set up the connection
        conn = IceImarisConnector();
        conn.startImaris();

        % wait until the connection is ready and some data is selected
        msg = ['Click "OK" to continue after opening a dataset and ', ...
            'selecting a Filament object.'];
        ans = questdlg(msg, 'Waiting for Imaris...', 'OK', 'Cancel', 'OK');
        if strcmp(ans, 'Cancel')
            return;
        end
    end

    exportFilaments(conn.mImarisApplication);
end

function exportFilaments(vImApp)
	vFactory = vImApp.GetFactory;
	vFilaments = vFactory.ToFilaments(vImApp.GetSurpassSelection);
	vSurpassScene = vImApp.GetSurpassScene;

	if ~vFactory.IsFilaments(vFilaments)
		for vChildIndex = 1:vSurpassScene.GetNumberOfChildren
			vDataItem = vSurpassScene.GetChild(vChildIndex - 1);
			if vFactory.IsFilaments(vDataItem)
				vFilaments = vFactory.ToFilaments(vDataItem);
				break;
			end
		end
		
		% check if there was a filament at all
		if isequal(vFilaments, [])
			msgbox('Could not find any Filaments!');
			return;
		end
	end
		
    % extract positions of filament points for each and store them
	for FilamentID = 0:(vFilaments.GetNumberOfFilaments - 1)
		vFilamentsXYZ = vFilaments.GetPositionsXYZ(FilamentID);
		fname = sprintf('filaments-%d.csv', FilamentID);
		csvwrite(fname, vFilamentsXYZ)
	end

end
