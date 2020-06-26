import re


def de_emojify(text):
    regex_pattern = re.compile(pattern="["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    return regex_pattern.sub(r'', text)


def remove_empty_entries(list_with_empties: list):
    return [entry for entry in list_with_empties if entry not in [' ', '','️ ','️']]
