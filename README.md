Website to highlight Toronto-related data
===
Content
---
*	Dashboard: weather, calendar, road closures, local news
*	Explore selected datasets
    *   Indicators
    *   Neighbourhood Information
    *   Parks and Trails
    *   More to come
*	Stories about specific areas
    *   Power Use
    *   Bike Share Patterns
    *   Local News Info
    *   More to come

Technologies
---
*   Amazon Route 53 for domain and DNS
*   AWS EC2 + S3 for Webserver + data processing
*	AWS RDS as Data Warehouse
*	Use Celery and Redis to schedule, queue and process ETL task for load into RDS
*   Flask as Web Framework to generate webpages and run page logic in conjunction with Python and Pandas
*   Plotly for graphs
*   Bootstrap for website components and CSS
*   Nginx and Gunicorn as webserver and proxy to serve website

![Architecture](https://github.com/jackjyliu/project/blob/main/todata/static/img/arch_diagram_v4.svg)