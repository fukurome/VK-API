import json

import requests

from constants import (
    KEYS,
    TOKEN,
    USER_ID,
    OUTPUT_PATH,
    URL,
    FIELDS,
    V,
    MAX_COUNT
)


def formatting_data(data: list) -> list:
    new_data = []
    for i in range(len(data)):
        dic = {}
        for key in KEYS:
            dic[key] = data[i].get(key)
            if dic[key] is not None:
                if key == 'country':
                    dic[key] = dic[key]['title']
                if key == 'city':
                    dic[key] = dic[key]['title']
        new_data.append(dic)
    return new_data


def dict_to_json(data, output_path=f'{OUTPUT_PATH}.json'):
    string = json.dumps(data, ensure_ascii=False, indent=4)
    json_file = open(output_path, "w", encoding="utf-8")
    json_file.write(string)
    json_file.close()


def do_request_and_make_report(offset, page=1):
    request = f"{URL}?" \
              f"v={V}&" \
              f"access_token={TOKEN}&" \
              f"user_id={USER_ID}&" \
              f"fields={FIELDS}&" \
              f"count={MAX_COUNT}&" \
              f"offset={offset}"

    response = requests.get(request)
    try:
        data = response.json()['response']
    except KeyError:
        print('\033[31mERROR: ' + response.json()['error']['error_msg'])
        return

    friends_list = data['items']
    new_friends_list = formatting_data(friends_list)

    dict_to_json(new_friends_list, f"report_page{page}.json")
    return data['count']


def main():
    friends_count = do_request_and_make_report(offset=0, page=1)
    if MAX_COUNT < friends_count:
        for i in range(1, friends_count // MAX_COUNT + 1):
            do_request_and_make_report(offset=MAX_COUNT * i, page=i + 1)


if __name__ == "__main__":
    main()
