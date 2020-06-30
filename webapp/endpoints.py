from flask import jsonify

from webapp.app import db


def get_players_from_db():
    sql = """select * from playerinfo limit 10"""
    return jsonify(db.query_db(sql))


def upload_tweets_to_db(tweets_json):
    def format_single_value(row_dict, col):
        if col not in row_dict.keys():
            return 'null'
        elif isinstance(row_dict[col], str) and row_dict[col] != '':
            return f"'{row_dict[col]}'"
        elif isinstance(row_dict[col], str) and row_dict[col] == '':
            return 'null'
        return str(row_dict[col])

    def insert_values_str(row_dict):
        vals = ", ".join([
            format_single_value(row_dict, col) for col in columns
        ])
        return f"({vals})"

    if len(tweets_json) > 0:
        # keep columns consistent
        columns = [k for k in tweets_json[0].keys()]
        # format rows, join together
        vals_str = ",\n".join(insert_values_str(row) for row in tweets_json)
        sql = f'insert into scraped_tweets ({", ".join(columns)}) \nvalues\n{vals_str};'
        result = db.insert(sql)

    return jsonify({'Result': 'success'})


def get_followed_accounts_from_db(user_id=None, user_name=None):
    sql = "select * from scraped_accounts"
    column, value = ('id', user_id) if user_id is not None else ('twitter_handle', f"'{user_name}'")
    if user_id is not None or user_name is not None:
        sql += f' where {column} = {value}'
    results = db.query_db(sql)

    if (user_id is None and user_name is None) or len(results) == 0:
        # no results or unspecified account
        return jsonify(results)
    else:
        # specific account
        results = results[0]
        account_id = user_id if user_id is not None else results['id']
        sql = f'select twitter_id from scraped_tweets where account_id = {account_id}'
        results['tweet_ids'] = [res['twitter_id'] for res in db.query_db(sql)]
        return jsonify(results)
