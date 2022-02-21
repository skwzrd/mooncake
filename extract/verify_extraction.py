import pandas as pd
import os
from glob import glob
from config import (
    translations_directory,
    translations_filename,
    download_directory,
)


def check_for_duplicates(mp3_files, df_translations):
    mp3_character_count = len(mp3_files)
    translation_character_count = len(df_translations['chinese'].drop_duplicates())
    if mp3_character_count != translation_character_count:
        raise ValueError(mp3_character_count, '!=', translation_character_count)


def compare_characters(mp3_files, df_translations):
    set_of_characters = set(df_translations['chinese'])

    errors = False
    for mp3_file in mp3_files:
        if not mp3_file in set_of_characters:
            print(f'{mp3_file}.mp3 not in translation listing.')
            errors = True

    for character in set_of_characters:
        if character not in mp3_files:
            print(f'{character} doesn\'t have an mp3.')
            errors = True

    if errors:
        raise ValueError('Check output for errors.')


def main():
    mp3_files = [
        os.path.basename(mp3_file).replace('.mp3', '')
        for mp3_file in glob(os.path.join(download_directory, '*.mp3'))
    ]
    df = pd.read_csv(os.path.join(translations_directory, translations_filename))

    # should be the same - no duplicates in the translations and no missing mp3 files.
    check_for_duplicates(mp3_files, df)
    compare_characters(mp3_files, df)


if __name__ == '__main__':
    main()
