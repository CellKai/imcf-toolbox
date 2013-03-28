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

	% extract positions of filament points for each and store them
	for FilamentID = 0:(vFilaments.GetNumberOfFilaments - 1)
		vFileName = vImApp.GetCurrentFileName;
		[fpath, fname, ext] = fileparts(char(vFileName));
		fname = sprintf('%s-filaments-%d.csv', fname, FilamentID);
		[fname, fpath] = uiputfile(fullfile(fpath, fname), ...
			'File name for the filaments export');
		if fname == 0
			fprintf('aborting due to user request\n');
			return;
		end
		fprintf('writing filament format to "%s"\n\n', [fpath fname]);

		vFilamentsXYZ = vFilaments.GetPositionsXYZ(FilamentID);
		csvwrite(fullfile(fpath, fname), vFilamentsXYZ);
	end
end
