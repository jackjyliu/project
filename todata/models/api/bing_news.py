"""
access news headlines from Bing News Search API
return dictionary of news headlines, description, url
use raw=True for raw json file
"""

import requests
from todata.models.credentials import NEWS_API_KEY

API_URL = 'https://api.bing.microsoft.com/v7.0/news/search'


def bing_news(query='toronto', mkt='en-CA', count=10, freshness='day', raw=False):

    # build API request
    params = {
        'q':query, 
        'mkt':mkt, 
        'count':count, 
        'freshness':freshness, 
        'textDecorations':False, 
        'textFormat':'raw'}

    headers = {'Ocp-Apim-Subscription-Key': NEWS_API_KEY}

    # Call API
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
        
        # return raw json file if requested
        if raw:
            return results

    except Exception as ex:
        raise ex

    # extract headline, news url, description from each news item

    headlines = [article["name"] for article in results["value"]]
    descriptions = [article["description"] for article in results["value"]]
    news_url = [article["url"] for article in results["value"]]

    # list of dictionaries of news articles
    news_list = list()
    for i in range(count):
        news_item = {'headline': headlines[i], 'description': descriptions[i], 'url': news_url[i]}
        news_list.append(news_item)

    return news_list