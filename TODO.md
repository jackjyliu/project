Project TODO
===

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

*   ML Experiments (ML on datasets from postgres database, with PyCaret?)

*   About Page
    *   Describe website purpose
    *   Website Architure
    *   Contact Info
        *   Internal Message
        *   Gmail address?

Model
---
*   Move credentials to main root folder or swtich to environ?
*   Schedule cron jobs to ETL (and maybe run models?)
*   Build dashboards
*   ML
    *   Catboost + SHAP
    *   Pycaret for simple ML?


Data
---
*   Break off sql_load into multiple functions
*   ETL pipelines
    *   Hourly open weather
    *   Daily bing news
*   Data Sources
    *   TTC
    *   Traffic?
    *   Population Data for per capita calcs