
'''
import cdstoolbox as ct

@ct.application(title='Hello World!')
@ct.output.figure()
@ct.output.download()
def application():

    data = ct.catalogue.retrieve(
        'seasonal-monthly-single-levels',
        {
            'originating_centre': 'ecmwf',
            'variable': '2m_temperature',
            'product_type': 'ensemble_mean',
            'year': '2018',
            'month': ['02'],
            'leadtime_month': ['1'],
        }
    )

    fig = ct.cdsplot.geomap(
        data, pcolormesh_kwargs={'cmap': 'RdBu_r'}, title='Mean {long_name}',
        projection=ct.cdsplot.crs.Robinson()
    )

    return fig, data
'''


import cdstoolbox as ct

@ct.application(title='Download data')
@ct.output.download()
def download_application():
    data = ct.catalogue.retrieve(
        'satellite-land-cover',
        {
            'variable': 'all',
            'year': '2018',
            'grid': [2,2],
            'version': 'v2.1.1',
        }
    )
    return data

data = download_application()
print(type(data))

'''
import cdstoolbox as ct
@ct.application(title='Example application workflow')
@ct.output.livemap()
def example_application(data_variable):
    temperature, cloud = ct.catalogue.retrieve(
        'reanalysis-era5-single-levels',
        {
            'variable': [
                '2m_temperature', 'high_cloud_cover'
            ],
            'product_type': 'reanalysis',
            'year': '2011',
            'month': '6',
            'day': '27',
            'time': '18:00'
        }
    )
    plot = ct.livemap.plot([temperature, cloud])
    return temperature, cloud
#plot = ct.livemap.plot([temperature, cloud])
'''