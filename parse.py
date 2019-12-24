import requests
from bs4 import BeautifulSoup
import pandas as pd
import pandas_gbq
url = "https://ege.hse.ru/rating/2011/41333661/gos/"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

tbl = soup.find("table", {"id": "transparence_t"})

data_frame = pd.read_html(str(tbl))[0]
data_frame.to_csv('2011p.csv')
