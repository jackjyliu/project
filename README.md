Build Website to show Toronto-related data visualization, forecasting, ML
===

Pages
---
*	Toronto related dashboard: weather, events, TTC, road closures, local news?
*	Select data viz
*	Electricity use vs prices
*	Impact of weather on TTC
*	Forecasts
*	ML example + sandbox
*	Limited sample size (randomly select 10k rows?)

Technologies
---
*	Postgres database
*	Python ETL, webscrapping, logic
*	Dash + plotly for data viz
*	Datashader for large viz
*	FB Prophet for forecast - probably not uses too much cpu and ram
*	Catboost for ML?
*	With SHAP value explanations
*	Github for version control
*	Host on AWS
*	S3: store web files
*	EC2: run code
*	RDS: run postgresql
*	Light sail + EC2 for ETL, ML tasks?

Budget
---
*	 $50/month

Challenges
---
*	Embedding dash in flask? Some tutorials online

Architecture
---
*	Do bulk of data processing work over night
*	Use EC2 to run ETL, webscrapping and push to RDS
*	After load, use EC2 to update dashboards

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
*	Local news (twitter or webscrapping) - Bing New API? 
*	Weather forecast - Openweather API?