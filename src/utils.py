import os
import logging

logger = logging.getLogger(__name__)

def get_value_from_file(file_name):
    try:
        with open(file_name, 'r') as f:
            return f.readline().rstrip()
    except:
        return None