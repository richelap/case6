# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 09:49:36 2021

@author: EFLCAdmin
"""

#%%
import dash
import dash_html_components as html
import dash_core_components as dcc
import requests
totalHits = 1000000
conversionRate = 60
revenuePerPurchase = 50
ntpcuy =2
samplingCost = 25000000
potentialRevenue = 50

tpar = float(totalHits) * float(revenuePerPurchase) * float(ntpcuy)
uor = (1 - float(conversionRate)/100) * tpar
convertedRev = (float(conversionRate)/100) * tpar
netProfit = convertedRev - float(samplingCost)
netProfitNFS = (1 - float(potentialRevenue)/100) * netProfit
MaxAllowSpend = (float(potentialRevenue)/100) * netProfit
MaxSpendPerHit = float(MaxAllowSpend/totalHits)


a = ['Unconverted Revenue', 'Sampling Cost', 'Max Allowable Spend', 'Net Profit Not For Sampling']
b = [uor, samplingCost, MaxAllowSpend, netProfitNFS]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs([
         dcc.Tab(label='Current Flights', children=[
            html.Div([
            
                html.Div([
                html.Pre(
                    id='counter_text',
                    children='Active flights worldwide:'
                ),
                dcc.Graph(id='live-update-graph',style={'width':1200}),
                dcc.Interval(
                    id='interval-component',
                    interval=6000, # 6000 milliseconds = 6 seconds
                    n_intervals=0
                )])
            ])
        ]),       
        dcc.Tab(label='ROI App', children=[
        html.Div([
                html.Div(style = {'background-color':'rgb(0,123,255)', 'width':'100%', 'height':40}),
                html.Div([
                        html.Div([
                                html.H2("Return of Investments Inputs:", style = {'color':'rgb(0,123,255)'}),
                                html.Table([                          
                                        html.Tr(children = [
                                            html.Td("Total Hits:", style={'width': '50%'}),
                                                            
                                            html.Td(
                                                dcc.Input(id = 'totalHits', type='number', value = 1000000, style = {'fontSize': 20})
                                                )
                                        ]),
                                       
                                        html.Tr(children = [
                                            html.Td("Conversion Rate:", style={'width': '50%'}),
                                                            
                                            html.Td(
                                                dcc.Input(id = 'conversionRate', type='number', value = 60, style = {'fontSize': 20})
                                                )
                                        ]),
                                        html.Tr(children = [
                                            html.Td("Revenue Per Purchase (PhP):", style={'width': '50%'}),
                                                            
                                            html.Td(
                                                dcc.Input(id = 'revenuePerPurchase', type='number', value = 50, style = {'fontSize': 20})
                                            )
                                        ]),
                                        html.Tr(children = [
                                            html.Td("Number of Times of Purchase per Converted User per Year:", className='lined', style={'width': '50%'}),
                                                            
                                            html.Td(
                                                dcc.Input(id = 'ntpcuy', type='number', value = 2, style = {'fontSize': 20})
                                            )
                                        ]),
                                        html.Tr(children = [
                                            html.Td("Total Cost of Sampling (PhP):", style={'width': '50%'}),
                                                            
                                            html.Td(
                                                dcc.Input(id = 'samplingCost', type='number', value = 25000000, style = {'fontSize': 20})
                                            )
                                        ]),
                                        html.Tr(children = [
                                            html.Td("% of Potential Revenue You are willing to allocate for sampling", style={'width': '50%'}),
                                                            
                                            html.Td(
                                                dcc.Input(id = 'potentialRevenue', type='number', value = 50, style = {'fontSize': 20})
                                            )
                                        ]),
                                ], style = {'width':'100%'}),
                                html.Hr(),
                                html.Button(id = 'submitButton',
                                    children = 'Calculate ROI',
                                    n_clicks = 0, className='btn btn-primary btn',
                                    style = {'fontSize': '15px', 'color':'white', 'background-color':'rgb(0,123,255)', 'float':'right', 'border-radius':'5px', 'border':'5px','padding':'10px'}
                                ),
                        ], style = {'width':'30%', 'display':'inline-block', 'float':'left', 'marginTop':'0px'}),
        
                        html.Div([
                                html.H2(children='Investment/Income Breakdown:', style = {'textAlign':'center', 'color':'rgb(0,123,255)', 'font':'Verdana'}),
                                dcc.Graph(id = 'donut', 
                                    style = {'height':300}, 
                                    config = {
                                            'displayModeBar':False,
                                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']},
                                    figure = { "data": [{
                                            "values": b,
                                            "labels": a,
                                            "marker": {
                                                    'colors':['rgb(242, 217, 187)',
                                                    'rgb(44,82,103)',
                                                    'rgb(134, 169, 189)',
                                                    'rgb(255, 59, 60)'],
                                                      'line':{'colors':['rgba(1,1,1,0)'], 'width': 2}
                                                    },
                                            "hoverinfo":"label+percent",
                                            "hole": .4,
                                            "type": "pie",
                                            'textposition':'outside',
                                            'outsidetextfont':{"size":11},
                                            "textinfo":"label+value"
                                          }],
                                          'layout': {#'title': 'Investment or Income Breakdown',
                                                     'showlegend': False,
                                                     'margin':dict(t = 0)},
                                                      'config':{
                                                          'displayModeBar':False,
                                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                                      }
                                ),
                                html.H2(children='ROI Parameters Computed:', style = {'color':'rgb(0,123,255)', 'font':'Verdana', 'textAlign':'center'}),
                                html.Table([
                                        html.Tr(children = [
                                            html.Td("Total Potential Annual Revenue",style={'width': 150, 'border':'1px solid black', 'fontSize':15}),
                                                        
                                            html.Td(
                                                html.Div(id = 'tparOutput',children=tpar , style = {'float':'right'}
                                            ), style={'width': 200, 'border':'1px solid black'})
                                        ], style = {'height':'10%'}),
                                        html.Tr(children = [
                                            html.Td("Unconverted Opportunity Revenue",style={'width': 150, 'border':'1px solid black'}),
                                                        
                                            html.Td(
                                                html.Div(id = 'uorOutput',children=uor, style = {'float':'right'}
                                            ),style={'width': 200, 'border':'1px solid black'})
                                        ]),
                                        html.Tr(children = [
                                            html.Td("Converted Revenue",style={'width': 150, 'border':'1px solid black'}),
                                                        
                                            html.Td(
                                                html.Div(id = 'convertedRev',children=convertedRev, style = {'float':'right'}
                                            ), style={'width': 200, 'border':'1px solid black'})
                                        ]),
                                        html.Tr(children = [
                                            html.Td("Maximum Allowable Spend",style={'width': 150, 'border':'1px solid black'}),
                                            
                                            html.Td(
                                                html.Div(id = 'MaxAllowSpend',children=MaxAllowSpend, style = {'float':'right'}
                                            ), style={'width': 200, 'border':'1px solid black'})
                                        ]),
                                        html.Tr(children = [
                                            html.Td("Maximum Spend per Hit",style={'width': '60%', 'border':'1px solid black'}),
                                                        
                                            html.Td(
                                                html.Div(id = 'MaxSpendPerHit',children=MaxSpendPerHit, style = {'float':'right'}
                                            ), style={'width': '40%', 'border':'1px solid black'})
                                        ])
                                ], style = {'border-collapse':'collapse', 'width':'100%'}),
                                html.H2(children = "Estimated Net Profit From Sampling:", style = {'color':'rgb(0,123,255)', 'font':'Verdana', 'textAlign':'center'}),
                                html.Table([
                                        html.Tr(children = [
                                            html.Td("Net Profit",style={'width': '30%', 'border':'1px solid black'}),
                                                
                                            html.Td(
                                                html.Div(id = 'netProfit',children=netProfit, style = {'float':'right'}
                                            ), style={'width': '70%', 'border':'1px solid black'})
                                        ])
                                ], style ={'border-collapse':'collapse', 'width':'100%'})
                        ], className='cmd', style = {'width':'35%', 'display':'inline-block','float':'left'}),
        
                        html.Div([
                                html.H2("Waterfall Chart", style = {'textAlign':'center', 'color':'rgb(0,123,255)', 'font':'Verdana', 'height':'10vh'}),
                                dcc.Graph(id = 'waterfall',
                                    figure = {
                                        'data': [
                                                {'labels':['tpar','uor'],
                                                  'x':['Total Potential Annual Revenue', 'Unconverted Opportunity Revenue'],
                                                  'y':[tpar,-uor],
                                                  'type':'waterfall',
                                                  'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                                                  'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                                                  'connector': {'visible':False}},
                                                  {'labels':['tcs','uor'],
                                                  'x':['Converted Revenue', 'Sampling Cost'],
                                                  'y':[convertedRev,-float(samplingCost)],
                                                  'type':'waterfall',
                                                  'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                                                  'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                                                  'connector': {'visible':False}},
                                                {'labels':['tcs','uor'],
                                                  'x':['Net Profit', 'Net Profit Not For Sampling'],
                                                  'y':[netProfit,-netProfitNFS],
                                                  'type':'waterfall',
                                                  'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                                                  'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                                                  'connector': {'visible':False}},
                                                {'labels':['tcs'],
                                                  'x':['Max Allowable Spend'],
                                                  'y':[MaxAllowSpend],
                                                  'type':'waterfall',
                                                  'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                                                  'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                                                  'connector': {'visible':False}}
                                                ],
                                    'layout': {'showlegend': False,
                                                'xaxis':{'automargin':True, 'title':'ROI Parameters'},
                                                'margin':dict(t = 0)
                                            }}
                                      )
                        ], style = {'width':'35%', 'display':'inline-block', 'float':'right'})
                    ])
                ])
        ]),
        dcc.Tab(label='Twitter Mining', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
    ])
])

counter_list = []

@app.callback(Output('counter_text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    url = "https://data-live.flightradar24.com/zones/fcgi/feed.js?faa=1\
           &mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&stats=1"
    # A fake header is necessary to access the site:
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = res.json()
    counter = 0
    for element in data["stats"]["total"]:
        counter += data["stats"]["total"][element]
    counter_list.append(counter)
    return 'Active flights worldwide: {}'.format(counter)

@app.callback(Output('live-update-graph','figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    fig = go.Figure(
        data = [go.Scatter(
        x = list(range(len(counter_list))),
        y = counter_list,
        mode='lines+markers'
        )])
    return fig

if __name__ == '__main__':
    app.run_server() 