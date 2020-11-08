import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from collections import OrderedDict
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from django_plotly_dash import DjangoDash
from django.conf import settings

app = DjangoDash("app")
#server = app.server

# Read in excel data from csv
df = pd.read_csv(settings.MEDIA_ROOT + '/' + 'data.csv',encoding='ISO-8859-1')

# Deleting all rows where we don't have a customer id
df = df.dropna(subset=['CustomerID'])

# Deleting all rows where the quantity and unit price of an item is below 0
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

# Deleting all duplicate rows
df = df.drop_duplicates()

# Creating a new column that has the total cost of the item
df['TotalCost'] = df['Quantity'] * df['UnitPrice']

# storing a list of top 20 most purchased products in a dataframe
most_purchased_prods = pd.DataFrame(df['Description'].value_counts().head(20)).rename(columns={'Description': 'Count'})

most_purchased_prods['Item'] = most_purchased_prods.index
most_purchased_prods.reset_index(drop=True, inplace=True)
most_purchased_prods = most_purchased_prods.iloc[:, [1, 0]]

# storing a list of 20 countries with the most traffic
most_purchased_bycountry = pd.DataFrame(df['Country'].value_counts().head(20)).rename(columns={'Country': 'Count'})

most_purchased_bycountry['Country'] = most_purchased_bycountry.index
most_purchased_bycountry.reset_index(drop=True, inplace=True)
most_purchased_bycountry = most_purchased_bycountry.iloc[:, [1, 0]]

most_purchased_bycountry_10 = most_purchased_bycountry[:10]

# storing a list of 20 countries with the most traffic excluding UK
nonuk_df = df[df['Country'] != 'United Kingdom']
most_purchased_bycountry_nonuk = pd.DataFrame(nonuk_df['Country'].value_counts().head(20)).rename(
    columns={'Country': 'Count'})

most_purchased_bycountry_nonuk['Country'] = most_purchased_bycountry_nonuk.index
most_purchased_bycountry_nonuk.reset_index(drop=True, inplace=True)
most_purchased_bycountry_nonuk = most_purchased_bycountry_nonuk.iloc[:, [1, 0]]

# Creating a new column that stores the date that the item was purchased
df['InvoiceDateCon'] = pd.to_datetime(df['InvoiceDate'])
df['InvoiceDateCon'] = pd.to_datetime(df['InvoiceDateCon'])


# Creating a function to get the month and year from a datetime value
def get_month(x): return dt.datetime(x.year, x.month, 1)


df['InvoiceDateCon'] = df['InvoiceDateCon'].apply(get_month)

# Grouping the data by customer ids and searching for the earliest month that the customer made a purchase (Cohort Month)
grouping = df.groupby('CustomerID')['InvoiceDateCon']
df['CohortMonth'] = grouping.transform('min')


def get_date_int(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    return year, month


invoice_year, invoice_month = get_date_int(df, 'InvoiceDateCon')

cohort_year, cohort_month = get_date_int(df, 'CohortMonth')

years_diff = invoice_year - cohort_year
months_diff = invoice_month - cohort_month

# Calculating the cohort index by calculating the difference between the earliest purchase and the current purchase
df['CohortIndex'] = years_diff * 12 + months_diff + 1

df['TimeOfPurchase'] = pd.to_datetime(df['InvoiceDate'])

# Calculating the purchase count by time
time_of_purchase = df.groupby(['TimeOfPurchase']).agg({'TimeOfPurchase': 'count'}).rename(
    columns={'TimeOfPurchase': 'Count'})

# Creating the Cohort Table
grouping = df.groupby(['CohortMonth', 'CohortIndex'])
cohort_data = grouping['CustomerID'].nunique()
cohort_data = cohort_data.reset_index()
cohort_counts = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerID')

# Creating the Retention Rate Table
cohort_sizes = cohort_counts.iloc[:, 0]
retention = cohort_counts.div(cohort_sizes, axis=0)
retention_round = retention.round(3) * 100

retention_round.index = retention_round.index.date

last_timestamp = df['InvoiceDate'].max() + dt.timedelta(days= 1)

rfm = df.groupby(['CustomerID']).agg({'InvoiceDate': lambda x: (last_timestamp - x.max()).days,
                                      'InvoiceNo': 'count', 'TotalCost': 'sum'})

rfm.rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'TotalCost': 'MonetaryValue'}
           , inplace=True)

# Building RFM segments
r_labels = range(4, 0, -1)
f_labels = range(1, 5)
m_labels = range(1, 5)
r_quartiles = pd.qcut(rfm['Recency'], q=4, labels=r_labels)
f_quartiles = pd.qcut(rfm['Frequency'], q=4, labels=f_labels)
m_quartiles = pd.qcut(rfm['MonetaryValue'], q=4, labels=m_labels)
rfm = rfm.assign(R=r_quartiles, F=f_quartiles, M=m_quartiles)


# Build RFM Segment and RFM Score
def add_rfm(x): return str(x['R']) + str(x['F']) + str(x['M'])


rfm['RFM_Segment'] = rfm.apply(add_rfm, axis=1)
rfm['RFM_Score'] = rfm[['R', 'F', 'M']].sum(axis=1)


def segments(df):
    if df['RFM_Score'] > 9:
        return 'Top'
    elif (df['RFM_Score'] > 5) and (df['RFM_Score'] <= 9):
        return 'Middle'
    else:
        return 'Low'


rfm['General_Segment'] = rfm.apply(segments, axis=1)

rfm_cluster = rfm.iloc[:, 0:3]

rfm_cluster_log = np.log(rfm_cluster)
scaler = StandardScaler()
scaler.fit(rfm_cluster_log)
rfm_norm = scaler.fit_transform(rfm_cluster_log)
rfm_norm = pd.DataFrame(data=rfm_norm, index=rfm_cluster_log.index, columns=rfm_cluster_log.columns)

kmeans = KMeans(n_clusters=5)
kmeans.fit(rfm_norm)

rfm_norm['Cluster'] = kmeans.labels_
rfm['Cluster'] = kmeans.labels_

rfm_summary = rfm.groupby(['Cluster']).agg({'Recency': 'mean', 'Frequency': 'mean',
                                            'MonetaryValue': ['mean', 'count'], }).round(0)

df_trim = df.iloc[:, [6, 7, 8, 9, 11]]

rfm_c1 = rfm[rfm['Cluster'] == 0]
rfm_c2 = rfm[rfm['Cluster'] == 1]
rfm_c3 = rfm[rfm['Cluster'] == 2]
rfm_c4 = rfm[rfm['Cluster'] == 3]
rfm_c5 = rfm[rfm['Cluster'] == 4]

c1_summary = rfm_c1.groupby(['General_Segment']).agg({'Recency': 'mean', 'Frequency': 'mean',
                                                      'MonetaryValue': ['mean', 'count'], }).round(0)

c2_summary = rfm_c2.groupby(['General_Segment']).agg({'Recency': 'mean', 'Frequency': 'mean',
                                                      'MonetaryValue': ['mean', 'count'], }).round(0)

c3_summary = rfm_c3.groupby(['General_Segment']).agg({'Recency': 'mean', 'Frequency': 'mean',
                                                      'MonetaryValue': ['mean', 'count'], }).round(0)

c4_summary = rfm_c4.groupby(['General_Segment']).agg({'Recency': 'mean', 'Frequency': 'mean',
                                                      'MonetaryValue': ['mean', 'count'], }).round(0)

c5_summary = rfm_c5.groupby(['General_Segment']).agg({'Recency': 'mean', 'Frequency': 'mean',
                                                      'MonetaryValue': ['mean', 'count'], }).round(0)

rfm['CustomerID'] = rfm.index

rfm.reset_index(drop=True, inplace=True)

df_rework = pd.merge(df_trim, rfm, on='CustomerID')


def update_invoices_text():
    num_reco = len(df.InvoiceNo.unique())
    return (f"{num_reco:,}")


def update_items_text():
    num_reco = len(df.Description.unique())
    return (f"{num_reco:,}")


def update_customers_text():
    num_reco = len(df.CustomerID.unique())
    return (f"{num_reco:,}")


def update_countries_text():
    num_reco = len(df.Country.unique())
    return (f"{num_reco:,}")


def country_first_name():
    return most_purchased_bycountry['Country'][0]


def country_first_count():
    num_reco = most_purchased_bycountry['Count'][0]
    return (f"{num_reco:,}")


def country_second_name():
    return most_purchased_bycountry['Country'][1]


def country_second_count():
    num_reco = most_purchased_bycountry['Count'][1]
    return (f"{num_reco:,}")


def country_third_name():
    return most_purchased_bycountry['Country'][2]


def country_third_count():
    num_reco = most_purchased_bycountry['Count'][2]
    return (f"{num_reco:,}")


rfm_analysis = rfm.groupby('RFM_Score').agg({'Recency': 'mean', 'Frequency': 'mean',
                                             'MonetaryValue': ['mean', 'count']}).round(1)

rfm_analysis['RFM_Score'] = rfm_analysis.index
rfm_analysis.reset_index(drop=True, inplace=True)
rfm_analysis = rfm_analysis.iloc[:, [4, 0, 1, 2, 3]]

rfm_analysis.columns = rfm_analysis.columns.droplevel()
rfm_analysis.columns = ['RFM_Score', 'Recency', 'Frequency', 'MonetaryValue', 'Count']

general_segment_analysis = rfm.groupby('General_Segment').agg({'Recency': 'mean', 'Frequency': 'mean',
                                                               'MonetaryValue': ['mean', 'count']}).round(1)

general_segment_analysis['General_Segment'] = general_segment_analysis.index
general_segment_analysis.reset_index(drop=True, inplace=True)
general_segment_analysis = general_segment_analysis.iloc[:, [4, 0, 1, 2, 3]]

general_segment_analysis.columns = general_segment_analysis.columns.droplevel()
general_segment_analysis.columns = ['General_Segment', 'Recency', 'Frequency', 'MonetaryValue', 'Count']


def top_tier_count():
    num_reco = general_segment_analysis['Count'][2]
    return (f"{num_reco:,}")


def middle_tier_count():
    num_reco = general_segment_analysis['Count'][1]
    return (f"{num_reco:,}")


def low_tier_count():
    num_reco = general_segment_analysis['Count'][0]
    return (f"{num_reco:,}")


cluster_analysis = rfm.groupby(['Cluster']).agg({'Recency': 'mean', 'Frequency': 'mean',
                                                 'MonetaryValue': ['mean', 'count'], }).round(0)

cluster_analysis['Cluster'] = cluster_analysis.index
cluster_analysis.reset_index(drop=True, inplace=True)
cluster_analysis = cluster_analysis.iloc[:, [4, 0, 1, 2, 3]]

cluster_analysis.columns = cluster_analysis.columns.droplevel()
cluster_analysis.columns = ['Cluster', 'Recency', 'Frequency', 'MonetaryValue', 'Count']

cluster_options = []
for cluster in cluster_analysis.index:
    cluster_options.append({'label': str(cluster), 'value': cluster})

app.layout = html.Div([
    html.Div(
        [
            html.Div(
                [

                ],
                className="one-third column",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "E-Commerce Monthly Dashboard",
                                style={"margin-bottom": "0px", "width": "100%", 'font-size': '45px',
                                       'font-weight': 'bold', 'color': 'rgb(49, 69, 106)'},
                            ),
                        ]
                    )
                ],
                className="one-half column",
                id="title",
            ),
            html.Div(
                [
                    html.A(
                        html.Button("Analysis", id="learn-more-button"),
                        href="https://www.kaggle.com/vernon360961/rfm-and-cohort-analysis",
                    )
                ],
                className="one-third column",
                id="button",
            ),

        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "25px", 'font-weight': 'bold'},
    ),
    html.Div(
        [

            html.Div(
                [html.Div(
                    [html.P("Total Invoices"),
                     html.H1(id="conf_text", children=update_invoices_text(), style={'font-weight': '700'})],
                    id="invoices",
                    className="mini_container",
                    style={
                        'background-color': 'white',
                        'color': 'rgba(49,69,106,1)',
                        'font-size': '22px',
                        'text-align': 'center',
                        'flex': '1'
                    }
                ),
                    html.Div(
                        [html.P("Unique Items"),
                         html.H1(id="reco_text", children=update_items_text(), style={'font-weight': '700'})],
                        id="items",
                        className="mini_container",
                        style={
                            'background-color': 'white',
                            'color': 'rgba(49,69,106,1)',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    ),
                    html.Div(
                        [html.P("Total Customers"),
                         html.H1(id="deat_text", children=update_customers_text(), style={'font-weight': '700'})],
                        id="customers",
                        className="mini_container",
                        style={
                            'background-color': 'white',
                            'color': 'rgba(49,69,106,1)',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    ),
                    html.Div(
                        [html.P("Total Countries"),
                         html.H1(id="temp_text", children=update_countries_text(), style={'font-weight': '700'})],
                        id="countries",
                        className="mini_container",
                        style={
                            'background-color': 'white',
                            'color': 'rgba(49,69,106,1)',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    )
                ],
                id="one-info-container",
                className=" row container-display",
            ),

        ],
        className="full columns",
        style={"margin-bottom": "0px"},
    ),
    html.Div(
        [
            html.Div(
                [
                    html.H5(
                        "Top Performing Products", style={'margin-top': '40px',
                                                          'font-size': '32px',
                                                          'font-weight': '700',
                                                          'text-align': 'center',
                                                          'color': 'rgb(49, 69, 106)',
                                                          'margin-bottom': '30px'}
                    ),
                ]
            )
        ],
        className="full columns",
    )

    ,

    html.Div([

        html.Div(
            [
                html.H5(
                    "Top 20 Products", style={'margin-top': '20px',
                                              'font-size': '23px',
                                              'font-weight': '700',
                                              'text-align': 'center',
                                              'color': 'rgb(49, 69, 106)',
                                              'padding-top': '15px',
                                              'margin-bottom': '20px'
                                              }
                ),
            ]
        ),
        dash_table.DataTable(
            data=most_purchased_prods.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in most_purchased_prods.columns],
            fixed_rows={'headers': True, 'data': 0},
            sort_action="native",
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '60px',
                # 'height': 'auto',
                # all three widths are needed
                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                'whiteSpace': 'normal'
            },
            style_table={
                'height': '459px',
                'overflowX': 'hidden',
                'borderRadius': '0px'
            },
            style_header={
                "left": "50%",
                "marginRight": "-50%"
            }
        ),
        html.Div(id='datatable-interactivity-container')
    ],
        id="right-column",
        className="four columns",
        style={"margin-top": "0px"},
    ),

    html.Div(
        [

            html.Div(
                [
                    html.H5(
                        "Popular Items", style={'margin-top': '20px',
                                                'font-size': '23px',
                                                'font-weight': '700',
                                                'text-align': 'center',
                                                'color': 'rgb(49, 69, 106)',
                                                'padding-top': '15px',
                                                'margin-bottom': '20px'
                                                }
                    ),
                ]
            ),
            html.Div(
                [dcc.Graph(
                    id='scatter10',
                    figure={
                        'data': [

                            go.Scatter(
                                x=most_purchased_prods['Item'],
                                y=most_purchased_prods['Count'],
                                marker=dict(color="green", size=12),
                                mode="lines+markers",
                                name="Recovered",
                            )
                        ],
                        'layout': go.Layout(
                            # title = 'Countries Most Affected by the Corona Virus',
                            xaxis={'fixedrange': True},
                            yaxis={'fixedrange': True},
                            hovermode='closest'
                        )
                    }
                )],
                id="compGraphContainer",
                className="pretty_container",
                style={
                    'background-color': '#ffffff',
                    'padding': '5px',
                }
            ),

        ],
        className="eight columns",
    ),
    html.Div(
        [
            html.Div(
                [
                    html.H5(
                        "Top Performing Countries", style={'margin-top': '40px',
                                                           'font-size': '32px',
                                                           'font-weight': '700',
                                                           'text-align': 'center',
                                                           'color': 'rgb(49, 69, 106)',
                                                           'margin-bottom': '30px'}
                    ),
                ]
            )
        ],
        className="full columns",
    ),

    html.Div(
        [

            html.Div(
                [html.Div(
                    [html.P(children=country_first_name()),
                     html.H1(id="country_first_count", children=country_first_count(), style={'font-weight': '700'})],
                    id="country_first_count_1",
                    className="mini_container",
                    style={
                        'background-color': 'white',
                        'color': 'rgba(49,69,106,1)',
                        'font-size': '22px',
                        'text-align': 'center',
                        'flex': '1'
                    }
                ),
                    html.Div(
                        [html.P(children=country_second_name()),
                         html.H1(id="country_second_count", children=country_second_count(),
                                 style={'font-weight': '700'})],
                        id="country_second_count_1",
                        className="mini_container",
                        style={
                            'background-color': 'white',
                            'color': 'rgba(49,69,106,1)',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    ),

                    html.Div(
                        [html.P(children=country_third_name()),
                         html.H1(id="country_third_count", children=country_third_count(),
                                 style={'font-weight': '700'})],
                        id="country_third_count_1",
                        className="mini_container",
                        style={
                            'background-color': 'white',
                            'color': 'rgba(49,69,106,1)',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    )
                ],
                id="one-info-container-1",
                className=" row container-display",
            ),

        ],
        className="full columns",
        style={"margin-bottom": "0px"},
    ),

    html.Div([

        html.Div(
            [
                html.H5(
                    "Top 10 Countries", style={'margin-top': '20px',
                                               'font-size': '23px',
                                               'font-weight': '700',
                                               'text-align': 'center',
                                               'color': 'rgb(49, 69, 106)',
                                               'padding-top': '15px',
                                               'margin-bottom': '20px'
                                               }
                ),
            ]
        ),
        dash_table.DataTable(
            data=most_purchased_bycountry_10.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in most_purchased_bycountry_10.columns],
            fixed_rows={'headers': True, 'data': 0},
            sort_action="native",
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '60px',
                # 'height': 'auto',
                # all three widths are needed
                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                'whiteSpace': 'normal'
            },
            style_table={
                'height': '459px',
                'overflowX': 'hidden',
                'borderRadius': '0px'
            },
            style_header={
                "left": "50%",
                "marginRight": "-50%"
            }
        ),
        html.Div(id='datatable-interactivity-container-1')
    ],
        id="right-column-1",
        className="four columns",
        style={"margin-top": "0px"},
    ),

    html.Div(
        [

            html.Div(
                [
                    html.H5(
                        "Top Countries Excluding UK", style={'margin-top': '20px',
                                                             'font-size': '23px',
                                                             'font-weight': '700',
                                                             'text-align': 'center',
                                                             'color': 'rgb(49, 69, 106)',
                                                             'padding-top': '15px',
                                                             'margin-bottom': '20px'
                                                             }
                    ),
                ]
            ),
            html.Div(
                [dcc.Graph(
                    id='bar',
                    figure={
                        'data': [

                            go.Bar(
                                x=most_purchased_bycountry_nonuk['Country'],
                                y=most_purchased_bycountry_nonuk['Count'],
                                name='Confirmed',
                                marker=dict(color='crimson')
                            )
                        ],
                        'layout': go.Layout(
                            # title = 'Countries Most Affected by the Corona Virus',
                            xaxis={'fixedrange': True},
                            yaxis={'fixedrange': True},
                            hovermode='closest'
                        )
                    }
                )],
                id="compGraphContainer-1",
                className="pretty_container",
                style={
                    'background-color': '#ffffff',
                    'padding': '5px',
                }
            ),

        ],
        className="eight columns",
    )

    ,
    html.Div(
        [
            html.Div(
                [
                    html.H5(
                        "Customer Insights", style={'margin-top': '40px',
                                                    'font-size': '32px',
                                                    'font-weight': '700',
                                                    'text-align': 'center',
                                                    'color': 'rgb(49, 69, 106)',
                                                    'margin-bottom': '30px'}
                    ),
                ]
            )
        ],
        className="full columns",
    ),

    html.Div(
        [

            html.Div(
                [
                    html.H5(
                        "Time of Purchase", style={'margin-top': '20px',
                                                   'font-size': '23px',
                                                   'font-weight': '700',
                                                   'text-align': 'center',
                                                   'color': 'rgb(49, 69, 106)',
                                                   'padding-top': '15px',
                                                   'margin-bottom': '20px'
                                                   }
                    ),
                ]
            ),
            html.Div(
                [dcc.Graph(
                    id='scatter-2',
                    figure={
                        'data': [
                            go.Scatter(

                                x=time_of_purchase.index,
                                y=time_of_purchase['Count'],
                                marker_color=time_of_purchase['Count'],
                                mode='markers'
                            )

                        ],
                        'layout': go.Layout(
                            # title = 'Countries Most Affected by the Corona Virus',
                            xaxis={'showgrid': False, 'fixedrange': True},
                            yaxis={'title': 'No. of Purchases', 'showgrid': False, 'fixedrange': True},
                            hovermode='closest'
                        )
                    }
                )],
                id="confworldGraphContainer-3",
                className="pretty_container",
                style={
                    'background-color': '#ffffff',
                    'padding': '5px',
                }
            ),

        ],
        className="full columns",
    )

    ,
    html.Div(
        [
            html.Div(
                [
                    html.H5(
                        "RFM Analysis", style={'margin-top': '40px',
                                               'font-size': '32px',
                                               'font-weight': '700',
                                               'text-align': 'center',
                                               'color': 'rgb(49, 69, 106)',
                                               'margin-bottom': '30px'}
                    ),
                ]
            )
        ],
        className="full columns",
    ),

    html.Div([

        html.Div(
            [
                html.H5(
                    "RFM Score Analysis", style={'margin-top': '20px',
                                                 'font-size': '23px',
                                                 'font-weight': '700',
                                                 'text-align': 'center',
                                                 'color': 'rgb(49, 69, 106)',
                                                 'padding-top': '15px',
                                                 'margin-bottom': '20px'
                                                 }
                ),
            ]
        ),
        dash_table.DataTable(
            data=rfm_analysis.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in rfm_analysis.columns],
            fixed_rows={'headers': True, 'data': 0},
            sort_action="native",
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '60px',
                # 'height': 'auto',
                # all three widths are needed
                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                'whiteSpace': 'normal'
            },
            style_table={
                'height': '459px',
                'overflowX': 'hidden',
                'borderRadius': '0px'
            },
            style_header={
                "left": "50%",
                "marginRight": "-50%"
            }
        ),
        html.Div(id='datatable-interactivity-container-1a')
    ],
        id="right-column-1a",
        className="four columns",
        style={"margin-top": "0px"},
    ),

    html.Div(
        [

            html.Div(
                [
                    html.H5(
                        "Avg. RFM values by RFM Score", style={'margin-top': '20px',
                                                               'font-size': '23px',
                                                               'font-weight': '700',
                                                               'text-align': 'center',
                                                               'color': 'rgb(49, 69, 106)',
                                                               'padding-top': '15px',
                                                               'margin-bottom': '20px'
                                                               }
                    ),
                ]
            ),
            html.Div(
                [dcc.Graph(
                    id='scatter3a',
                    figure={
                        'data': [
                            go.Bar(
                                x=rfm_analysis['RFM_Score'],
                                y=rfm_analysis['Recency'],
                                name='Avg. Recency',
                                marker=dict(color='#1E88E5')
                            ),
                            go.Bar(
                                x=rfm_analysis['RFM_Score'],
                                y=rfm_analysis['Frequency'],
                                name='Avg. Frequency',
                                marker=dict(color='#43A047')
                            ),
                            go.Bar(
                                x=rfm_analysis['RFM_Score'],
                                y=rfm_analysis['MonetaryValue'],
                                name='Avg. MonetaryValue',
                                marker=dict(color='#E53935')
                            )
                        ],
                        'layout': go.Layout(
                            # title = 'Countries Most Affected by the Corona Virus',
                            xaxis={'showgrid': False, 'fixedrange': True, 'title': 'RFM Score', 'tickmode': 'linear'},
                            yaxis={'showgrid': False, 'fixedrange': True},
                            hovermode='closest',
                            yaxis_type='log'
                        )
                    }
                )],
                id="countGraphContaineraaa",
                className="pretty_container",
                style={
                    'background-color': '#ffffff',
                    'padding': '5px',
                }
            ),

        ],
        className="eight columns",
    ),

    html.Div(
        [
            html.Div(
                [
                    html.H5(
                        "General Segmentation Count", style={'margin-top': '40px',
                                                             'font-size': '32px',
                                                             'font-weight': '700',
                                                             'text-align': 'center',
                                                             'color': 'rgb(49, 69, 106)',
                                                             'margin-bottom': '30px'}
                    ),
                ]
            )
        ],
        className="full columns",
    ),

    html.Div(
        [

            html.Div(
                [html.Div(
                    [html.P(children="Top Tier Customers"),
                     html.H1(id="top_tier_count", children=top_tier_count(), style={'font-weight': '700'})],
                    id="top_tier_count_1",
                    className="mini_container",
                    style={
                        'background-color': 'white',
                        'color': 'rgba(49,69,106,1)',
                        'font-size': '22px',
                        'text-align': 'center',
                        'flex': '1'
                    }
                ),
                    html.Div(
                        [html.P(children="Middle Tier Customers"),
                         html.H1(id="middle_tier_count", children=middle_tier_count(), style={'font-weight': '700'})],
                        id="middle_tier_count_1",
                        className="mini_container",
                        style={
                            'background-color': 'white',
                            'color': 'rgba(49,69,106,1)',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    ),

                    html.Div(
                        [html.P(children="Low Tier Customers"),
                         html.H1(id="low_tier_count", children=low_tier_count(), style={'font-weight': '700'})],
                        id="low_tier_count_1",
                        className="mini_container",
                        style={
                            'background-color': 'white',
                            'color': 'rgba(49,69,106,1)',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    )
                ],
                id="one-info-container-1a",
                className=" row container-display",
            ),

        ],
        className="full columns",
        style={"margin-bottom": "0px"},
    )
    ,

    html.Div(
        [
            html.Div(
                [
                    html.H5(
                        "Machine Learning Segmentation (Clustering)", style={'margin-top': '40px',
                                                                             'font-size': '32px',
                                                                             'font-weight': '700',
                                                                             'text-align': 'center',
                                                                             'color': 'rgb(49, 69, 106)',
                                                                             'margin-bottom': '30px'}
                    ),
                ]
            )
        ],
        className="full columns",
    )

    ,

    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H5(
                                "Filter By Cluster", style={'margin-top': '60px',
                                                            'font-size': '22px',
                                                            'font-weight': '700',
                                                            'text-align': 'center',
                                                            'color': 'rgb(49, 69, 106)',
                                                            'margin-left': '10px',
                                                            'margin-bottom': '10px'}
                            ),
                        ]
                    )
                ]
            ),
            html.Div(
                [dcc.Dropdown(id='cluster-picker', options=cluster_options, value=cluster_analysis.index[0])],
                id="cGraphContaineras",
                className="pretty_container",
                style={
                    'background-color': '#ffffff',
                    'padding': '0px',
                }
            ),
            html.Div(
                [
                    html.Div(
                        [html.P("Avg. Recency"), html.H1(id="recency_text", style={'font-weight': '700'})],
                        id="recency_text_a",
                        className="mini_container",
                        style={
                            'background-color': '#538cea',
                            'color': 'white',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    ),
                    html.Div(
                        [html.P("Avg. Frequency"), html.H1(id="frequency_text", style={'font-weight': '700'})],
                        id="frequency_text_a",
                        className="mini_container",
                        style={
                            'background-color': '#4cc770',
                            'color': 'white',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    ),
                    html.Div(
                        [html.P("Avg. Monetary Value"), html.H1(id="monetary_text", style={'font-weight': '700'})],
                        id="monetary_text_a",
                        className="mini_container",
                        style={
                            'background-color': '#cc4b4b',
                            'color': 'white',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    ),
                    html.Div(
                        [html.P("Count"), html.H1(id="count_text", style={'font-weight': '700'})],
                        id="count_text_a",
                        className="mini_container",
                        style={
                            'background-color': 'rgb(50, 50, 156)',
                            'color': 'white',
                            'font-size': '22px',
                            'text-align': 'center',
                            'flex': '1'
                        }
                    )
                ],
                id="country-info-container-a",
                className="row container-display",
            )
        ],
        className="full columns",
    )

    ,

    html.Div(
        [

            html.Div(
                [
                    html.H5(
                        "Visualizing Clusters", style={'margin-top': '20px',
                                                       'font-size': '23px',
                                                       'font-weight': '700',
                                                       'text-align': 'center',
                                                       'color': 'rgb(49, 69, 106)',
                                                       'padding-top': '15px',
                                                       'margin-bottom': '20px'
                                                       }
                    ),
                ]
            ),
            html.Div(
                [dcc.Graph(
                    id='scatter3aa',
                    figure={
                        'data': [
                            go.Scatter3d(x=rfm_norm['Recency'], y=rfm_norm['Frequency'], z=rfm_norm['MonetaryValue'],
                                         mode='markers', marker=dict(
                                    size=3,
                                    color=rfm_norm['Cluster'],
                                    colorscale='Viridis',
                                    opacity=0.6
                                ))
                        ],
                        'layout': go.Layout(
                            # title = 'Countries Most Affected by the Corona Virus',
                            xaxis={'showgrid': False, 'fixedrange': True},
                            yaxis={'showgrid': False, 'fixedrange': True},
                            hovermode='closest',
                            scene=dict(
                                xaxis=dict(
                                    title='Recency'),
                                yaxis=dict(
                                    title='Frequency'),
                                zaxis=dict(
                                    title='MonetaryValue'), ),
                        )
                    }
                )],
                id="countGraphContaineraaaa",
                className="pretty_container",
                style={
                    'background-color': '#ffffff',
                    'padding': '5px',
                }
            ),

        ],
        className="four columns",
    )
    ,

    html.Div(
        [

            html.Div(
                [
                    html.H5(
                        "Comparing RFM values by Cluster", style={'margin-top': '20px',
                                                                  'font-size': '23px',
                                                                  'font-weight': '700',
                                                                  'text-align': 'center',
                                                                  'color': 'rgb(49, 69, 106)',
                                                                  'padding-top': '15px',
                                                                  'margin-bottom': '20px'
                                                                  }
                    ),
                ]
            ),
            html.Div(
                [dcc.Graph(
                    id='scatter3ab',
                    figure={
                        'data': [
                            go.Bar(
                                x=cluster_analysis['Cluster'],
                                y=cluster_analysis['Recency'],
                                name='Avg. Recency',
                                marker=dict(color='#1E88E5')
                            ),
                            go.Bar(
                                x=cluster_analysis['Cluster'],
                                y=cluster_analysis['Frequency'],
                                name='Avg. Frequency',
                                marker=dict(color='#43A047')
                            ),
                            go.Bar(
                                x=cluster_analysis['Cluster'],
                                y=cluster_analysis['MonetaryValue'],
                                name='Avg. MonetaryValue',
                                marker=dict(color='#E53935')
                            )
                        ],
                        'layout': go.Layout(
                            # title = 'Countries Most Affected by the Corona Virus',
                            xaxis={'showgrid': False, 'fixedrange': True, 'tickmode': 'linear', 'title': 'Cluster'},
                            yaxis={'showgrid': False, 'fixedrange': True},
                            hovermode='closest',
                            yaxis_type='log'
                        )
                    }
                )],
                id="countGraphContaineraaaaa",
                className="pretty_container",
                style={
                    'background-color': '#ffffff',
                    'padding': '5px',
                }
            ),

        ],
        className="eight columns",
    ),

    html.Div([

        html.Div(
            [
                html.H5(
                    "Avg. RFM values by Cluster", style={'margin-top': '20px',
                                                         'font-size': '23px',
                                                         'font-weight': '700',
                                                         'text-align': 'center',
                                                         'color': 'rgb(49, 69, 106)',
                                                         'padding-top': '15px',
                                                         'margin-bottom': '20px'
                                                         }
                ),
            ]
        ),
        dash_table.DataTable(
            data=cluster_analysis.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in cluster_analysis.columns],
            fixed_rows={'headers': True, 'data': 0},
            sort_action="native",
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '60px',
                # 'height': 'auto',
                # all three widths are needed
                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                'whiteSpace': 'normal'
            },
            style_table={
                'height': '459px',
                'overflowX': 'hidden',
                'borderRadius': '0px'
            },
            style_header={
                "left": "50%",
                "marginRight": "-50%"
            }
        ),
        html.Div(id='datatable-interactivity-container-1aaa')
    ],
        id="right-column-1aaa",
        className="full columns",
        style={"margin-top": "0px"},
    )

    ,

    html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.H5(
                            "Author: Vernon Fernandes", style={'margin-top': '20px',
                                                               'font-size': '14px',
                                                               'text-align': 'center',
                                                               'color': 'rgb(49, 69, 106)',
                                                               'padding-top': '15px',
                                                               'margin-bottom': '20px'
                                                               }
                        ),
                        href="http://vernonfernandes.net/",
                    )
                ],
                className="full columns",
            )
        ]
    )

])


@app.callback(
    Output("recency_text", "children"),
    [Input('cluster-picker', 'value')],
)
def update_rec_text(selected_cluster):
    filtered_recency_text = cluster_analysis[cluster_analysis['Cluster'] == selected_cluster]

    num_count_rec = filtered_recency_text['Recency']
    return num_count_rec


@app.callback(
    Output("frequency_text", "children"),
    [Input('cluster-picker', 'value')],
)
def update_freq_text(selected_cluster):
    filtered_freq_text = cluster_analysis[cluster_analysis['Cluster'] == selected_cluster]

    num_count_freq = filtered_freq_text['Frequency']
    return num_count_freq


@app.callback(
    Output("monetary_text", "children"),
    [Input('cluster-picker', 'value')],
)
def update_mon_text(selected_cluster):
    filtered_mon_text = cluster_analysis[cluster_analysis['Cluster'] == selected_cluster]

    num_count_mon = filtered_mon_text['MonetaryValue']
    return num_count_mon


@app.callback(
    Output("count_text", "children"),
    [Input('cluster-picker', 'value')],
)
def update_count_text(selected_cluster):
    filtered_count_text = cluster_analysis[cluster_analysis['Cluster'] == selected_cluster]

    num_count_count = filtered_count_text['Count']
    return num_count_count
