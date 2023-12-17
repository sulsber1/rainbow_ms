import rainbow as rb
import plotly as pt
import pandas as pd
import numpy as np
import plotly.express as px
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Create the CSVs of Raw Data
# datadir = rb.read("C:\\Users\\sulsb\\OneDrive\\Desktop\\github\\rainbow\\rainbow\\tests\\inputs\\blue.raw")
# for name in datadir.by_name:
#     csv_name = os.path.splitext(name)[0] + ".csv"
#     datadir.export_csv(name, csv_name)

# Make the plotly subplots
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))


df = pd.read_csv('_FUNC001.csv')

# Sum the row values (may have first column?)
df.loc[0:,'Row_Total'] = df.sum(numeric_only=True, axis=1)


# # TIC
# fig = px.line(x=TIC_df['RT (min)'].to_list(), y=TIC_df['Row_Total'].to_list())
# fig.show()


fig.add_trace(go.Line(x=df['RT (min)'].to_list(), y=df['Row_Total'].to_list()), row=1, col=1)





df.loc['Column_Total']= df.sum(numeric_only=True, axis=0)

# ugly but converts all the headers to floats, maybe pandas could do this?
headers = list(map(float, df.columns.to_list()[1:-1]))

# get the column total from the last row
column_total = df.loc['Column_Total']
# remove the RT and the Row_Total columns
short_list = column_total.to_list()[1:-1]

# Merge the datafarme back together
df1 = pd.DataFrame(headers, columns=['Mass'])
df2 = pd.DataFrame(short_list, columns=['MZ'])
df3 = pd.concat([df1, df2], axis=1)

# Filter for the data
df3 = df3[df3['MZ'] > 100000000]


# fig = px.bar(x=df3['Mass'], y=df3['MZ'], hover_name=df3['Mass'])
# # Set the range as the biggest and Smallest 
# fig.update_layout(
#     xaxis=dict(
#         range=[0, 1000],  # Set custom range
#     )
# )

# fig.update_xaxes(
#     showspikes=True,
#     spikecolor="red",
#     spikesnap="cursor",
#     spikemode="across",
#     spikedash="solid",
# )
# fig.show()

fig.add_trace(go.Bar(x=df3['Mass'], y=df3['MZ']), row=1, col=2)

# Speicifc mass - 587.0
# Get all the data from the specific column
mass_column = df.loc[:, '587.0'].to_list()[:-1]
# get all the retention times
retention_times = df.loc[:, 'RT (min)'].to_list()[:-1]

df1 = pd.DataFrame(retention_times, columns=['RT'])
df2 = pd.DataFrame(mass_column, columns=['MZ'])
df3 = pd.concat([df1, df2], axis=1)

# Filter for the retention time
# df3 = df3[df3['RT'] > 100000000]

# Filter for the data
df3 = df3[df3['MZ'] > 35000]

# There are some things to cut off the end of the df for now
fig.add_trace(go.Bar(x=df3['RT'], y=df3['MZ']), row=2, col=1)
# Set the range as the biggest and Smallest 
fig.update_layout(
    xaxis=dict(
        range=[0, retention_times[-2]],  # Set custom range
    )
)

fig.update_xaxes(
    showspikes=True,
    spikecolor="red",
    spikesnap="cursor",
    spikemode="across",
    spikedash="solid",
)



# User selects a time on the 


fig.show()