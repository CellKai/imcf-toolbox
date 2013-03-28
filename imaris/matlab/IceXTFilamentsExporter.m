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
        % start Imaris and set up the connection
		conn = IceImarisConnector();
		conn.startImaris();
	end

	% if called from matlab using an existing connection (useful for
	% debugging), it is better to do some sanity checks first:
	if ~conn.isAlive
		fprintf('Error: no connection to Imaris!\n');
		return;
	end
	vImApp = conn.mImarisApplication;
	fprintf('connection ID: %s\n', char(vImApp));
	while ~vImApp.GetFactory.IsFilaments(vImApp.GetSurpassSelection)
		msg = 'Select a FILAMENTS object in Imaris!';
		title = 'Selection required';
		ans = questdlg(msg, title, 'OK', 'Cancel', 'OK');
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
