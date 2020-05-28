import requests
import os
import csv
import json
import pprint as pp


def send_request(url):
    headers = {
        'user-agent': 'Safari/537.36'
    }
    res = requests.request('GET', url=url, headers=headers)
    if res.status_code == 200:
        return res
    return send_request(url)


def write_csv(lines, file_name):
    file = open(file_name, 'a', encoding='utf-8', newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerows(lines)
    file.close()


def main():
    model_loads = json.loads(send_request(url="https://www.bmwusa.com/bin/services/warranty-books").text)
    count = 0
    for model_load in model_loads['subTags']:
        if count > 6:
            break
        count += 1
        year = model_load['name']
        subTags = model_load['subTags']
        for subTag in subTags:
            model = subTag['title']
            name = subTag['name']
            model_url = 'https://www.bmwusa.com/bin/services/warranty-books?year={}&series={}'.format(year, name)
            model_wars = json.loads(send_request(url=model_url).content)['pdfs']
            for model_war in model_wars:
                category_name = model_war['categoryName']
                category_url = 'https://www.bmwusa.com/' + model_war['url']
                line = [year, 'BMW', model, 'PDF', category_name, category_url]
                print(line)
                write_csv(lines=[line], file_name=file_name)


if __name__ == '__main__':
    print('---- Start ----')
    base_url = 'https://www.bmwusa.com/explore/bmw-value/bmw-ultimate-service/service-and-warranty-books.html'
    csv_header = [['YEAR', 'MAKE', 'MODEL', 'SECTION', 'TITLE', 'PDF']]
    file_name = 'BMW_Service_Warranty.csv'
    write_csv(lines=csv_header, file_name=file_name)
    main()
    print('--- The End ---')