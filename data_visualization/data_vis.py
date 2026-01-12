import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import csv
import pathlib

shapefile_path = '/workspace/data_visualization/shapefile_states_ger/NUTS250_N1.shp'
# !!!Change path to processed data
population_data_path = '/workspace/data/raw/population_states_ger_data.csv'
matplotlib.use('Agg')


def load_shapefile(shapefile_path):
    map_ger = gpd.read_file(shapefile_path)
    return map_ger


def load_destatis_csv(population_data_path) -> pd.DataFrame:
    population_df = pd.read_csv(population_data_path, delimiter=';', encoding='latin1')
    return population_df


def viasualize_map(map_ger):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    map_ger.plot(column="NUTS_NAME", categorical=True,edgecolor="black",linewidth=0.8,
                 ax=ax, legend=True)
    ax.axis("off")
    plt.tight_layout()

    plt.savefig("germany_states.png", dpi=300)
    
    return fig, ax
# Example usage
map_ger = load_shapefile(shapefile_path)
#population_df = load_destatis_csv(population_data_path)
fig, ax = viasualize_map(map_ger)