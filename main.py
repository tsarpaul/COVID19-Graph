import io
import sys

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


try:
	country = sys.argv[1]
except:
	country = 'Israel'

r = requests.get('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
textfile = io.StringIO(r.text)
df = pd.read_csv(textfile, sep=',')
# Merge provinces
df = df.groupby('Country/Region').sum()

stats = df.iloc[:,3:]
df['sum'] = stats.sum(axis=1)

percent_stats = stats.iloc[:,1:].astype(float)
div_stats = stats.iloc[:,:-1].astype(float)
percent_stats /= div_stats.values
percent_stats -= 1
percent_stats *= 100
percent_stats = percent_stats.round(2)

country_stats = percent_stats.loc[country]

first_stat_index = 0
for index, stat in enumerate(country_stats):
	if not (stat == 0 or str(stat) == str(np.inf) or str(stat) == str(np.nan)):
		first_stat_index = index
		break
country_stats = country_stats[first_stat_index:]
country_stats = country_stats.replace(0, np.nan).replace(np.inf, np.nan).dropna()
country_stats = country_stats.T

ax = country_stats.plot(kind='bar')
ax.set_title("COVID19 Infections Growth in " + country, fontsize=18)
for p in ax.patches:
	ax.annotate(str(p.get_height()) + "%", (p.get_x(), p.get_height() * 1.01))
plt.show()
