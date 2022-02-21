# .mp3 Extraction

What does `get_chinese_mp3s.py` do?
- Uses `~/translations/chinese_hsk_level_1_to_6.csv` to gather a list of Chinese characters needing audio.
- Downloads a .mp3 for each character from the [Sound of Text](https://soundoftext.com/) API.
  - The time between requests can be tuned with the variable `time_between_character_retrievals`. The defaults wait time is 0.1 seconds.
- Saves .mp3s to `~/audio/vocabulary`.
- Outputs a download log in `~/log`.

What does `verify_extraction.py` do?
- Checks to see if each character in `~/translations/chinese_hsk_level_1_to_6.csv` has a .mp3.
- Ensures `~/audio/vocabulary` only contains .mp3s for Chinese characters in `~/translations/chinese_hsk_level_1_to_6.csv`.
- Verifies there are no duplicate translations.
