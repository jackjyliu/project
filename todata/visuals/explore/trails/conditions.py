import pandas as pd
from todata.models.sql.functions import sql_read_pd
import plotly.express as px
import plotly.io as pio

def condition():
    return NotImplementedError


def current_condition():
    # based on past temps and preciptation
    # plot past 5/7 days condition
    # description
    # colour code?

    return NotImplementedError # return dictionary of summary + plot

def next_two_days():
    # plot of next two days of weather condition + sunrise/set
    # description
    # colour code?

    return NotImplementedError # return dictionary of summary + plot