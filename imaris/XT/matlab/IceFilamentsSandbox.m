%
% to use this in combination with IceImarisConnector, do this:
%   conn = IceImarisConnector();
%   conn.startImaris();
%   FilamentsSandbox(conn.mImarisApplication);


function FilamentsSandbox(vImarisApplication)

% vImarisApplication = conn.mImarisApplication;

% this will give the selected filament object
vFactory = vImarisApplication.GetFactory;
vFilaments = vFactory.ToFilaments(vImarisApplication.GetSurpassSelection);

% if no filament was selected we need to search for it
vSurpassScene = vImarisApplication.GetSurpassScene;
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

% vFilaments
% vFilamentIndex = 0:vFilaments.GetNumberOfFilaments - 1

% store the coordinates
vFilamentsXYZ = vFilaments.GetPositionsXYZ(0);

% vSurpassScene.GetChild(0)
% vFactory.IsFilaments(vSurpassScene.GetChild(3))
% vFactory.IsFilaments(vSurpassScene.GetChild(4))
% vFilaments = vFactory.ToFilaments(vImarisApplication.GetSurpassSelection)