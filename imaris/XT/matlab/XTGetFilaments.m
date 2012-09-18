%
%  Filaments Sandbox for Imaris 7
%

17

conn = IceImarisConnector();
conn.startImaris();

questdlg('Please open a dataset and select a Filament object!');
% but = warndlg('Please open a dataset and select a Filament object!', 'Waiting for Imaris', 'modal');

vImarisApplication = conn.mImarisApplication;
vFactory = vImarisApplication.GetFactory;
vFilaments = vFactory.ToFilaments(vImarisApplication.GetSurpassSelection);
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
	
vFilamentsXYZ = vFilaments.GetPositionsXYZ(0);
vFilamentsXYZ

csvwrite('h:\bla.csv', vFilamentsXYZ)