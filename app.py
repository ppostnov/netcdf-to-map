from netcdf_mapper import downloader

# the example how download the data for one year
d = downloader.FileRecipient()
d.download('2008', '2008-test')
# d.unzipper('2018-test')
