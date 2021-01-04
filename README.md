Build Website to show Toronto-related data visualization, forecasting, ML
===
Pages
---
*	Toronto related dashboard: weather, events, TTC, road closures, local news?
*	Select data viz
*	Electricity use vs prices
*	Impact of weather on TTC delays
*	Forecasts?
*	ML example + sandbox
*	Limited sample size (randomly select 10k rows?)

Technologies
---
*	Postgres database
*	Python ETL, webscrapping, logic
*   plotly for data viz or maybe bokeh
*   bootstrap for layout and css?
*	Datashader for large viz
*	With SHAP value explanations
*	Github for version control
*	Host on AWS

Architecture
---
*   Amazon Route 53 for domain
*   AWS Lightsail for Webserver + data processing
*	AWS RDS: run postgresql
*	Do bulk of data processing work over night
*	Use Lightsail to run ETL, webscrapping and push to RDS
*	After load, use Lightsail to update dashboards