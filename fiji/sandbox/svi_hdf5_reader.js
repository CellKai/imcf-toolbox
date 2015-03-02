importClass(Packages.HDF5ImageJ);
importClass(Packages.ch.systemsx.cisd.hdf5.HDF5Factory);
importClass(Packages.ch.systemsx.cisd.hdf5.IHDF5SimpleReader);
importClass(Packages.loci.formats.services.NetCDFService);
importClass(Packages.loci.common.services.ServiceFactory);

dir = '/home/ehrenfeu/imageproc/data/__TESTFILES/HDF5';
fname = '2014.02.28_DAPI_Phalloidin_aTub_06_Markerintro01_1_53109b472c0e0_hrm';
fext = '.h5';
dset = '/' + fname + '/ImageData/Image';

id = dir + '/' + fname + fext;
print(len(id));

reader = HDF5Factory.openForReading(id);
dsInfo = reader.object().getDataSetInformation(dset);
print('DataSetInformation: ' + dsInfo);

//var rawdata = reader.float32().readMDArray(dset).getAsFlatArray();



/*
factory = new ServiceFactory();
netcdf = factory.getInstance(NetCDFService);
netcdf.setFile(id);
*/

/*
HDF5ImageJ.loadCustomLayoutDataSetToHyperStack(
	dir + '/' + fname + fext,
	dset,
	'ctzyx'
);
*/