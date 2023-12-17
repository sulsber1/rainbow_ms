# Time series data (assumed format)
dates = ["2023-10-01", "2023-10-07", "2023-10-14", "2023-10-21"]
temperature_station1 = [20, 23, 25, 22]
temperature_station2 = [18, 21, 20, 19]
precipitation_station1 = [5, 10, 2, 8]
precipitation_station2 = [3, 7, 1, 6]


import plotly.graph_objects as go

# Create subplots
fig = go.FigureWidget(layout=go.Layout(xaxis_title="Date", yaxis_title="Temperature (°C)"))

# Temperature subplot
fig.add_trace(
    go.Scatter(
        x=dates,
        y=temperature_station1,
        name="Station 1 (Temp)",
        opacity=0.7,
        hoverinfo="skip",
    )
)
fig.add_trace(
    go.Scatter(
        x=dates,
        y=temperature_station2,
        name="Station 2 (Temp)",
        opacity=0.7,
        hoverinfo="skip",
    )
)

# Invisible hover trace for temperature
fig.add_trace(
    go.Scatter(
        x=dates,
        y=[0 for _ in dates],  # Dummy y values for hover trigger
        name="(Hover for Temp)",
        showlegend=False,
        hovertemplate="Date: %{x}<br>Station 1: %{y1}°C<br>Station 2: %{y2}°C",
        mode="markers",
    )
)

# Precipitation subplot (shared x-axis)
fig.update_layout(yaxis2_title="Precipitation (mm)")
fig.add_trace(
    go.Scatter(
        x=dates,
        y=precipitation_station1,
        name="Station 1 (Precip)",
        xaxis="x2",
        yaxis="y2",
        opacity=0.7,
        hoverinfo="skip",
    )
)
fig.add_trace(
    go.Scatter(
        x=dates,
        y=precipitation_station2,
        name="Station 2 (Precip)",
        xaxis="x2",
        yaxis="y2",
        opacity=0.7,
        hoverinfo="skip",
    )
)

# Invisible hover trace for precipitation
fig.add_trace(
    go.Scatter(
        x=dates,
        y=[0 for _ in dates],  # Dummy y values for hover trigger
        xaxis="x2",
        yaxis="y2",
        name="(Hover for Precip)",
        showlegend=False,
        hovertemplate="Date: %{x}<br>Station 1: %{y1}mm<br>Station 2: %{y2}mm",
        mode="markers",
    )
)

# Configure shared x-axis range
fig.update_layout(xaxis_range=[min(dates), max(dates)])

# Adjust marker size and opacity for visual appeal
fig.update_traces(marker_size=10, marker_opacity=1)

# Display the plot
fig.show()
