import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from decouple import config
import numpy as np

mapbox_token = config("MAPBOX_SECRET")
mapbox_style = config("MAPBOX_STYLE")

px.set_mapbox_access_token(mapbox_token)

color_scale = [
    "#fadc8f",
    "#f9d67a",
    "#f8d066",
    "#f8c952",
    "#f7c33d",
    "#f6bd29",
    "#f5b614",
    "#F4B000",
    "#eaa900",
    "#e0a200",
    "#dc9e00",
    "#FFA07A",
]


def scatter_mapbox(
    geo_data: pd.DataFrame = None, zoom: int = 10
) -> px.scatter_mapbox:
    """
     Plot real-estate transactions on map.
    Args:
        geo_data (pd.DataFrame): Pandas DataFrame.
        zoom(int): Zoom level.

    Returns:
        px.scatter_mapbox: Scatter plot of transaction data.
    """

    # Scaled the data exponentially to show smaller values.
    geo_data.loc[:, "scaled"] = (
        geo_data.loc[:, "transaction_price(unit_price_m^2)"] ** 0.9
    )

    fig = px.scatter_mapbox(
        geo_data,
        lat="latitude",
        lon="longitude",
        color="transaction_price(unit_price_m^2)",
        size="scaled",
        hover_name="area_name",
        hover_data=[
            "transaction_price(unit_price_m^2)",
            "area(m^2)",
            "area_name",
            "nearest_station_distance(minute)",
        ],
        color_continuous_scale=color_scale,
    )

    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # height=700,
        # width=700,
        coloraxis_showscale=False,
        mapbox_style=mapbox_style,
        mapbox=dict(
            center=dict(
                lat=geo_data["latitude"].mean(),
                lon=geo_data["longitude"].mean(),
            ),
            zoom=zoom,
        ),
    )

    fig.data[0].update(
        hovertemplate="%{customdata[2]} <br>Unit Price: %{customdata["
        "0]}<br>Area: %{customdata[1]}<br>Nearest Station: %{customdata[3]} Minutes"
    )
    return fig


def hexbin_with_animation(
    geo_data: pd.DataFrame = None, zoom: int = 10, num_hexagon: int = 15
) -> px.scatter_mapbox:
    """
     Plot real-estate transactions on map.
    Args:
        geo_data (pd.DataFrame): Pandas DataFrame.
        zoom(int): Zoom level.
        num_hexagon: Number of hexagons.

    Returns:
        px.scatter_mapbox: Hexbin with Animation plot.
    """
    fig = ff.create_hexbin_mapbox(
        data_frame=geo_data,
        lat="latitude",
        lon="longitude",
        nx_hexagon=num_hexagon,
        animation_frame=geo_data["transaction_period"],
        labels={"color": "Price per M^2", "frame": "Period"},
        color="transaction_price(unit_price_m^2)",
        agg_func=np.mean,
        color_continuous_scale="Icefire",
        opacity=0.9,
        min_count=1,
        show_original_data=True,
        original_data_marker=dict(opacity=0.5, size=4, color="deeppink"),
    )
    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=700,
        # width=700,
        coloraxis_showscale=True,
        mapbox_style=mapbox_style,
        mapbox=dict(
            center=dict(
                lat=geo_data["latitude"].mean(),
                lon=geo_data["longitude"].mean(),
            ),
            zoom=zoom,
        ),
    )
    fig.layout.sliders[0].pad.t = 20
    fig.layout.updatemenus[0].pad.t = 40
    return fig
