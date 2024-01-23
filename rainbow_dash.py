from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.graph_objects import Figure
import rainbow as rb
import os
##### GLOBAL VARIABLES ######

df = None
## TIC ##

## MASS SPECTRA ##

MS_LOW_X_RANGE = 0
MS_HIGH_X_RANGE = 1000

## EIC ##


"""
Create the CSVs of Raw Data
This is will need to be adjusted, I just so happened to grab an MS file
per https://rainbow-api.readthedocs.io/en/latest/tutorial.html you can grab turn the files into
objects and see which detected, but there's no easy way to tell.

"""
def create_CSV_of_MS(run=False):
    if run:
        # point towards the raw folder
        # https://github.com/evanyeyeye/rainbow
        #datadir = rb.read("C:\\Users\\sulsb\\OneDrive\\Desktop\\github\\rainbow\\rainbow\\tests\\inputs\\blue.raw")
        for name in datadir.by_name:
            csv_name = os.path.splitext(name)[0] + ".csv"
            datadir.export_csv(name, csv_name)
#datadir = rb.read("C:\\Users\\sulsb\\OneDrive\\Desktop\\github\\rainbow\\rainbow\\tests\\inputs\\blue.raw")

datadir = rb.read("/Users/dannysulsberger/Desktop/github/rainbow/tests/inputs/blue.raw")
for name in datadir.by_name:
    csv_name = os.path.splitext(name)[0] + ".csv"
    datadir.export_csv(name, csv_name)

    """
        Create Global DF

        Example of what's red
        "RT Min", 160.0, 161, ...
        1.01, 0, 1000, ...
        1.02, 500, 250, ...

    """
    df = pd.read_csv('_FUNC001.csv')


# Create some graphs for the initial site 
mt_fig = Figure()
mt_fig.update_layout(xaxis=dict(rangemode="tozero"))
mt_fig.update_layout(title=f"Mass @ ")
mt_fig.update_layout(xaxis=dict(title="Time (sec)"), yaxis=dict(title="Intensity"))
mt_fig.update_layout(hovermode="x unified")

# Make the plotly subplots for the TIC
# This could maybe just be a go plot? but it works now.
fig = make_subplots(
    rows=1, cols=1,
    subplot_titles=("TIC",))


fig = Figure()
""" 
    Graph: TIC Workflow
    x = Time, y = Total_Mass
    Show = The sum of the all the masses over the entire run (time)
    for each time point, sum all masses and plot that point

"""

# Sum the row values skipping the first column (retionion times)
# Appends "Row_total" column + value to each row
df.loc[0:,'Row_Total'] = df.sum(numeric_only=True, axis=1)


# Need to add traces for subplots (multiple plots)
# Huge hack -> https://community.plotly.com/t/why-are-lasso-and-boxselect-tools-not-shown/71795/3
# If they arent hidden the graph looks horrible
fig.add_trace(
    go.Scatter(
        x=df['RT (min)'].to_list(), y=df['Row_Total'].to_list()
        , mode='lines+markers', line_color='crimson', marker_color='rgba(0,0,0,0)',
        ))

fig.update_layout(xaxis=dict(title="Time (sec)"), yaxis=dict(title="Intensity"))
fig.update_traces(xaxis='x1')
fig.update_layout(hovermode="x unified")


"""  
    ~~~ NOT USED ~~
    Aggregate all the masses for the entire
    x = Specific_mass , y = Total_M/Z, show = Masses detected for entire chromatogram
    


#df.loc['Column_Total']= df.sum(numeric_only=True, axis=0)

# ugly but converts all the headers to floats, maybe pandas could do this?
#headers = list(map(float, df.columns.to_list()[1:-1]))

# get the column total from the last row
#column_total = df.loc['Column_Total']
# remove the RT and the Row_Total columns
#short_list = column_total.to_list()[1:-1]

# Merge the datafarme back together
# df1 = pd.DataFrame(headers, columns=['Mass'])
# df2 = pd.DataFrame(short_list, columns=['MZ'])
# df3 = pd.concat([df1, df2], axis=1)

# Filter for the data
# df3 = df3[df3['MZ'] > 100000000]

# # get all the retention times
# retention_times = df.loc[:, 'RT (min)'].to_list()[:-1]

# df1 = pd.DataFrame(retention_times, columns=['RT'])

# df3 = pd.concat([df1, df2], axis=1)

# # Filter for the data
# df3 = df3[df3['MZ'] > 15000]

"""


""" 
    Graph: EIC Workflow
    x = M/Z (s), y = Rel M/Z
    Show = The sum of the all the masses over the entire run (time)
    for each time point, sum all masses and plot that point

"""

def create_EIC_graph(EIC_mass):
    if EIC_mass:
        EIC_mass = str(EIC_mass)
        filtered_df = df[['RT (min)', EIC_mass]]
        fig = Figure()
        fig.add_trace(go.Scatter(x=filtered_df['RT (min)'], y=filtered_df[EIC_mass]),)
        fig.update_layout(xaxis=dict(rangemode="tozero"))
        fig.update_layout(title=f"Mass @{EIC_mass}")
        fig.update_layout(xaxis=dict(title="Time (sec)"), yaxis=dict(title="Intensity"))
        fig.update_layout(hovermode="x unified")
        return fig
    fig = Figure()
    fig.update_layout(xaxis=dict(rangemode="tozero"))
    fig.update_layout(title=f"Mass = {EIC_mass}")
    fig.update_layout(xaxis=dict(title="Time (sec)"), yaxis=dict(title="Intensity"))
    fig.update_layout(hovermode="x unified")
    return fig



"""
    Graph: MASS SPECTRA
    Given a specific time range, aggregate every specific mass and display -> taken from the callback
"""

def create_mass_spec_graph(time_0, time_1, fig):

    # This pass for the default (no time specified) Graph
    df3 = df[df['RT (min)'].between(MS_LOW_X_RANGE,MS_HIGH_X_RANGE)]

    if time_0 and time_1:
        df3 = df[df['RT (min)'].between(time_0,time_1)]
    
    df3 = df3.copy(deep=True)
    df3.loc['Column_Total']= df3.sum(numeric_only=True, axis=0)
    del df3['RT (min)']
    del df3['Row_Total']

    # Normalize the values, largest = 100 Smallest = 1
    column_total = df3.loc['Column_Total']
    column_total = 100 * (column_total - column_total.min()) / (column_total.max() - column_total.min())

    # Overwrite df with normalized data
    df3.loc['Column_Total'] = column_total

    ## !!!! Filter the normailzed data to show relative amounts greater than X
    filtered_norm_rel_mass = column_total[column_total >= 25]

    # Convert back to df -> probably an easier way
    mass_df = pd.Series.to_frame(filtered_norm_rel_mass, name="Mass")
    
    #grab the filtered indices + cnovert to list -> convert values to floats
    indices = mass_df.index.values.tolist()
    indices = list(map(float, indices))
    

    #grab the filtered Masses + cnovert to list -> convert values to floats
    mass_col = mass_df['Mass'].to_list()
    mass_col = list(map(float, mass_col))
    
    # Hacky way to make the graph go from low to high
    indices.append(MS_HIGH_X_RANGE)
    mass_col.append(MS_LOW_X_RANGE)

    fig = Figure()
    fig.add_trace(go.Bar(x=indices, y=mass_col, width=3))
    if time_0 and time_1:
        fig.update_layout(title=f"Mass from {round(time_0, 2)}s to {round(time_1, 2)}s")
    fig.update_layout(xaxis=dict(title="M/Z"), yaxis=dict(title="Rel  M/Z"))

    # Force the x axis to display to 0, if not it will show min-max as the range
    fig.update_layout(xaxis=dict(rangemode="tozero"))
    fig.update_layout(xaxis=dict(dtick=50))
    fig.update_layout(hovermode="x")
    
    fig.add_annotation(
        x=mass_df['Mass'].idxmax(),
        y=100,
        xref="x",
        yref="y",
        text=f"{mass_df['Mass'].idxmax()}",
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
        )
   
    
    return fig

def make_MT(callback=False):
    fig = Figure()
    fig.add_trace(
    go.Scatter(
        x=df['RT (min)'].to_list(), y=df['Row_Total'].to_list()
        , mode='lines+markers', line_color='crimson', marker_color='rgba(0,0,0,0)',
        ))

    fig.update_layout(xaxis=dict(title="Time (sec)"), yaxis=dict(title="Intensity"))
    fig.update_traces(xaxis='x1')
    fig.update_layout(hovermode="x unified")
    if callback:
            all_x = [x['x'] for x in callback['points']]
            all_y = [x['y'] for x in callback['points']]
            fig.add_trace(go.Scatter(x=all_x, y=all_y, fill='toself', fillcolor='red', name='Selected Area'))
    # fig = Figure()
    # fig.add_trace(go.Scatter(
    #             x=df['RT (min)'].to_list(), y=df['Row_Total'].to_list(), width=3
    #     , mode='lines+markers', line_color='crimson', marker_color='rgba(0,0,0,0)',
    # ))
    # fig.update_layout(xaxis=dict(title="Time (sec)"), yaxis=dict(title="Intensity"))
    # fig.update_traces(xaxis='x1')
    # fig.update_layout(hovermode="x unified")
    return fig

def add_trace():

    return fig



@callback(
    [Output('mass-spectrum', 'figure'), 
     Output('basic-interactions', 'figure')],
    Input('basic-interactions', 'selectedData'))
def update_MASS_SPECTRA(selectedData):
    # Not super - to show the 'integrated aka filled' peak, we have to make a trace and put it over the graph
    # This causes the callback to get an update for the graph THEN from the trace.  The trace will contain
    # no x/y coord in the selectedData var and will always be sent to the callback second thus I need to return
    # the existing graph as a global.  Probably need to look into this, but it's stable at the moment.
    global current_graph
    if selectedData:
        print(selectedData)
        if 'range' in selectedData:
            # print('hits it')
            # print(selectedData)
            x1_coord = selectedData['range']['x'][0]
            x2_coord = selectedData['range']['x'][-1]
            current_graph = create_mass_spec_graph(x1_coord, x2_coord, fig), make_MT(selectedData)
            return current_graph
        return current_graph
    return create_mass_spec_graph(None, None, fig), make_MT()

@callback(
    Output('EIC-mass', 'figure', allow_duplicate=True),
    [Input('mass-spectrum', 'clickData'),
     Input('EIC-mass-dropdown', 'value')], prevent_initial_call=True)
def update_EIC(EIC_mass_obj, obj2):
    if EIC_mass_obj:
        EIC_mass_obj = float(EIC_mass_obj['points'][0]['x'])
    if obj2:
        return create_EIC_graph(obj2)
    return create_EIC_graph(EIC_mass_obj)
    

"""
    Plotly style info - heavily borrowing from tutorial -> https://dash.plotly.com/interactive-graphing

"""

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# https://plotly.com/python/configuration-options/
app = Dash(prevent_initial_callbacks="initial_duplicate")
app.layout = html.Div([

        html.Div([
        dcc.Dropdown(df.columns.values,id='EIC-mass-dropdown',
        )
    ], style={'display' : 'grid', 'grid-template-columns': '1fr 1fr', 
              'grid-column-start' : 'col-start 2'}),
    
    html.Div([
            dcc.Graph(
        id='basic-interactions', config = {'displayModeBar': True}
            
        )
        ,

        dcc.Graph(id='mass-spectrum', config = {'displayModeBar': False}),
    ], style={'display' : 'grid', 'grid-template-columns': '1fr 1fr'}),

    html.Div([
        dcc.Graph(id='EIC-mass', figure=mt_fig, config = {'displayModeBar': False}),
    ], style={'display' : 'grid', 'grid-template-columns': '1fr 1fr'}),

],
)

if __name__ == '__main__':
    create_CSV_of_MS(False)
    if df.empty:
        df = pd.read_csv('_FUNC001.csv')
    app.run_server(debug=True, use_reloader=True, port=8052) 