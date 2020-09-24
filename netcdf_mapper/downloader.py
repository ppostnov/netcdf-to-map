import cdsapi
import zipfile


class FileRecipient(object):
    """
    """

    def __init__(self):
        self.c = cdsapi.Client()

    def download(self, year: str, filename: str) -> object:
        self.c.retrieve(
            'satellite-land-cover',
            {
                'variable': 'all',
                'format': 'zip',
                'version': 'v2.1.1',
                'year': '2018',
            },
            f'data\\{filename}.zip'
        )

    def unzipper(self, filename: str):
        with zipfile.ZipFile(f'data\\{filename}.zip', 'r') as zip_ref:
            zip_ref.extractall('data')

    def clearner(self):
        pass

    def parser(self):
        pass    

    def execute(self):
        pass
