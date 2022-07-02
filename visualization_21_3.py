"""Visualization for 2021 March"""

import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv('../../Data/Visualization/covid_21_03.csv')
df.head()

df['text'] = df['province'] + '<br>Active cases: ' + df['active cases'].astype(str)
limits_1 = [(0, 35007)]
colors = ["royalblue"]
scale = 12.8

fig = go.Figure()

for i in range(len(limits_1)):
    lim = limits_1[i]
    df_sub = df[lim[0]:lim[1]]
    fig.add_trace(go.Scattergeo(
        locationmode='USA-states',
        lon=df_sub['lon'],
        lat=df_sub['lat'],
        text=df_sub['text'],
        marker=dict(
            size=df_sub['active cases'] / scale,
            color=colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode='area'
        ),
        name='{0} - {1}'.format(lim[0], lim[1])))

dg = pd.read_csv('../../Data/Visualization/crime_21_03.csv')
dg.head()

dg['text'] = dg['province'] + '<br>Crime cases: ' + dg['crime cases'].astype(str)
limits_2 = [(0, 44745)]
colors = ["crimson"]
scale = 10

for j in range(len(limits_2)):
    lim = limits_2[j]
    dg_sub = dg[lim[0]:lim[1]]
    fig.add_trace(go.Scattergeo(
        locationmode='USA-states',
        lon=dg_sub['lon'],
        lat=dg_sub['lat'],
        text=dg_sub['text'],
        marker=dict(
            size=dg_sub['crime cases'] / scale,
            color=colors[j],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode='area'
        ),
        name='{0} - {1}'.format(lim[0], lim[1])))

fig.update_layout(
    title_text='2021 March Covid-19 vs. Crimes',
    showlegend=True,
    geo=dict(
        visible=True, resolution=50, scope="north america",
        landcolor='rgb(217, 217, 217)',
        showcountries=True, countrycolor="White",
        showsubunits=True, subunitcolor="White",
        lataxis=dict(
            showgrid=True,
            gridwidth=0.5,
            range=[42, 83],
            dtick=5
        ),
        lonaxis=dict(
            showgrid=True,
            gridwidth=0.5,
            range=[-141, -53],
            dtick=5
        )),
    height=800
    )

fig.show()
