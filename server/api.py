from typing import Dict
import pandas as pd
from flask import session  # sessions stored on server (objects permitted)
from db import query_db, query_db_df
from config import (
    default_study_session_type,
    default_hsk,
    default_size,
    default_user_id,
)


def get_df():
    sql_string = """select * from character;"""
    session['df'] = query_db_df(sql_string)
    return session['df']


def make_json(df=None) -> Dict[str, str]:
    if df is None:
        df = get_df()
    d = {}
    for i, row in enumerate(df.iterrows()):
        row = row[1]
        d[i] = {
            'index': row[0],
            'chinese': row[1],
            'pinyin': row[2],
            'english': row[3],
            'hsk': row[4],
        }
    return d


def filter_by_hsk(df, hsk: int = default_hsk):
    return df[df.hsk == hsk]


def get_new_characters(user_id, hsk, size):
    sql_string = """
    select *
    from character
    where character.id not in
    (
        select character.id
        from character
        left join stats on stats.character_id = character.id
        left join user on user.id = stats.user_id
        where
        stats.last_studied not null
        and user.id = ?
    )
    and character.hsk = ?
    order by random() limit ?;
    """
    params = [user_id, hsk, size]
    df = query_db_df(sql_string, params=params)
    if len(df) == 0:
        raise ValueError('No new characters to learn.')
    return df


def get_new_count(user_id, hsk):
    sql_string = """
    select count(character.id) as new_count
    from character
    where character.id not in
    (
        select character.id
        from character
        left join stats on stats.character_id = character.id
        left join user on user.id = stats.user_id
        where
        stats.last_studied not null
        and user.id = ?
    )
    and character.hsk = ?;
    """
    params = [user_id, hsk]
    new_count = query_db(sql_string, params, one_one=True)
    return new_count


def get_known_characters(user_id, hsk, size):
    if size == 0:
        return None
    sql_string = """
    select character.*
    from character
    left join stats on stats.character_id = character.id
    left join user on user.id = stats.user_id
    where
    stats.last_studied not null
    and user.id = ?
    and character.hsk = ?
    order by random() limit ?;
    """
    params = [user_id, hsk, size]
    df = query_db_df(sql_string, params=params)
    if len(df) == 0:
        raise ValueError('No known characters to learn.')
    return df


def get_known_count(user_id, hsk):
    sql_string = """
    select count(character.id) as known_count
    from character
    left join stats on stats.character_id = character.id
    left join user on user.id = stats.user_id
    where
    stats.last_studied not null
    and user.id = ?
    and character.hsk = ?;
    """
    params = [user_id, hsk]
    known_count = query_db(sql_string, params, one_one=True)
    return known_count


def get_hsk_count(hsk=None):
    sql_string = """
    select count(character.id) as hsk_count
    from character
    where character.hsk = ?;
    """
    if hsk is None:
        sql_string = """select count(character.id) as hsk_count from character;"""
    params = [hsk]
    hsk_count = query_db(sql_string, params, one_one=True)
    return hsk_count


class IQNotHighEnough(Exception):
    pass


def get_study_session(
    hsk=default_hsk, study_session_type=default_study_session_type, size=default_size
):
    user_id = default_user_id
    if study_session_type == 'new':
        df = get_new_characters(user_id, hsk, size)

    elif study_session_type == 'known':
        df = get_known_characters(user_id, hsk, size)

    elif study_session_type == 'equally_mixed':
        known_count = get_known_count(user_id, hsk)
        hsk_count = get_hsk_count(hsk)

        size = min(size, hsk_count)

        # if we can get it, we want half known and half new
        size_2 = size // 2
        if known_count == 0:
            known_size = 0
            new_size = size
        elif known_count <= size_2 and known_count > 0:
            known_size = known_count
            new_size = size - known_size
        elif known_count > size_2:
            known_size = size_2
            new_size = size - size_2
        else:
            raise IQNotHighEnough(known_count, hsk_count, size, size_2)

        if known_size + new_size != size:
            raise IQNotHighEnough(
                new_size, known_size, known_count, hsk_count, size, size_2
            )

        df_known = get_known_characters(user_id, hsk, known_size)
        df_new = get_new_characters(user_id, hsk, new_size)
        df = pd.concat([df_known, df_new]).sample(frac=1)  # concat and shuffle df rows
    else:
        raise NotImplementedError(study_session_type)
    print(df)
    return make_json(df)


def update_character_stat(user_id, character_id, delta):
    if None in [user_id, character_id, delta]:
        raise NotImplementedError(user_id, character_id, delta)
    sql_string = """
    insert into stats(id, user_id, character_id, stat, last_studied)
    values (
        (select id from stats where user_id = ? and character_id = ?),
        ?,
        ?,
        ?,
        strftime('%Y-%m-%d %H:%M:%S', 'now')
    )
    on conflict do
    update set stat=stat + ?, last_studied=strftime('%Y-%m-%d %H:%M:%S', 'now') where user_id = ? and character_id = ?
    """
    params = [
        user_id,
        character_id,
        user_id,
        character_id,
        delta,
        delta,
        user_id,
        character_id,
    ]
    query_db(sql_string, params)
    return 0


def get_characters(hsk=default_hsk):
    df = get_df()
    df = filter_by_hsk(df, hsk)
    return make_json(df)
