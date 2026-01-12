import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import geopandas as gpd
import pathlib
import sys
import os
# Check where you are
print("Current directory:", os.getcwd())
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.preprocess import load_destatis_csv as ldc

shapefile_path = 'data_visualization/shapefile_states_ger/NUTS250_N1.shp'
population_data_path = 'data/raw/population_raw.csv'

def load_shapefile(shapefile_path):
    # load shapefile using geopandas
    map_ger_gdf = gpd.read_file(shapefile_path)
    return map_ger_gdf


def load_population_csv(population_data_path) -> pd.DataFrame:
    # load the preprocessed population data using preprocess module
    population_df = ldc(pathlib.Path(population_data_path))
    # switch columns and rows to get year as index
    #population_df = population_df.set_index("bundesland").T    # transpose rows ↔ columns
    #population_df.index = population_df.index.astype(int)
    #population_df.index.name = "year"
    return population_df


def merge_map_population(map_ger_gdf, population_df):
    # Merge map GeoDataFrame with population DataFrame for a specific year
    states = map_ger_gdf[map_ger_gdf["NUTS_LEVEL"] == 1].copy()
    states["bundesland"] = states["NUTS_NAME"].str.strip()

    states = states.dissolve(by="bundesland", as_index=False)
    population_map_gdf = states.merge(population_df, left_on='bundesland', right_on='bundesland', how='left' )
    population_map_gdf = population_map_gdf.drop(columns=['bundesland', 'NUTS_CODE', 'NUTS_LEVEL', 'BEGINN', 'OBJID', 'GF'])
    return population_map_gdf


def vis_ger_map(shapefile_path):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    map_ger_gdf = load_shapefile(shapefile_path)
    map_ger_gdf.plot(column="bundesland", categorical=True,edgecolor="black",linewidth=0.8,
                 ax=ax, legend=True)
    # ax.axis("off")
    # plt.tight_layout()

    plt.savefig("germany_states.png", dpi=300)
    return fig, ax


def vis_ger_population_map(population_map_gdf):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    #visualize population for year 1999
    population_map_gdf.plot(column=1999, cmap='YlOrRd', legend=True)
    # population_map_gdf.plot(column=['bundesland'] , cmap='OrRd', edgecolor="black", linewidth=0.8,
    #                 ax=ax, legend=True)
    # ax.set_title("Population Distribution in Germany by State")
    # ax.axis("off")
    # plt.tight_layout()

    plt.savefig("germany_population_map.png", dpi=300)
    return fig, ax



population_df = load_population_csv(population_data_path)
map_ger_gdf = load_shapefile(shapefile_path)
# ger_map = vis_ger_map(shapefile_path)

population_map_gdf = merge_map_population(map_ger_gdf, population_df)
# fig, ax = vis_ger_population_map(population_map_gdf)
