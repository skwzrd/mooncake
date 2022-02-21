import os

translations_filename = 'chinese_hsk_level_1_to_6.csv'

directory = os.path.abspath(os.path.dirname(__file__))

translations_directory = os.path.join(directory, '..', 'translations')
download_directory = os.path.join(directory, '..', 'audio', 'vocabulary')

log_directory = os.path.join(directory, 'log')
