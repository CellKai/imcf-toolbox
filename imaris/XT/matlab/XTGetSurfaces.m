%
%  Surfaces Sandbox for Imaris 7 by Niko Ehrenfeuchter
%
%  Requirements:
%    - IceImarisConnector (https://github.com/aarpon/IceImarisConnector)
%

function XTGetSurfaces()
	ver = 28;
	
	% start Imaris and set up the connection
	conn = IceImarisConnector();
	conn.startImaris();

	% wait until the connection is ready and the user has selected some data
    msg = 'Click "OK" to continue after opening a dataset and selecting a Surface object.'
	ans = questdlg(msg, 'Waiting for Imaris...', 'OK', 'Cancel', 'OK')
	switch ans
		case 'OK'
			extractSurfaces(conn.mImarisApplication);
	end
end

function extractSurfaces(vImApp)
	vFactory = vImApp.GetFactory;
	vSurfaces = vFactory.ToSurfaces(vImApp.GetSurpassSelection);
	vSurpassScene = vImApp.GetSurpassScene;

	% check if a surface was selected in imaris:
    if ~vFactory.IsSurfaces(vSurfaces)
		% otherwise try all elements and take the first surface object:
        for vChildIndex = 1:vSurpassScene.GetNumberOfChildren
			vDataItem = vSurpassScene.GetChild(vChildIndex - 1);
			if vFactory.IsSurfaces(vDataItem)
				vSurfaces = vFactory.ToSurfaces(vDataItem);
				break;
			end
		end
		
		% check if there was a surface at all
		if isequal(vSurfaces, [])
			msgbox('Could not find any Surface!');
			return;
		end
    end
    
    % NOTE: GetNumberOfSurfaces returns the number of surfaces in this
    % surface object, NOT the number of surface objects in the scene
		
    % extract positions of surface points for each and store them
	for SurfaceID = 0:(vSurfaces.GetNumberOfSurfaces - 1)
		vSurfaceVertices = vSurfaces.GetVertices(SurfaceID);
        vSurfaceTriangles = vSurfaces.GetTriangles(SurfaceID);
		fname = sprintf('surface-%d-vertices.csv', SurfaceID);
		csvwrite(fname, vSurfaceVertices)
        fname = sprintf('surface-%d-triangles.csv', SurfaceID);
        csvwrite(fname, vSurfaceTriangles)
	end

end
