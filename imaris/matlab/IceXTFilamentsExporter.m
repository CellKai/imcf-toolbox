%
%  Filaments Exporter for Imaris 7 by Niko Ehrenfeuchter
%
%  Requirements:
%	- IceImarisConnector (https://github.com/aarpon/IceImarisConnector)
%
%%% Imaris meta information %%%
% <CustomTools>
%  <Menu>
%   <Submenu name="Filaments Functions">
%	<Item name="Filaments Exporter" icon="Matlab"
%	   tooltip="Export points of selected Filaments to CSV.">
%	  <Command>MatlabXT::IceXTFilamentsExporter(%i)</Command>
%	</Item>
%   </Submenu>
%  </Menu>
%  <SurpassTab>
%	<SurpassComponent name="bpFilaments">
%	  <Item name="Export Filaments to CSV">
%		<Command>MatlabXT::IceXTFilamentsExporter(%i)</Command>
%	  </Item>
%	</SurpassComponent>
%  </SurpassTab>
% </CustomTools>

function IceXTFilamentsExporter(mImarisApplication)
	ver = 32;	% internal version number
	
	if nargin == 1
        javaaddpath ImarisLib.jar;
		% mImarisApplication
		conn = IceImarisConnector(mImarisApplication);
    else
        % fprintf('No ImarisID given, trying to start the application\n');
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
		
	% FIXME: this works only on windows
	home = getenv('USERPROFILE');
	oldpwd = cd(home);

	% extract positions of filament points for each and store them
	for FilamentID = 0:(vFilaments.GetNumberOfFilaments - 1)
		vFilamentsXYZ = vFilaments.GetPositionsXYZ(FilamentID);
		fname = sprintf('filaments-%d.csv', FilamentID);
		[fname, fpath] = uiputfile(fname, 'Save Filament as CSV file');
		csvwrite(fullfile(fpath, fname), vFilamentsXYZ);
	end
	
	cd(oldpwd);

end
