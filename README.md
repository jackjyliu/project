Build Website to show Toronto-related data visualization, forecasting, ML
===

TODO
---
*   Get domain name
*   Refactor login and api keys
*   Gather more data
*   Web page design

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
*	<s>Dash +</s> difficult to integrate with flask
*   plotly for data viz or maybe bokeh
*   bootstrap for layout and css?
*	Datashader for large viz
*	<s>FB Prophet for forecast - probably not uses too much cpu and ram</s>
*	Catboost for ML?
*	With SHAP value explanations
*	Github for version control
*	Host on AWS

Challenges
---
<s>*	Embedding dash in flask? Some tutorials online</s>
*   Need to cache toronto news twice a day due to limited API calls

Architecture
---
*   Amazon Route 53 for domain
*   AWS Lightsail for Webserver + data processing
*	AWS RDS: run postgresql
*	Do bulk of data processing work over night
*	Use Lightsail to run ETL, webscrapping and push to RDS
*	After load, use Lightsail to update dashboards

Testing
---
*	Learn technologies in Windows VScode
*	Build test website in WSL2
*	Load WSL2 into Amazon lightsail

Data 
---
*	Toronto Rainfall: use average of all stations sum over whole hour **DONE**
*	Holiday data **DONE**
*	TTC Data
*	Local news (twitter or webscrapping) - Bing New API **API DONE**
*	Weather forecast - Openweather API (**API DONE**, need to insert to database??)
*   Is there toronto traffic data? for cars, transit, foot, retail?