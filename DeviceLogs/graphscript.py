##**********************************************************************************************************
#   Title: Graph Script
#   Author: Samia Sami
#	Date: June 17, 2019
# 	Description: This program will will fetch one year data from the Postgres and store it in Pandas DataFrame. 
# 	             Using the Pandas DataFrame, it will then plot the graphs.
##**********************************************************************************************************
##Fetch the data and then plot the graphs
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2

conn = psycopg2.connect(database="postgres", user='postgres', password='teampower',port='5436')
cur = conn.cursor()
query = """
select * from public.meterdata order by "Local Time Stamp" DESC Limit 525600"""
# execute the query
cur.execute(query)
# retrieve an annual result set
data = cur.fetchall()

# close cursor and connection
cur.close()
conn.close()


#change the data from tuple to dataframes

df = pd.DataFrame(data, columns=['Local Time Stamp', 'Current Average','Voltage B-C', 'Voltage A-B', 'Voltage L-L', 'Active Power Total', 'Apparent Power Total','Reactive Power Total','Active Energy Delivered (KWh)','Active Energy Received (KWh)','Apparent Energy Delivered (KVAh)',
                   'Power Factor Total', 'Apparent Energy Received (KVAh)','Reactive Energy Delivered (KVARh)','Reactive Energy Received (KVARh)'])


app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='PM5560 Meter Data'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df['Local Time Stamp'] , 'y': df['Voltage B-C'], 'type': 'line', 'name': 'Voltage B-C'},
                {'x': df['Local Time Stamp'] , 'y': df['Voltage A-B'], 'type': 'line', 'name': 'Voltage A-B'},
                {'x': df['Local Time Stamp'], 'y': df['Voltage L-L'], 'type': 'line', 'name': 'Voltage L-L'},

            ],
            'layout': {
                'title': 'Voltage'
            }
        }
    ),

    

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': df['Local Time Stamp'], 'y': df["Current Average"], 'type': 'line', 'name': 'Current Average'},
               
            ],
            'layout': {
                'title': 'Current Average'
            }
        }
    ),

    dcc.Graph(
        id='example-graph-1',
        figure={
            'data': [
                {'x': df['Local Time Stamp'], 'y': df["Power Factor Total"], 'type': 'line', 'name': 'Power Factor Total'},
               
            ],
            'layout': {
                'title': 'Power Factor'
            }
        }
    ),

    dcc.Graph(
        id='example-graph-3',
        figure={
            'data': [
                {'x': df['Local Time Stamp'], 'y': df["Active Energy Delivered (KWh)"], 'type': 'line', 'name': 'Active Energy Delivered (KWh)'},
                {'x': df['Local Time Stamp'], 'y': df["Reactive Energy Delivered (KVARh)"], 'type': 'line', 'name': 'Reactive Energy Delivered (KVARh)'},
                {'x': df['Local Time Stamp'], 'y': df["Apparent Energy Delivered (KVAh)"], 'type': 'line', 'name': 'Apparent Energy Delivered (KVAh)'},
               
            ],
            'layout': {
                'title': 'Energy Delivered'
            }
        }
    ),

    dcc.Graph(
        id='example-graph-4',
        figure={
            'data': [
                {'x': df['Local Time Stamp'], 'y': df["Active Energy Received (KWh)"], 'type': 'line', 'name': 'Active Energy Received (KWh)'},
                {'x': df['Local Time Stamp'], 'y': df["Reactive Energy Received (KVARh)"], 'type': 'line', 'name': 'Reactive Energy Received (KVARh)'},
                {'x': df['Local Time Stamp'], 'y': df["Apparent Energy Received (KVAh)"], 'type': 'line', 'name': 'Apparent Energy Received (KVAh)'},
               
            ],
            'layout': {
                'title': 'Energy Received'
            }
        }
    ),

    dcc.Graph(
        id='example-graph-5',
        figure={
            'data': [
                {'x': df['Local Time Stamp'], 'y': df["Active Power Total"], 'type': 'line', 'name': 'Active Power Total'},
                {'x': df['Local Time Stamp'], 'y': df["Reactive Power Total"], 'type': 'line', 'name': 'Reactive Power Total'},
                {'x': df['Local Time Stamp'], 'y': df["Apparent Power Total"], 'type': 'line', 'name': 'Apparent Power Total'},
               
            ],
            'layout': {
                'title': 'Total Power'
            }
        }
    )

])

if __name__ == '__main__':
    app.run_server(debug=False, port=5093)
