from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import logging
import pandas as pd
import numpy as np
from django.conf import settings
import plotly.offline as py
import plotly.tools as tls
import json
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as ctls
from chart_studio.grid_objs import Column, Grid
from plotly.subplots import make_subplots
import plotly.figure_factory as ff



# marker=dict(color='rgb(0,0,0)' ,size=8)
# plot_bgcolor='rgba(100,0,100,0)'


class Plotly:
    list = []
    #basic charts

    def scatter(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        trace1 = go.Scatter(df,
                            x=x_data, y=y_data, mode='markers', name='points',
                            marker=dict(size=8, opacity=0.4)
                            )
        data = [trace1]
        layout = go.Layout(
            showlegend=True,
            autosize=True,
            # width=800,
            height=800,
            xaxis=dict(
                domain=[0, 0.85],
                showgrid=True,
                zeroline=False
            ),
            yaxis=dict(
                domain=[0, 0.85],
                showgrid=True,
                zeroline=False
            ),
            margin=dict(
                t=50
            ),
            hovermode='closest',
            bargap=0,
        )

        fig = go.Figure(data=data, layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def Scatter(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.scatter(df, x=x_data, y=y_data, color=color,)
        fig.update_layout( template="plotly_white")
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "line"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "pie"],
                            label="Pie",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "violin"],
                            label="Violin",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "box"],
                            label="Box",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.250,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.4,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def line(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.line(df, x=x_data, y=y_data, color=color,)
        fig.update_layout( template="plotly_white")
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "line"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "pie"],
                            label="Pie",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "violin"],
                            label="Violin",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "box"],
                            label="Box",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.250,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.4,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def bar(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.histogram(df, x=x_data, color=color,)
        fig.update_layout( template="plotly_white")
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "line"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "pie"],
                            label="Pie",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "violin"],
                            label="Violin",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "box"],
                            label="Box",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.250,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.4,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def pie(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.pie(df, values=y_data, names=x_data,)
        fig.update_layout( template="plotly_white")
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "line"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "pie"],
                            label="Pie",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "violin"],
                            label="Violin",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "box"],
                            label="Box",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.250,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.4,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def bubble(x_data,y_data,f,color):
        df = px.data.gapminder()
        fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",
                         size="pop", color="continent",
                         hover_name="country", log_x=True, size_max=60)
        fig.update_layout(template="plotly_white")
        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def gantt(x_data,y_data,f,color):
        df = [dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'),
              dict(Task="Job-1", Start='2017-02-15', Finish='2017-03-15', Resource='Incomplete'),
              dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Not Started'),
              dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Complete'),
              dict(Task="Job-3", Start='2017-03-10', Finish='2017-03-20', Resource='Not Started'),
              dict(Task="Job-3", Start='2017-04-01', Finish='2017-04-20', Resource='Not Started'),
              dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
              dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')]

        colors = {'Not Started': 'rgb(220, 0, 0)',
                  'Incomplete': (1, 0.9, 0.16),
                  'Complete': 'rgb(0, 255, 100)'}

        fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                              group_tasks=True)
        fig.update_layout(template="plotly_white")

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def hrbar(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                            shared_yaxes=False, vertical_spacing=0.001)

        fig.append_trace(go.Bar(
            x=df[y_data],
            y=df[x_data],
            marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ),
            #name='Household savings, percentage of household disposable income',
            orientation='h',
        ), 1, 1)

        fig.append_trace(go.Scatter(
            x=df[y_data], y=df[x_data],
            mode='lines+markers',
            line_color='rgb(128, 0, 128)',
            #name='Household net worth, Million USD/capita',
        ), 1, 2)

        fig.update_layout(
            title='Household savings & net worth for eight OECD countries',
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                domain=[0, 0.85],
            ),
            yaxis2=dict(
                showgrid=False,
                showline=True,
                showticklabels=False,
                linecolor='rgba(102, 102, 102, 0.8)',
                linewidth=2,
                domain=[0, 0.85],
            ),
            xaxis=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                domain=[0, 0.42],
            ),
            xaxis2=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                domain=[0.47, 1],
                side='top',
                dtick=25000,
            ),
            legend=dict(x=0.029, y=1.038, font_size=10),
            margin=dict(l=100, r=20, t=70, b=70),
            paper_bgcolor='rgb(248, 248, 255)',
            plot_bgcolor='rgb(248, 248, 255)',
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div


    #Statistical Charts

    def box(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.box(df, x=x_data, y=y_data, color=color,)
        fig.update_layout(template="plotly_white")
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "line"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "pie"],
                            label="Pie",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "violin"],
                            label="Violin",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "box"],
                            label="Box",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.250,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.4,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),

            ],
            autosize=True,
            height = 600,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def violin(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.violin(df, x=x_data, y=y_data, color=color, height=500)
        fig.update_layout(template="plotly_white")
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "line"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "pie"],
                            label="Pie",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "violin"],
                            label="Violin",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "box"],
                            label="Box",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.250,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.4,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def box_scatter(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.box(df, x=x_data, y=y_data, color=color, height=500, points="all")
        fig.update_layout(template="plotly_white")
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "line"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "pie"],
                            label="Pie",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "violin"],
                            label="Violin",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "box"],
                            label="Box",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.250,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.4,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def violin_box(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.violin(df, x=x_data, y=y_data, color=color, height=500, box=True)
        fig.update_layout(template="plotly_white")
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "line"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "pie"],
                            label="Pie",
                            method="restyle"
                        ),
                        dict(
                             args=["type", "violin"],
                            label="Violin",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "box"],
                            label="Box",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.250,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.4,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def violn_box_scatter(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.violin(df, x=x_data, y=y_data, color=color, height=500, box=True, points='all',
                          animation_frame='Month Name')

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown

            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def distplot(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = ff.create_distplot(df[y_data], df[x_data], bin_size=.2)
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "line"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "pie"],
                            label="Pie",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "violin"],
                            label="Violin",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "box"],
                            label="Box",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.3,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.250,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.4,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def histogram2d(x_data, y_data, f):
        t = np.linspace(-1, 1.2, 2000)
        x = (t ** 3) + (0.3 * np.random.randn(2000))
        y = (t ** 6) + (0.3 * np.random.randn(2000))

        fig = go.Figure()
        fig.add_trace(go.Histogram2dContour(
            x=x,
            y=y,
            colorscale='Blues',
            reversescale=True,
            xaxis='x',
            yaxis='y'
        ))
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            xaxis='x',
            yaxis='y',
            mode='markers',
            marker=dict(
                color='rgba(0,0,0,0.3)',
                size=3
            )
        ))
        fig.add_trace(go.Histogram(
            y=y,
            xaxis='x2',
            marker=dict(
                color='rgba(0,0,0,1)'
            )
        ))
        fig.add_trace(go.Histogram(
            x=x,
            yaxis='y2',
            marker=dict(
                color='rgba(0,0,0,1)'
            )
        ))

        fig.update_layout(
            autosize=False,
            xaxis=dict(
                zeroline=False,
                domain=[0, 0.85],
                showgrid=False
            ),
            yaxis=dict(
                zeroline=False,
                domain=[0, 0.85],
                showgrid=False
            ),
            xaxis2=dict(
                zeroline=False,
                domain=[0.85, 1],
                showgrid=False
            ),
            yaxis2=dict(
                zeroline=False,
                domain=[0.85, 1],
                showgrid=False
            ),
            height=800,
            width = 1000,
            bargap=0,
            hovermode='closest',
            showlegend=False
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def strip(x_data, y_data, f,color):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.strip(df, x=x_data, y=y_data, color=color, animation_frame='Year', height=600)
        #fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "line"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "pie"],
                            label="Pie",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "violin"],
                            label="Violin",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "box"],
                            label="Box",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
                dict(
                    buttons=list(xbutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.250,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"

                ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.4,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True,
            template="plotly_white"
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    #ai and ml charts
    def ols(self):
        df = px.data.tips()
        fig = px.scatter(
            df, x='total_bill', y='tip', opacity=0.65,
            trendline='ols', trendline_color_override='darkblue'
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div

    def new(x_data, y_data, f):
        df = pd.read_csv(settings.MEDIA_ROOT + '/' + f)
        fig = px.scatter(df, y=y_data, x=x_data)
        xbutton = []
        ybutton = []
        for col in df.columns:
            xbutton.append(
                dict(
                    args=['x', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )
        for col in df.columns:
            ybutton.append(
                dict(
                    args=['y', [df[str(col)]]],
                    label=str(col),
                    method='restyle'
                ),
            )

        fig.update_layout(
            title="graph",
            yaxis_title="s",
            xaxis_title="activity",
            # Add dropdown
            updatemenus=[
               dict(
                   buttons=list(xbutton),
                   direction="down",
                   pad={"r": 10, "t": 10},
                   showactive=True,
                   x=0.1,
                   xanchor="left",
                   y=1.2,
                   yanchor="top"

               ),
                dict(
                    buttons=list(ybutton),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.37,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            autosize=True
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div
