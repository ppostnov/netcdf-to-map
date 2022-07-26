from netcdf_mapper import downloader

# the example how download the data for one year
d = downloader.FileRecipient()
d.download('2018', '2018-test')
