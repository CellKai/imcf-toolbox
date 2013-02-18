%
% Surface growing for Imaris 7 by Niko Ehrenfeuchter
%
% Requirements:
%    - IceImarisConnector (https://github.com/aarpon/IceImarisConnector)
% 
%%% Imaris meta information %%%
% <CustomTools>
%  <Menu>
%   <Submenu name="Surfaces Functions">
%    <Item name="Surfaces Growing" icon="Matlab"
%       tooltip="Grow Isosurfaces along their normal vectors.">
%      <Command>MatlabXT::IceXTSurfacesGrowing(%i)</Command>
%    </Item>
%   </Submenu>
%  </Menu>
%  <SurpassTab>
%    <SurpassComponent name="bpSurfaces">
%      <Item name="Surfaces Growing">
%        <Command>MatlabXT::IceXTSurfacesGrowing(%i)</Command>
%      </Item>
%    </SurpassComponent>
%  </SurpassTab>
% </CustomTools>

function IceXTSurfacesGrowing(mImarisApplication)
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

    growSurfaces(conn.mImarisApplication);
end

function growSurfaces(vImApp)
%     vFactory = vImApp.GetFactory;
%     vSurfaces = vFactory.ToSurfaces(vImApp.GetSurpassSelection);
%     vSurpassScene = vImApp.GetSurpassScene;
%     vSurfaceHull = vFactory.CreateSurfaces;
%     vSurfaces.GetNumberOfSurfaces
%     SurfaceID = 0
%     vSurfaceVertices = vSurfaces.GetVertices(SurfaceID);
%     vMean = mean(vSurfaceVertices, 1)
%     vVertices = vSurfaceVertices;
%     vNormals = [vVertices(:, 1) - vMean(1), ...
%                 vVertices(:, 2) - vMean(2), ...
%                 vVertices(:, 3) - vMean(3)];
%     vVerticesNew = vVertices + vNormals;
%     vTriangles = vSurfaces.GetTriangles;
%     vTriangles = vSurfaces.GetTriangles(SurfaceID);
%     vSurfaceHull.AddSurface(vVerticesNew, vTriangles, vNormals, vIndexT)
%     vSurfaceHull.SetName(['Normal-increased ', char(vSurfaces.GetName)])
%     vSurfaceHull.SetColorRGBA(vSurfaces.GetColorRGBA);
%     vSurfaces.GetParent.AddChild(vSurfaceHull, -1)
end

