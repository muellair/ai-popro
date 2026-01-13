import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import geopandas as gpd
import pathlib
import sys
import os
# Check where you are
print("Current directory:", os.getcwd())
sys.path.append(os.getcwd())
from src.preprocess import load_destatis_csv as ldc

SHAPEFILE_PATH = 'data/shapefile_states_ger/NUTS250_N1.shp'
POPULATION_DATA_PATH = 'data/raw/population_raw.csv'
OUTPUT_PATH = 'data_visualization/output/'

def load_shapefile(SHAPEFILE_PATH):
    # load Germany's shapefile on Bundesland-level with geopandas
    map_ger_gdf = gpd.read_file(SHAPEFILE_PATH)
    
    map_states_gdf = map_ger_gdf[map_ger_gdf["NUTS_LEVEL"] == 1].copy()
    map_states_gdf["bundesland"] = map_states_gdf["NUTS_NAME"].str.strip()
    map_states_gdf = map_states_gdf.dissolve(by="bundesland", as_index=False)
    return map_states_gdf


def load_population_csv(POPULATION_DATA_PATH) -> pd.DataFrame:
    # load the preprocessed population data using preprocess module
    population_df = ldc(pathlib.Path(POPULATION_DATA_PATH))
    return population_df


def merge_map_population(map_states_gdf, population_df):
    print('passing here')
    # Merge map GeoDataFrame with population DataFrame for a specific year
    population_map_gdf = map_states_gdf.merge(population_df, left_on='bundesland', right_on='bundesland', how='left' )
    population_map_gdf = population_map_gdf.drop(columns=['bundesland', 'NUTS_CODE', 'NUTS_LEVEL', 'BEGINN', 'OBJID', 'GF'])
    return population_map_gdf


def vis_ger_map(shapefile_path):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    map_ger_gdf = load_shapefile(shapefile_path)
    map_ger_gdf.plot(column="bundesland", categorical=True,edgecolor="black",linewidth=0.8,
                 ax=ax, legend=True)
    # ax.axis("off")
    # plt.tight_layout()

    plt.savefig(OUTPUT_PATH + "germany_states.png", dpi=300)
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

    plt.savefig(OUTPUT_PATH + "germany_population_map.png", dpi=300)
    return fig, ax



population_df = load_population_csv(POPULATION_DATA_PATH)
map_states_gdf = load_shapefile(SHAPEFILE_PATH)
vis_ger_map(SHAPEFILE_PATH)

population_map_gdf = merge_map_population(map_states_gdf, population_df)
fig, ax = vis_ger_population_map(population_map_gdf)
