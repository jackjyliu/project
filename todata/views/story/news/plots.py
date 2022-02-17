"""
plotly visuals for toronto bikeshare data
"""
import pandas as pd

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import todata.views.plotly_custom_theme

pio.templates.default = "simple_white+custom"


def topic_pct():
    
    topic_pct = pd.read_pickle('./todata/static/stories/news/topic_pct.pkl')
    fig = px.line(topic_pct, x="week", y="pct", color='topic', color_discrete_sequence=px.colors.qualitative.G10,
                )
    fig.update_layout(
        title="News Topics % by Week",
        title_x=0.5,
        xaxis_title="Date (Week of)",
        yaxis_title="Topic %",
        legend=dict(x=0.05, y=1),
        margin={"r": 0, "l": 0, "b": 0},
        hovermode='x unified'
    )
    fig.update_traces(hovertemplate="%{y}%")

    plot = pio.to_html(fig, full_html=False, auto_play=False, config={"displayModeBar": False})

    return plot


def ner_words():
    
    ner_flat_count_trim = pd.read_pickle('./todata/static/stories/news/ner_count.pkl')
    fig = px.treemap(ner_flat_count_trim, path=[px.Constant("all"), 'type', 'word'], values='count')
    fig.update_traces(root_color="lightgrey")
    fig.update_traces(
        hovertemplate = '%{label}<br>%{value} stories'
    )
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

    plot = pio.to_html(fig, full_html=False, auto_play=False, config={"displayModeBar": False})

    return plot


def sentiment_count():
    
    merged_tree_count = pd.read_pickle('./todata/static/stories/news/sentiment_count.pkl')
    fig = px.sunburst(merged_tree_count, path=['topic', 'sentiment'], values='count',
                    color='sentiment',
                    color_discrete_map={'positive':'darkgreen', 'neutral':'PaleGoldenRod', 'negative':'darkred'},
                    hover_data={
                        'sentiment':True,
                        'topic':True,
                        'count':True
                    })
    fig.update_traces(hovertemplate = '%{label}<br>%{value} stories')
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    
    plot = pio.to_html(fig, full_html=False, auto_play=False, config={"displayModeBar": False})

    return plot


def data_sample():

    data_sample = pd.read_pickle('./todata/static/stories/news/data_sample.pkl')
    fig = go.Figure(data=[go.Table(
                        columnwidth=[8,25,40,5,6,20],
                        header=dict(values=list(data_sample.columns)),
                        cells=dict(values=[data_sample.date, data_sample.headline, data_sample.description, data_sample.topic, data_sample.sentiment, data_sample.keywords],align='left'),
                        )
                    ])
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0),
                        height=250)

    plot = pio.to_html(fig, full_html=False, auto_play=False, config={"displayModeBar": False})

    return plot


def topic_week():

    topic_week = pd.read_pickle('./todata/static/stories/news/topic_week.pkl')
    fig = px.bar(topic_week, x='topic', y='percentage', color='weekday', barmode='group')
    fig.update_traces(hovertemplate = '%{x}<br>%{y}%')
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0), legend=dict(x=0.05, y=0.9), title="News Topic % (Weekday vs Weekend)", title_x=0.5, title_y=0.95, legend_title='',
                        xaxis_title="Topic",
                        yaxis_title="Topic %",)
    
    plot = pio.to_html(fig, full_html=False, auto_play=False, config={"displayModeBar": False})

    return plot