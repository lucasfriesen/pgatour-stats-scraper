# pgatour-stats-scraper
## Web Scraper for PGA TOUR Stats from pgatour.com

### Dependencies: os, pandas, requests, bs4, time

#### Install the pga_stats_scraper script, and use the master function as follows:

------------------------------------------------------------

import pga_stats_scraper as ps
df = ps.collect_stats(PATH, YEARS)

PATH -> The folder to save all files

YEARS -> List of years as integers - valid years include 2009 to present.

#### EXAMPLE 1:

Collect data for the PGA TOUR stats for the 2018 and 2019 seasons, saving to Desktop.

df = ps.collect_stats('C:/Users/###/Desktop/', [2018, 2019])

#### EXAMPLE 2:

Collect stats for all years and save in Documents folder.

df = ps.collect_stats('C:/Users/###/Documents/', list(range(2009,2020)))
