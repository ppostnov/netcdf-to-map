"""
    Downloader, модуль отвечающий за загрузку и распаковку
    данных с copernicus.eu. Класс FileRecipient содержит
    два основных метода. Метод download() для загрузки
    данных, он принимает на вход payload body, который в
    свою очередь принимает значения четырех переменных -
    тип переменной из netcdf файла, формат файла для
    выгрузки, версию формата файла источника и год за
    который требуются данные. Метод unzip() обеспечивает
    автоматическое разархивирование из формата *.zip для
    полученных данных.
"""

import cdsapi
import zipfile
import logging


class FileRecipient(object):
    """
    """

    def __init__(self):
        self.c = cdsapi.Client()

    def download(self, year: str, filename: str, ver: str) -> object:
        self.c.retrieve(
            'satellite-land-cover',
            {
                'variable': 'all',
                'format': 'zip',
                'version': ver,
                'year': year,
            },
            f'data\\netcdf\\{filename}.zip'
        )

    def unzip(self, filename: str):
        logging.info(f'Unzipping {filename}...')
        with zipfile.ZipFile(f'data\\netcdf\\{filename}.zip', 'r') as zip_ref:
            zip_ref.extractall('data\\netcdf')
        logging.info('Unzip is complete')

    def clearner(self):
        pass

    def parser(self):
        pass

    def execute(self):
        pass
