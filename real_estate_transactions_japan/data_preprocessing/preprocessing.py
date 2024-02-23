import numpy as np
import pandas as pd


class RealEstatePreprocessing:
    def __init__(self, transaction_data_path: str, japan_towns_data_path: str):
        """
        Initiate class object with raw transaction data path and Japan town
        (geo-location data).

        Args:
            transaction_data_path:  Raw real estate transaction data csv file
            path.
            japan_towns_data_path: Japan town's geo-location data csv file path.
        """
        self.transaction_data_path = transaction_data_path
        self.japan_towns_data_path = japan_towns_data_path

    def _load_data(self):
        """Load Data"""
        df = pd.read_csv(self.transaction_data_path, encoding="shift-jis")
        df2 = pd.read_csv(self.japan_towns_data_path)
        return df, df2

    @staticmethod
    def _area_column_preprocessing(area_name: str) -> str:
        if not area_name:
            return "nan"
        area_name = str(area_name)
        if area_name:
            if "(" in area_name:
                area_name = area_name.split("(")[0].lower()
            if area_name[-1].isnumeric():
                return "".join(area_name.split()[:-1]).lower()
            else:
                return area_name.replace(" ", "").replace("-", "").lower()

    def process_transactions(self):
        """Clean transaction data"""
        df, df2 = self._load_data()
        df2.rename(
            columns={
                "cityCode": "city_town_ward_village_code",
                "townAlphabet": "area_name",
            },
            inplace=True,
        )
        df2["area_name"] = df2["area_name"].apply(
            self._area_column_preprocessing
        )
        df2.drop_duplicates(
            subset=["city_town_ward_village_code", "area_name"], inplace=True
        )

        df.rename(columns=self._column_rename_dict(), inplace=True)
        del df["no"]

        df["region"].fillna("Unknown", inplace=True)

        df["area_name"].fillna("nan", inplace=True)

        df["area_name"] = df["area_name"].apply(
            lambda x: x.replace(" ", "").replace("-", "").lower()
        )
        cols = [
            "nearest_station_name",
            "nearest_station_distance(minute)",
            "layout",
            "land_shape",
            "frontage",
            "total_floor_area(m^2)",
            "year_of_construction",
            "building_structure",
            "use",
            "purpose_of_use",
            "frontage_road_direction",
            "frontage_road_classification",
            "frontage_road_breadth(m)",
            "city_planning",
            "maximus_building_coverage_ratio(%)",
            "maximus_floor_area_ratio(%)",
            "renovation",
            "transactional_factors",
        ]
        for col in cols:
            df[col].fillna("Unknown", inplace=True)

        df["transaction_period"] = df["transaction_period"].apply(
            lambda x: x[-4:] + "-" + x[0]
        )
        df["total_area"] = df["area(m^2)"].apply(
            lambda x: int(x.replace(" m^2 or greater.", "").replace(",", ""))
        )

        df.loc[
            df[df["transaction_price(unit_price_m^2)"].isnull()].index,
            "transaction_price(unit_price_m^2)",
        ] = (
            df[df["transaction_price(unit_price_m^2)"].isnull()][
                "transaction_price(total)"
            ]
            / df[df["transaction_price(unit_price_m^2)"].isnull()]["total_area"]
        )

        df["transaction_price(unit_price_m^2)"] = (
            df["transaction_price(unit_price_m^2)"].apply(np.ceil).astype(int)
        )
        df3 = pd.merge(
            df, df2, how="left", on=["city_town_ward_village_code", "area_name"]
        )
        df3 = df3[df3["latitude"].notnull()]
        df3.reset_index(inplace=True, drop=True)
        print(df3.shape, df.shape)

        return df3

    def _column_rename_dict(self):
        column_mapping = {
            "No": "no",
            "Type": "type",
            "Region": "region",
            "City,Town,Ward,Village code": "city_town_ward_village_code",
            "Prefecture": "prefecture",
            "City,Town,Ward,Village": "city_town_ward_village_name",
            "Area": "area_name",
            "Nearest station：Name": "nearest_station_name",
            "Nearest station：Distance(minute)": "nearest_station_distance(minute)",
            "Transaction-price(total)": "transaction_price(total)",
            "Layout": "layout",
            "Area(m^2)": "area(m^2)",
            "Transaction-price(Unit price m^2)": "transaction_price(unit_price_m^2)",
            "Land shape": "land_shape",
            "Frontage": "frontage",
            "Total floor area(m^2)": "total_floor_area(m^2)",
            "Year of construction": "year_of_construction",
            "Building structure": "building_structure",
            "Use": "use",
            "Purpose of Use": "purpose_of_use",
            "Frontage road：Direction": "frontage_road_direction",
            "Frontage road：Classification": "frontage_road_classification",
            "Frontage road：Breadth(m)": "frontage_road_breadth(m)",
            "City Planning": "city_planning",
            "Maximus Building Coverage Ratio(%)": "maximus_building_coverage_ratio(%)",
            "Maximus Floor-area Ratio(%)": "maximus_floor_area_ratio(%)",
            "Transaction period": "transaction_period",
            "Renovation": "renovation",
            "Transactional factors": "transactional_factors",
        }
        return column_mapping
