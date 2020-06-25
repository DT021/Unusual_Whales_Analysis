import re

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

# Function which removes the empty or useless entries in the list which was is passed in
def remove_empty_entries(l:list):
    if len(l)<=0:
        return l
    elif l[0] == '' or l[0] == '️ ' or l[0] == '️':
        return remove_empty_entries(l[1::])
    else:
        return [l[0]]+remove_empty_entries(l[1::])

def create_dict_from_str(s: str):
    s = deEmojify(s)
    s = re.split("\n", s)
    s = remove_empty_entries(s)
    print(s)
    # dictionary for the symbol retrieved in the unusual flow call out
    symbol_dict = {}
    for i in range(len(s)):
        if i == 0:
            new_entry = re.split(' ', s[i])
            dict_name = ''
            for j in range(len(new_entry)):
                if j == 0:
                    new_entry[i] = new_entry[j].replace('$', '')
                    dict_name = 'Name'
                elif j == 1:
                    dict_name = 'Expiration Date'
                elif j == 2:
                    dict_name = 'Type'
                else:
                    new_entry[i] = new_entry[j].replace('$', '')
                    dict_name = 'Strike'
                symbol_dict[dict_name]= new_entry[j]
            continue
        new_entry = re.split(": ", s[i])
        if new_entry[1].__contains__('$'):
            new_entry[1] = new_entry[1].replace('$', '')
        elif new_entry[1].__contains__('%'):
            new_entry[1] = new_entry[1].replace('%', '')
        symbol_dict[new_entry[0]] = float(new_entry[1])
    return symbol_dict


