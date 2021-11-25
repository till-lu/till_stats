#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 19:21:22 2021

@author: Till
"""
from bs4 import BeautifulSoup
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

qbthurs = ['Andy Dalton', 'Tim Boyle', 'Jared Goff', 'Trevor Siemian', 'Derek Carr', 'Dak Prescott', 'Josh Allen']
roof_fixed = ['LVR', 'NOR', 'DET', 'MIN', 'LAC', 'LAR']
roof_retr = ['DAL', 'IND', 'ATL', 'HOU', 'ARI']

   
url = 'https://www.pro-football-reference.com'
year = 2021
maxp = 300

 
# grab fantasy players
r = requests.get(url + '/years/' + str(year) + '/fantasy.htm')
soup = BeautifulSoup(r.content, 'html.parser')
parsed_table = soup.find_all('table')[0]  

df = []

# first 2 rows are col headers
for i,row in enumerate(parsed_table.find_all('tr')[2:]):
    if i % 10 == 0: print(i, end=' ')
    if i >= maxp: 
        print('\nComplete.')
        break
        
    try:
        dat = row.find('td', attrs={'data-stat': 'player'})
        name = dat.a.get_text()
        stub = dat.a.get('href')
        stub = stub[:-4] + '/fantasy/' + str(year)
        pos = row.find('td', attrs={'data-stat': 'fantasy_pos'}).get_text()

        # grab this players stats
        tdf = pd.read_html(url + stub)[0]    

        # get rid of MultiIndex, just keep last row
        tdf.columns = tdf.columns.get_level_values(-1)

        # fix the away/home column
        tdf = tdf.rename(columns={'Unnamed: 4_level_2': 'Away'})
        tdf['Away'] = [1 if r=='@' else 0 for r in tdf['Away']]

        # drop all intermediate stats
        tdf = tdf.iloc[:,[1,2,3,4,5,-3]]
        
        # drop "Total" row
        tdf = tdf.query('Date != "Total"')
        
        # add other info
        tdf['Name'] = name
        tdf['Position'] = pos
        tdf['Season'] = year

        df.append(tdf)
    except:
        pass

df = pd.concat(df)
df.head()    


url = 'https://www.pro-football-reference.com'
year = 2020
maxp = 300

 
# grab fantasy players
r = requests.get(url + '/years/' + str(year) + '/fantasy.htm')
soup = BeautifulSoup(r.content, 'html.parser')
parsed_table = soup.find_all('table')[0]  

df2020 = []

# first 2 rows are col headers
for i,row in enumerate(parsed_table.find_all('tr')[2:]):
    if i % 10 == 0: print(i, end=' ')
    if i >= maxp: 
        print('\nComplete.')
        break
        
    try:
        dat = row.find('td', attrs={'data-stat': 'player'})
        name = dat.a.get_text()
        stub = dat.a.get('href')
        stub = stub[:-4] + '/fantasy/' + str(year)
        pos = row.find('td', attrs={'data-stat': 'fantasy_pos'}).get_text()

        # grab this players stats
        tdf = pd.read_html(url + stub)[0]    

        # get rid of MultiIndex, just keep last row
        tdf.columns = tdf.columns.get_level_values(-1)

        # fix the away/home column
        tdf = tdf.rename(columns={'Unnamed: 4_level_2': 'Away'})
        tdf['Away'] = [1 if r=='@' else 0 for r in tdf['Away']]

        # drop all intermediate stats
        tdf = tdf.iloc[:,[1,2,3,4,5,-3]]
        
        # drop "Total" row
        tdf = tdf.query('Date != "Total"')
        
        # add other info
        tdf['Name'] = name
        tdf['Position'] = pos
        tdf['Season'] = year

        df2020.append(tdf)
    except:
        pass

df2020 = pd.concat(df2020)
df2020.head()

#this part for scraping the data is largely from Steven Morse 
#(https://stmorse.github.io/journal/pfr-scrape-python.html), thank you!

df_total = pd.concat([df2020, df])
df_total = df_total.reset_index()
df_org = df

df_total.to_csv('2020_wk12_2021.csv')



qbthx = df_total[(df_total['Name'].isin(qbthurs))] 

qbthx['roof'] = 'open'
qbthx['homeroof'] = 0

qbthx1 = qbthx.reset_index()

for i in range(0, len(qbthx1)):
    if (qbthx1.loc[i, 'Away'] == 1) & (qbthx1.loc[i, 'Opp'] in roof_fixed):
        qbthx1.loc[i, 'roof'] = 'roof'
    elif (qbthx1.loc[i, 'Away'] == 1) & (qbthx1.loc[i, 'Opp'] in roof_retr):
        qbthx1.loc[i, 'roof'] = 'roof'
    elif (qbthx1.loc[i, 'Away'] == 0) & (qbthx1.loc[i, 'Tm'] in roof_retr):
        qbthx1.loc[i, 'roof'] = 'roof'
    elif (qbthx1.loc[i, 'Away'] == 0) & (qbthx1.loc[i, 'Tm'] in roof_fixed):
        qbthx1.loc[i, 'roof'] = 'roof'
        
for i in range(0, len(qbthx1)):
    if (qbthx1.loc[i, 'Tm'] in roof_retr) | (qbthx1.loc[i, 'Tm'] in roof_fixed):
        qbthx1.loc[i, 'homeroof'] = '1'


fig = sns.barplot(x="Name", y="FantPt", hue="roof", ci = None, palette = sns.color_palette("Paired"), data=qbthx1)
plt.xticks(rotation=90)
plt.ylabel("Fantasy Points")
fig.set_ylim([0, 35])
plt.title("FPPG by QBs at roofed and open stadiums")
plt.legend(title='')
plt.show(fig)
fig.figure.savefig('ThxgiveQbs2.png', bbox_inches = 'tight', dpi = 1200)


fig2 = sns.barplot(x="homeroof", y="FantPt", hue="roof", ci = None, palette = sns.color_palette("Paired"), data=qbthx1)
plt.ylabel("Fantasy Points")
plt.xlabel("Roof at homefield")
plt.xticks([1,0], ["Roof", "Open"])
fig2.set_ylim([0, 35])
plt.title("FPPG by QBs at roofed and open stadiums by roof at homefield")
plt.legend(title='')
plt.show(fig2)
fig2.figure.savefig('ThxgiveQbsHOMEROOF2.png', bbox_inches = 'tight', dpi = 1200)



df_total['roof'] = 'open'
df_total['homeroof'] = 0
for i in range(0, len(df_total)):
    if (df_total.loc[i, 'Away'] == 1) & (df_total.loc[i, 'Opp'] in roof_fixed):
        df_total.loc[i, 'roof'] = 'roof'
    elif (df_total.loc[i, 'Away'] == 1) & (df_total.loc[i, 'Opp'] in roof_retr):
        df_total.loc[i, 'roof'] = 'roof'
    elif (df_total.loc[i, 'Away'] == 0) & (df_total.loc[i, 'Tm'] in roof_retr):
        df_total.loc[i, 'roof'] = 'roof'
    elif (df_total.loc[i, 'Away'] == 0) & (df_total.loc[i, 'Tm'] in roof_fixed):
        df_total.loc[i, 'roof'] = 'roof'
        
for i in range(0, len(df_total)):
    if (df_total.loc[i, 'Tm'] in roof_retr) | (df_total.loc[i, 'Tm'] in roof_fixed):
        df_total.loc[i, 'homeroof'] = '1'
        
df_qb = df_total[df_total['Position'] == 'QB']



fig3 = sns.barplot(x="homeroof", y="FantPt", hue="roof", ci = None, palette = sns.color_palette("Paired"), data=df_qb)
plt.ylabel("Fantasy Points")
plt.xlabel("Roof at homefield")
plt.xticks([1,0], ["Roof", "Open"])
fig3.set_ylim([0, 35])
plt.title("FPPG by QBs at roofed and open stadiums by roof at homefield")
plt.legend(title='')
plt.show(fig3)
fig3.figure.savefig('ALLQbsHOMEROOF.png', bbox_inches = 'tight', dpi = 1200)

