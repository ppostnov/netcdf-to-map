import cdsapi


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
