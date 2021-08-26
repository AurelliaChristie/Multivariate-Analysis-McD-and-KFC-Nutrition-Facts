import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Data frame for final result
result_df = pd.DataFrame()

# Web URL
url = "https://www.fatsecret.co.id/kalori-gizi/search?q=McDonald%27s&pg="

for i in range(5):
    # Request & get the links to each food
    res = requests.get(f'{url}{i}')
    soup = BeautifulSoup(res.text, 'html.parser')
    links = [a['href'] for a in soup.select('.prominent')]

    for i in range(len(links)):
        # Request & get the nutrition data of each food
        res_nut = requests.get(f'https://www.fatsecret.co.id{links[i]}')
        soup_nut = BeautifulSoup(res_nut.text, 'html.parser')
        ## Nutrition names
        nut_name = [n.text for n in soup_nut.select('.nutrition_facts>.left')]
        nut_name[1] = "Kalori"
        names = ["Menu"]
        names.extend(nut_name)
        ## Nutrition values
        nut_value = [re.sub(',','.',re.search('[0-9]+,*[0-9]*',n.text).group()) for n in soup_nut.select('.nutrition_facts>.tRight')]
        values = [n.text for n in soup_nut.select('.breadcrumb_noLink')]
        values.extend(nut_value)

        if len(names) == len(values):
            # Create dictionary for final output
            result = {}
            for i in range(len(names)):
                result[names[i]] = [values[i]]
            # Save the dictionary into Data Frame
            df = pd.DataFrame(result)

        result_df = pd.concat([result_df, df], axis = 0, ignore_index=True)

result_df.to_csv('McDonalds.csv')