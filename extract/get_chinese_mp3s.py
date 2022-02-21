import pandas as pd
import os
import requests
import json
from time import sleep
from tqdm import tqdm
import logging
from config import (
    log_directory,
    translations_filename,
    translations_directory,
    download_directory,
)


logging.basicConfig(
    handlers=[
        logging.FileHandler(
            filename=os.path.join(log_directory, 'download.log'),
            encoding='utf-8',
            mode='a+',
        )
    ],
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def get_translations(filepath):

    is_valid_file = os.path.isfile(filepath)

    if is_valid_file:
        df = pd.read_csv(filepath)
    else:
        raise FileNotFoundError(filepath)

    return df


def make_mp3_filename(character):
    return f'{character}.mp3'


def character_downloaded(character):
    return os.path.isfile(
        os.path.join(download_directory, make_mp3_filename(character))
    )


def get_characters_not_downloaded(unfiltered_characters):
    characters = []
    for character in unfiltered_characters:
        if not character_downloaded(character):
            characters.append(character)
    return characters


def get_characters(translations, n=None):
    if n is None:
        unfiltered_characters = translations['chinese'].to_list()
    else:
        unfiltered_characters = translations.head(n)['chinese'].to_list()

    return get_characters_not_downloaded(unfiltered_characters)


def download_mp3(character, url):
    r = requests.get(url)
    filepath = os.path.join(download_directory, make_mp3_filename(character))
    with open(filepath, 'wb') as f:
        f.write(r.content)
    logging.info(f'Retreived: {character}')


def get_source_id_url_and_mp3(character, source_id):
    url = 'https://api.soundoftext.com/sounds/' + str(source_id)

    max_dl_attempts = 3
    seconds_between_attempts_multiplier = 5

    for i in range(0, max_dl_attempts):

        r = requests.get(url)
        res = json.loads(r.content)

        location = res.get('location', None)
        if location is not None:
            download_mp3(character, location)
            return

        status = res.get('status', None)
        time_to_wait = seconds_between_attempts_multiplier * i

        logging.info(f'Status: {status}. Attempting again in {time_to_wait} seconds.')
        sleep(time_to_wait)


def get_source_id(character):
    url = 'https://api.soundoftext.com/sounds'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {"engine": "Google", "data": {"text": character, "voice": "cmn-Hant-TW"}}

    r = requests.post(url, json=data, headers=headers)
    res = json.loads(r.content)

    return res.get('id', None)


def main():
    time_between_character_retrievals = 0.1

    characters = get_characters(
        get_translations(os.path.join(translations_directory, translations_filename))
    )

    t = tqdm(characters)
    for character in t:
        t.set_description(f'Downloading mp3 for: {character}')
        logging.info(f'Fetching: {character}')
        source_id = get_source_id(character)
        if source_id:
            get_source_id_url_and_mp3(character, source_id)

        sleep(time_between_character_retrievals)


if __name__ == '__main__':
    main()
