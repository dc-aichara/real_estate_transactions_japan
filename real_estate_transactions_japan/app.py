import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from maps import scatter_mapbox, hexbin_with_animation

st.set_page_config(layout="wide")
st.write(
    """
    <div style="text-align:center">
        <h1>Japan Real Estate Transactions</h1>
    </div>
    """,
    unsafe_allow_html=True,
)


def load_data(prefecture: str = "Tokyo"):
    global df
    df = pd.read_csv(f"data/{prefecture.lower()}_transactions.csv.gz")


with st.sidebar:
    prefecture_name = st.selectbox(
        "Which prefecture data would you like to see!",
        ["Tokyo", "Osaka", "Kyoto", "Hokkaido", "Saitama"]
    )
    load_data(prefecture_name)
    quarters = np.sort(df["transaction_period"].unique())
    quarter = st.selectbox("Which Quarter would you like to see!", quarters)
    purpose_of_use = st.selectbox(
        "Select purpose of land use",
        ["All"] + list(np.sort(df["purpose_of_use"].unique())),
    )
    city = st.selectbox(
        "Which city would you like to see!",
        ["All"] + list(np.sort(df["city_town_ward_village_name"].unique())),
    )
fig_animation = hexbin_with_animation(df, zoom=9, num_hexagon=20)
st.plotly_chart(fig_animation, use_container_width=True)


scatter_map_zoom = 10
quarter_data = df[df.loc[:, "transaction_period"] == quarter]
if (
    purpose_of_use != "All"
    and purpose_of_use in quarter_data["purpose_of_use"].unique()
):
    quarter_data = quarter_data[
        quarter_data["purpose_of_use"] == purpose_of_use
    ]
if (
    city != "All"
    and city in quarter_data["city_town_ward_village_name"].unique()
):
    quarter_data = quarter_data[
        quarter_data["city_town_ward_village_name"] == city
    ]
    scatter_map_zoom = 12

st.markdown(
    f"### <div style='text-align:center'> Prefecture: <span style='color:blue'> {prefecture_name} </span> "
    f"Quarter: <span style='color:blue'>{quarter} </span> "
    f"Purpose of Use: <span style='color:blue'>{purpose_of_use} </span> "
    f"City: <span style='color:blue'> {city} </span> </div>",
    unsafe_allow_html=True,
)

fig = scatter_mapbox(quarter_data, zoom=scatter_map_zoom)
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig2 = px.bar(
        quarter_data.groupby(["layout"], as_index=False)[
            "transaction_price(" "unit_price_m^2)"
        ]
        .mean()
        .sort_values(["transaction_price(unit_price_m^2)"], ascending=False),
        x="layout",
        y="transaction_price(unit_price_m^2)",
        color="layout",
        title="Purpose of Use Vs Unit Price per Meter Square",
    )
    fig2.update_layout(
        xaxis={"type": "category"},
        title_x=0.1,
        title_y=0.95,
        title_font=dict(size=20),
    )

    st.plotly_chart(fig2, use_container_width=True)

with col2:
    df8 = df.groupby(["transaction_period", "purpose_of_use"], as_index=False)[
        "transaction_price(unit_price_m^2)"
    ].mean()

    df8 = df8[~df8["purpose_of_use"].isin(["Unknown", "Other"])]

    fig3 = px.line(
        df8,
        x="transaction_period",
        y="transaction_price(unit_price_m^2)",
        color="purpose_of_use",
        title="Purpose of Use Vs Unit Price per Meter Square",
    )
    fig3.update_layout(
        xaxis={"type": "category"},
        title_x=0.10,
        title_y=0.95,
        title_font=dict(size=20),
    )

    st.plotly_chart(fig3, use_container_width=True)
