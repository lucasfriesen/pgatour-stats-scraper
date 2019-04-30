__author__ = "Lucas Friesen"

import os
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
from datetime import date
import win32com.client as win32
import time


def collect_stats(path, years):
    
    start_time = time.time()
    
    check_dirs(path)
    
    dm = links(path)
    
    dd = descriptions(path, dm)
    
    ds = scrape_stats(path, dm, dd, years)
    
    end_time = time.time()
    duration = float("{0:.2f}".format((end_time-start_time)/60))
    print('Stats updated in {} minutes.'.format((duration)))
    
    return ds

def check_dirs(path):
    """
    Creates directories required for the full collection process.
    
    Params:
        path = main directory
    Returns:
        None
    """
    
    print('Checking for directories within path - creating folders if not existing...')
    folders = ['stats/links', 'stats/seasons']
    
    for folder in folders:
        directory = path + folder
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(directory + ' - CREATED')
        else:
            print(directory + ' - EXISTS')
    
    print('Directories created/ready...')
    

def links(path):
    """
    Collects links for each stat posted on PGATOUR.com
    
    Params:
        path = main directory to save files in appropriate folders
    Returns:
        pandas Dataframe, with all stat links
    """
    
    PATH = path
    link_extend = 'https://www.pgatour.com'

    URL = "https://www.pgatour.com/stats.html"
    r = requests.get(URL)
    
    soup = BeautifulSoup(r.text, 'lxml')
    container = soup.find('div', class_='page-container')

    
    nav = container.find('div', class_='navigation section')
    
    lis = nav.find_all('li')
    
    category_links = []
    
    for li in lis[1:]:
        
        a = li.find('a')
        category_links.append(link_extend + a['href'])
    
    master = []
    stat = []
    stat_link = []
    
    for link in category_links:
        
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'lxml')
        
        container = soup.find('div', class_='section categories')
    
        lis = container.find_all('li')
        
        for li in lis:
            
            master.append(link)
            
            a1 = li.find('a')
            
            a1_url = a1['href']
            
            a1_url2 = (a1_url.split("html", 1)[0])
            
            stat.append(a1.text)
            stat_link.append(link_extend + a1_url2)
            
    
    dict_stats = {'master': master,
                  'stat': stat,
                  'stat_link': stat_link}
    
    ds = pd.DataFrame(dict_stats)
    
    ds.to_csv(PATH + "stats/links/StatLinks.csv", index=False)
    print('Stat links collected and saved')
    
    return ds


def descriptions(path, dm):
    """
    Collects stat descriptions from PGA TOUR to add context - DOES NOT RUN EACH TIME - DESCRIPTIONS DON'T CHANGE
    
    Params:
        path = main directory to save files in appropriate folders
        dm = dataframe of stat links, as collected from links() function
    Returns:
        pandas Dataframe, with all stat descriptions
    """
    
    stat = dm['stat']
    stat_link = dm['stat_link']
    master_link = dm['master']
    YEAR = '2019'
    
    stat_name2 = []
    link2 = []
    category2 = []
    year2 = []
    description = []
    
    for STAT, LINK, MASTER in zip(stat, stat_link, master_link):

        URL = LINK + YEAR + ".html"
        
        try:
            r = requests.get(URL)
        except:
            pass
            print(YEAR + ' - ' + STAT + ' NOT COLLECTED - ERROR')    
        
        stat_name2.append(STAT)
        link2.append(LINK)
        year2.append(YEAR)
        
        m1 = (MASTER.split(".", 3)[3]).split('_', 1)[0]
        category2.append(m1)
        
        soup = BeautifulSoup(r.text, 'lxml')
        footer = soup.find('div', {'class':'content-footer'})
        desc = footer.find('p')
        description.append(desc.text)
        
        print(YEAR + ' - ' + STAT + ' COLLECTED')
                
    dict_desc = {'year': year2,
                  'stat_name': stat_name2,
                  'link': link2,
                  'category': category2,
                  'description': description}
    
    dd = pd.DataFrame(dict_desc)
    dd = dd[['year', 'stat_name', 'link', 'category', 'description']]
    dd = dd.apply(lambda x: x.str.replace("\n",""))
    dd = dd.apply(lambda x: x.str.replace("\t",""))
    dd = dd.apply(lambda x: x.str.replace("\r",""))
        
    dd.to_csv(path + "stats/links/StatLinks_Descriptions.csv", index=False)
    
    return dd


def scrape_stats(path, dm, dd, years):
    """
    Collects stats for each year, saves to file and creates full stat dataset
    
    Params:
        path = main directory to save files in appropriate folders
        dm = pandas Dataframe with stat links
        dd = pandas Dataframe with stat descriptions
        years = list of years as integers
    Returns:
        Dataframe with full stats for all years previously and currently collected into the path folder, cleaned and saved to file
    """
    
    stat = dm['stat']
    stat_link = dm['stat_link']
    master_link = dm['master']
    _year = years

    
    for YEAR in _year:
        
        start_time2 = time.time()
        
        stat_name = []
        link = []
        category = []
        year = []
        rank = []
        rank_last = []
        athlete = []
        stat1_name = []
        stat2_name = []
        stat3_name = []
        stat4_name = []
        stat5_name = []
        stat6_name = []
        stat7_name = []
        stat1 = []
        stat2 = []
        stat3 = []
        stat4 = []
        stat5 = []
        stat6 = []
        stat7 = []
    
        num = 0
        
        for STAT, LINK, MASTER in zip(stat, stat_link, master_link):
            
            num = num + 1
            
            URL = LINK + str(YEAR) + ".html"
            
            try:
                r = requests.get(URL)  
                
                soup = BeautifulSoup(r.text, 'lxml')
                table = soup.find('table', {'id':'statsTable'})
                
                ths = table.find_all('th')
         
                try:
                    s1 = ths[3].text
                except:
                    s1 = ''
        
                try:
                    s2 = ths[4].text
                except:
                    s2 = ''
                    
                try:
                    s3 = ths[5].text
                except:
                    s3 = ''
                    
                try:
                    s4 = ths[6].text
                except:
                    s4 = ''
                    
                try:
                    s5 = ths[7].text
                except:
                    s5 = ''
                    
                try:
                    s6 = ths[8].text
                except:
                    s6 = ''
                    
                try:
                    s7 = ths[9].text
                except:
                    s7 = ''
                    
                    
                trs = table.find_all('tr')
                
                for tr in trs[1:]:
                    
                    stat_name.append(STAT)
                    link.append(LINK)
                    year.append(str(YEAR))
                    
                    m1 = (MASTER.split(".", 3)[3]).split('_', 1)[0]
                    category.append(m1)
                    
                    stat1_name.append(s1)
                    stat2_name.append(s2)
                    stat3_name.append(s3)
                    stat4_name.append(s4)
                    stat5_name.append(s5)
                    stat6_name.append(s6)
                    stat7_name.append(s7)
                    
                    tds = tr.find_all('td')
                    
                    rank.append(tds[0].text)
                    rank_last.append(tds[1].text)
                    athlete.append(tds[2].text)
                    
                    try:
                        stat1.append(tds[3].text)
                    except:
                        stat1.append('')
                        
                    try:
                        stat2.append(tds[4].text)
                    except:
                        stat2.append('')
                    
                    try:
                        stat3.append(tds[5].text)
                    except:
                        stat3.append('')
                    
                    try:
                        stat4.append(tds[6].text)
                    except:
                        stat4.append('')
                    
                    try:
                        stat5.append(tds[7].text)
                    except:
                        stat5.append('')
                    
                    try:
                        stat6.append(tds[8].text)
                    except:
                        stat6.append('')
                    
                    try:
                        stat7.append(tds[9].text)
                    except:
                        stat7.append('')
                    
                        
                print(str(YEAR) + ' - Stat ' + str(num) + '/' + str(len(stat_link)) + ' COLLECTED')  
            
            except:
                pass
                print(str(YEAR) + ' - ' + STAT + ' NOT COLLECTED - ERROR')  
                    
            
        dict_stats2 = {'year': year,
              'stat_name': stat_name,
              'link': link,
              'category': category,
              'rank': rank,
              'rank_last': rank_last,
              'athlete': athlete,
              'stat1_name': stat1_name,
              'stat1': stat1,
              'stat2_name': stat2_name,
              'stat2': stat2,
              'stat3_name': stat3_name,
              'stat3': stat3,
              'stat4_name': stat4_name,
              'stat4': stat4,
              'stat5_name': stat5_name,
              'stat5': stat5,
              'stat6_name': stat6_name,
              'stat6': stat6,
              'stat7_name': stat7_name,
              'stat7': stat7}

        
        ds2 = pd.DataFrame(dict_stats2)
        ds2 = ds2[['year', 'stat_name', 'link', 'category', 'rank', 'rank_last', 'athlete', 'stat1_name', 'stat1', 'stat2_name', 'stat2', 'stat3_name', 'stat3', 'stat4_name', 'stat4', 'stat5_name', 'stat5', 'stat6_name', 'stat6', 'stat7_name', 'stat7']]
        
        #clean the dataset for each season
        ds2 = ds2.apply(lambda x: x.str.replace("\n",""))
        ds2 = ds2.apply(lambda x: x.str.replace("\t",""))
        ds2 = ds2.apply(lambda x: x.str.replace("\r",""))
        
        ds2['rank'] = ds2['rank'].str.replace('T','')
        ds2['rank_last'] = ds2['rank_last'].str.replace('T','')
    
        dd = dd.sort_values(['category', 'stat_name'], ascending=[1, 1])
        ds2 = ds2.sort_values(['category', 'stat_name', 'year', 'rank'], ascending=[1, 1, 1, 1])
        
        ds3 = pd.merge(ds2, dd[['category', 'stat_name', 'description']], on=['category', 'stat_name'], how='outer')
        
        ds3.loc[ds3['category'] == 'RSCR', 'type'] = 'Scoring'
        ds3.loc[ds3['category'] == 'RAPP', 'type'] = 'Approach'
        ds3.loc[ds3['category'] == 'RPUT', 'type'] = 'Putting'
        ds3.loc[ds3['category'] == 'ROTT', 'type'] = 'Off The Tee'
        ds3.loc[ds3['category'] == 'RSTR', 'type'] = 'Streaks'
        ds3.loc[ds3['category'] == 'RARG', 'type'] = 'Around The Green'
        ds3.loc[ds3['category'] == 'RMNY', 'type'] = 'Money'
        ds3.loc[ds3['category'] == 'RPTS', 'type'] = 'Points'
               
        ds3 = ds3[['year', 'category', 'type', 'stat_name', 'link', 'description', 'rank', 'athlete', 'stat1_name', 'stat1', 'stat2_name', 'stat2', 'stat3_name', 'stat3', 'stat4_name', 'stat4', 'stat5_name', 'stat5', 'stat6_name', 'stat6', 'stat7_name', 'stat7']]
        ds3 = ds3.sort_values(['category', 'stat_name', 'year', 'rank'], ascending=[1, 1, 1, 1])
        ds3.to_csv(path + "stats/seasons/PGATourStats_" + str(YEAR) + ".csv", index=False)
        
        end_time2 = time.time()
        duration2 = float("{0:.2f}".format((end_time2-start_time2)/60))
        print(str(YEAR) + ' Stats collected in {} minutes.'.format(duration2))
        
        
    #append all seasons of stats together
    df_list = []
    for file in os.listdir(path + 'stats/seasons/'):
        if file.endswith('.csv'):
            df = pd.read_csv(path + 'stats/seasons/' + file)
            df_list.append(df)
    
    dall = pd.concat(df_list)
    dall = dall.sort_values(['category', 'stat_name', 'year', 'rank'], ascending=[1, 1, 1, 1])
    dall.drop_duplicates(subset=['category', 'stat_name', 'year', 'rank', 'athlete'], keep='first', inplace=True)
    dall.to_csv(path + 'stats/PGATourStats_Full.csv', index=False)
    
    dall2 = clean_stats(dall)
    
    dall2 = dall2.sort_values(['category', 'stat_name', 'year', 'stat', 'rank'], ascending=[1, 1, 1, 1, 1])
    dall2.drop_duplicates(subset=['category', 'stat_name', 'year', 'stat', 'rank', 'athlete'], keep='first', inplace=True)
    dall2.to_csv(path + 'stats/PGATourStats_Full_Clean.csv', index=False)
    
    print('Full stats dataset cleaned and saved to file')
    
    return dall2

def clean_stats(ds):
    """
    Cleans stats dataset
    
    Params:
        ds = stats dataset from scrape_stats - can be full (all years) or a single year
    Returns:
        Cleaned up pandas dataframe
    """
    
    print('Cleaning up stats dataset...')
    dm = pd.DataFrame(columns=['year', 'category', 'type', 'stat_name', 'link', 'description', 'rank', 'athlete', 'stat', 'value'])

    ds1 = ds[['year', 'category', 'type', 'stat_name', 'link', 'description', 'rank', 'athlete', 'stat1_name', 'stat1']]
    ds1 = ds1.rename(columns={'stat1_name' : 'stat', 'stat1' : 'value'})
    dm = dm.append(ds1)
    
    ds2 = ds[['year', 'category', 'type', 'stat_name', 'link', 'description', 'rank', 'athlete', 'stat2_name', 'stat2']]
    ds2 = ds2.rename(columns={'stat2_name' : 'stat', 'stat2' : 'value'})
    dm = dm.append(ds2)
    
    ds3 = ds[['year', 'category', 'type', 'stat_name', 'link', 'description', 'rank', 'athlete', 'stat3_name', 'stat3']]
    ds3 = ds3.rename(columns={'stat3_name' : 'stat', 'stat3' : 'value'})
    dm = dm.append(ds3)
    
    ds4 = ds[['year', 'category', 'type', 'stat_name', 'link', 'description', 'rank', 'athlete', 'stat4_name', 'stat4']]
    ds4 = ds4.rename(columns={'stat4_name' : 'stat', 'stat4' : 'value'})
    dm = dm.append(ds4)
    
    ds5 = ds[['year', 'category', 'type', 'stat_name', 'link', 'description', 'rank', 'athlete', 'stat5_name', 'stat5']]
    ds5 = ds5.rename(columns={'stat5_name' : 'stat', 'stat5' : 'value'})
    dm = dm.append(ds5)
    
    ds6 = ds[['year', 'category', 'type', 'stat_name', 'link', 'description', 'rank', 'athlete', 'stat6_name', 'stat6']]
    ds6 = ds6.rename(columns={'stat6_name' : 'stat', 'stat6' : 'value'})
    dm = dm.append(ds6)
    
    ds7 = ds[['year', 'category', 'type', 'stat_name', 'link', 'description', 'rank', 'athlete', 'stat7_name', 'stat7']]
    ds7 = ds7.rename(columns={'stat7_name' : 'stat', 'stat7' : 'value'})
    dm = dm.append(ds7)
    
    dm.dropna(axis=0, subset=['stat'], inplace=True)
    
    print('Stats cleaned and ready for export...')
    
    return dm
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
