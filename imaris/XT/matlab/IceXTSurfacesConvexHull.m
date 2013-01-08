%
%  Surfaces Convex Hull calculation for Imaris 7 by Niko Ehrenfeuchter
%
%  Requirements:
%    - IceImarisConnector (https://github.com/aarpon/IceImarisConnector)
% 
%    <CustomTools>
%      <Menu>
%       <Submenu name="Surfaces Functions">
%        <Item name="Surfaces Convex Hull" icon="Matlab" tooltip="Create a Surface which contains the convex hull of the selected Surfaces.">
%          <Command>MatlabXT::IceXTSurfacesConvexHull(%i)</Command>
%        </Item>
%       </Submenu>
%      </Menu>
%      <SurpassTab>
%        <SurpassComponent name="bpSurfaces">
%          <Item name="Convex Hull">
%            <Command>MatlabXT::IceXTSurfacesConvexHull(%i)</Command>
%          </Item>
%        </SurpassComponent>
%      </SurpassTab>
%    </CustomTools>
%

function IceXTSurfacesConvexHull(mImarisApplication)
	% internal version number
	ver = 4;

	if nargin == 1
        conn = IceImarisConnector(mImarisApplication);
    else
        % start Imaris and set up the connection
        conn = IceImarisConnector();
        conn.startImaris();

        % wait until the connection is ready and some data is selected
        msg = ['Click "OK" to continue after opening a dataset and ', ...
            'selecting a Surface object.'];
        ans = questdlg(msg, 'Waiting for Imaris...', 'OK', 'Cancel', 'OK');
        if strcmp(ans, 'Cancel')
            return;
        end
    end

    calculateSurfacesConvexHull(conn.mImarisApplication);
end

function calculateSurfacesConvexHull(vImApp)
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
    
    % create a new surfaces object:
    vSurfaceHull = vFactory.CreateSurfaces;
    
    % NOTE: GetNumberOfSurfaces returns the number of surfaces in this
    % surface object, NOT the number of surface objects in the scene
		
    % extract positions of surface points for each and store them
	for SurfaceID = 0:(vSurfaces.GetNumberOfSurfaces - 1)
		% extract the vertices coordinates
        vSurfaceVertices = vSurfaces.GetVertices(SurfaceID);
        vConvexHull = convhulln(double(vSurfaceVertices));
        
        % For an Imaris surface objects we also need the triangles, but the
        % convhulln() gives us just the indices of the vertex coordinates,
        % so we need to select the edges from the original surface.
        % first, we create an array of the size of the original vertices,
        % setting all values to false:
        vNumberOfPoints = size(vSurfaceVertices, 1);
        vPoints = false(vNumberOfPoints, 1);
        % next, set the indices of those belonging to the hull to true:
        vPoints(vConvexHull(:)) = true;
        % get their correspoding index number:
        vPoints = find(vPoints);
        % and finally use the index numbers to copy those vertices:
        vVertices = vSurfaceVertices(vPoints, :);
        
        % FIXME: explain these steps in detail!
        % remap vertex indices to our selection
        % and reorder triangle vertices (clockwise to counter)
        vPointsMap = zeros(vNumberOfPoints, 1);
        vPointsMap(vPoints) = 1:numel(vPoints);
        vTriangles = vPointsMap(vConvexHull(:, [1, 3, 2])) - 1;
        
        % generate normals by calculating the center and then the vectors
        % from there to the individual vertices:
        vMean = mean(vVertices, 1);
        vNormals = [vVertices(:, 1) - vMean(1), ...
                    vVertices(:, 2) - vMean(2), ...
                    vVertices(:, 3) - vMean(3)];
        % NOTE: it is not required to normalize the normal vectors since
        % apparently Imaris does this for us.
        
        % remember the time index
        vIndexT = vSurfaces.GetTimeIndex(SurfaceID);
        
        % add the new surface to the Imaris Surfaces object
        vSurfaceHull.AddSurface(vVertices, vTriangles, vNormals, vIndexT);
    end
    
    % set a name for the new Surfaces object:
    vSurfaceHull.SetName(['Convex Hull of ', char(vSurfaces.GetName)]);
    vSurfaceHull.SetColorRGBA(vSurfaces.GetColorRGBA);
    vSurfaces.GetParent.AddChild(vSurfaceHull, -1)
end


