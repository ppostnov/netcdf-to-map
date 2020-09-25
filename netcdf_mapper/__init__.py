import logging

logging.basicConfig(
    format='%(levelname)-4s [%(asctime)s] (%(module)s.py)'
           + ' [def %(funcName)-5s()] --> %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)


class Absorber(Object):
    pass