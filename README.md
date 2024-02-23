# Japan Real Estate Transaction Data Dashboard

## Development EVN setup

* Install poetry if you can don't have
```shell
curl -sSL https://install.python-poetry.org | python3 -
```
* Install dependencies.
```shell
poetry install
```
* Create a `.env` file and add MAPBOX style and token.

```shell
MAPBOX_SECRET=<Your MapBox Token>
MAPBOX_STYLE=mapbox://styles/mapbox/dark-v9
```

## Run Dashboard

```shell
poetry run streamlit run real_estate_transactions_japan/app.py
```

Dashboard live link: https://japan-real-estate-transactions.streamlit.app/
