Project TODO
===

This Week
---
Bash script to config: venv, start servers, flask configs
Cleanup Celery
Daemon tool
Webscrapping
Maps

Power Story
---
*   Catboost Factors
*   Temperature
*   Change Source Color to Light grey

Data
---
*   ETL pipelines (weather hourly, news 2x per day save to DB, dashboard will pull from DB)
    *   redis queue for task scheduling
*   Data Sources
    *   TTC
    *   Traffic?
    *   Population Data for per capita calcs

Dashboard (hourly cached?)
---

*   Toronto Indicators
    *   Last rainfall/snowfall
    *   Traffic/TTC/Road Closures
    *   Events
    *   Other useful daily data

Web
---
*   Domain name
*   Logo Design
*   How to make website mobile friendly
*   Font Choice: sans serif
*   Colour Choice: Black, Blue, Grey
*   Page Layout: grid + responsive
        *   add scrollspy for progress tracking + section jumping
*   Template Design (with bootstrap?)
    *   Tabs with dropdown menu

*   Dashboard (hourly cached?)
    *   Current Weather
    *   Current Weather
    *   Toronto Indicators
        *   Last rainfall/snowfall
        *   Traffic/TTC/Road Closures
        *   Events
        *   Other useful daily data

*   Data Stories (interesting stories about Toronto data)
    *   Power usage vs weather and weekly cycle
    *   Traffic / TTC Data
    *   News word analysis
        *   tf-idf for most common words?

*   Data Exploration (visualization of different data from postgres database, user choice)

*   Neighbourhoods of Toronto (with mapping)

*   About Page
    *   Describe website purpose
    *   Website Architure
    *   Contact Info
        *   Internal Message
        *   Gmail address?

Model
---
*   Move credentials to main root folder or swtich to environ?
*   ML
    *   Catboost + SHAP
    *   Pycaret for simple ML?