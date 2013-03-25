%
%  Surfaces to STL Exporter for Imaris 7 by Niko Ehrenfeuchter
%
%  Requirements:
%	- IceImarisConnector (https://github.com/aarpon/IceImarisConnector)
%
%%% Imaris meta information %%%
% <CustomTools>
%  <Menu>
%   <Submenu name="Surfaces Functions">
%	<Item name="Surfaces to STL Exporter" icon="Matlab"
%	   tooltip="Export selected Surfaces to STL.">
%	  <Command>MatlabXT::IceXTSurfacesToSTL(%i)</Command>
%	</Item>
%   </Submenu>
%  </Menu>
%  <SurpassTab>
%	<SurpassComponent name="bpSurfaces">
%	  <Item name="Export Surfaces to STL">
%		<Command>MatlabXT::IceXTSurfacesToSTL(%i)</Command>
%	  </Item>
%	</SurpassComponent>
%  </SurpassTab>
% </CustomTools>

function IceXTSurfacesToSTL(mImarisApplication)
	ver = 12;	% internal version number
	
	if nargin == 1
        javaaddpath ImarisLib.jar;
		% mImarisApplication
		conn = IceImarisConnector(mImarisApplication);
    else
        % start Imaris and set up the connection
		conn = IceImarisConnector();
		conn.startImaris();
		msg = ['Click "OK" to continue after opening a dataset and ', ...
					'selecting a Surface object.'];
		ans = questdlg(msg, 'Waiting for Imaris...', 'OK', 'Cancel', 'OK');
		if strcmp(ans, 'Cancel')
			return;
		end
	end

	exportSurfacesToSTL(conn.mImarisApplication);
end


function exportSurfacesToSTL(vImApp)
	vFactory = vImApp.GetFactory;
	vSurfaces = vFactory.ToSurfaces(vImApp.GetSurpassSelection);

	% vFactory.IsSurfaces(vSurfaces)
	% vSurfaces.GetNumberOfSurfaces
	% FIXME: iterate over all surfaces!

	vTri = vSurfaces.GetTriangles(0);
	vNormals = vSurfaces.GetNormals(0);
	vVertices = vSurfaces.GetVertices(0);

	fprintf('extracted %i individual triangles\n', length(vTri));

	% notification steps in percentage
	psteps = [ 5 10 25 50];
	nsteps = psteps * round(length(vTri) / 100);

	fname = 'surface.stl';
	[fname, fpath] = uiputfile(fname, 'Select a file name for the surface export');
	if fname == 0
		fprintf('aborting due to user request\n');
		return;
	end
	fprintf('writing STL format to "%s"\n', [fpath fname]);
	fid = fopen([fpath fname], 'w');
	fprintf(fid, 'solid imssurface\n');
	for tri = 1:length(vTri)
		% nid is the index of the current triangle in the nsteps array
		nid = find(nsteps == tri);
		% TODO: measure time and give an ETA
		if nid
			fprintf('%i%% completed (%i triangles)...\n', psteps(nid), tri)
		end
		vi = vTri(tri,:) + 1;
		fn = sum(vNormals(vi,:));
		fn = fn / norm(fn);
		tv = vVertices(vi,:);
		fprintf(fid, ['  facet normal ' num2str(fn, '%e %e %e') '\n' ...
		'    outer loop\n' ...
		'      vertex ' num2str(tv(1,:), '%e %e %e') '\n' ...
		'      vertex ' num2str(tv(2,:), '%e %e %e') '\n' ...
		'      vertex ' num2str(tv(3,:), '%e %e %e') '\n' ...
		'    endloop\n' ...
		'  endfacet\n']);
	end
	fprintf(fid, 'endsolid imssurface\n');
	fclose(fid);
end % exportSurfacesToSTL

% % tri=1
% vi = vTri(tri,:) + 1;
% fn = sum(vNormals(vi,:));
% fn = fn / norm(fn);
% tv = vVertices(vi,:);
% % num2str(tv(1,:))
% % num2str(tv(2,:))
% % num2str(tv(3,:))
% % tv
% % num2str(fn(:))
% % norm(fn)
% % num2str(fn)

% % sprintf(['solid bla\n' ...
% % '  facet normal ' num2str(fn) '\n' ...
% % '    outer loop\n' ...
% % '      vertex ' num2str(tv(1,:)) '\n' ...
% % '      vertex ' num2str(tv(2,:)) '\n' ...
% % '      vertex ' num2str(tv(3,:)) '\n' ...
% % '    endloop\n' ...
% % '  endfacet\n' ...
% % 'endsolid bla'])

% sprintf(['solid bla\n' ...
% '  facet normal ' num2str(fn, '%f %f %f') '\n' ...
% '    outer loop\n' ...
% '      vertex ' num2str(tv(1,:), '%f %f %f') '\n' ...
% '      vertex ' num2str(tv(2,:), '%f %f %f') '\n' ...
% '      vertex ' num2str(tv(3,:), '%f %f %f') '\n' ...
% '    endloop\n' ...
% '  endfacet\n' ...
% 'endsolid bla'])