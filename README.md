# pgatour-stats-scraper
Scrapes All Player Stats From PGA TOUR Website

Add the stats_functions script to your site-packages folder, and use the following code to collect PGA TOUR stats for desired seasons:

import stats_functions as sf
ds = sf.collect_stats(path, years)
