import logging

logging.basicConfig(filename='stdout.log', filemode='w')

def warn(s):
  logging.warning(s)