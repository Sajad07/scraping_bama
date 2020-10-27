from bs4 import BeautifulSoup
import requests
import re
import sqlite3
from datetime import date

today = date.today()
today = str(today)
today = today.replace('-', '_')
j = 1
while True:
    res = requests.get('https://bama.ir/car/peugeot/405/all-trims?page=%d' % (j,))
    soup = BeautifulSoup(res.text, 'html.parser')
    r = soup.find_all('span', attrs={"itemprop": "name"})
    try:
        r[3]
        print('page %d' % (j,))
    except IndexError:
        break
    new_url = re.findall(r'href=\"(https:.+car.+detail.+?)\" ', res.text)
    new_url = list(dict.fromkeys(new_url))
    for i in new_url:
        res = requests.get(i)
        soup = BeautifulSoup(res.text, 'html.parser')
        h1 = soup.find('h1')
        my_list = h1.text.split(' ')
        string2 = ' '.join(my_list[1:5])
        try:
            cnn = sqlite3.connect('tables_cars_in_bama.db')
            cur = cnn.cursor()
        except Exception as error:
            print(error)
        else:
            sql = "CREATE TABLE IF NOT EXISTS car_table%s(year text,model text,city text,url text);" % (
                today)
            cur.execute(sql)
            cnn.commit()
            sql = "INSERT INTO car_table%s VALUES('%s','%s','%s','%s')" % (
                today, my_list[0], string2, my_list[-1], i)
            cur.execute(sql)
            cnn.commit()
            cnn.close()
    j += 1
