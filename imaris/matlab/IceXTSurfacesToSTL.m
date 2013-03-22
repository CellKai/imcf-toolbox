
javaaddpath ImarisLib.jar;
conn = IceImarisConnector();
conn.startImaris();
msg = ['Click "OK" to continue after opening a dataset and ', ...
            'selecting a Surface object.'];
ans = questdlg(msg, 'Waiting for Imaris...', 'OK', 'Cancel', 'OK');
if strcmp(ans, 'Cancel')
	return;
end

vImApp = conn.mImarisApplication;



vFactory = vImApp.GetFactory;
vSurfaces = vFactory.ToSurfaces(vImApp.GetSurpassSelection);

% vFactory.IsSurfaces(vSurfaces)
% vSurfaces.GetNumberOfSurfaces

vTri = vSurfaces.GetTriangles(0);
vNormals = vSurfaces.GetNormals(0);
vVertices = vSurfaces.GetVertices(0);

fname = 'surface.stl';
[fname, fpath] = uiputfile(fname, 'Select a file name for the surface export');
fid = fopen([fpath fname], 'w');
fprintf(fid, 'solid imssurface\n');
for tri = 1:length(vTri)
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