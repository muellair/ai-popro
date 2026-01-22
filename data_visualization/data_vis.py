import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import geopandas as gpd
import pathlib
import sys
import os
import numpy as np
import diagnosticPlots as d_plots
import statsmodels.formula.api as smf

# Check where you are
print("Current directory:", os.getcwd())
sys.path.append(os.getcwd())
from src.preprocess import load_destatis_csv as ldc

SHAPEFILE_PATH = 'data/shapefile_states_ger/NUTS250_N1.shp'
POPULATION_DATA_PATH = 'data/raw/population_raw.csv'
OUTPUT_PATH = 'data_visualization/output/'
PREPROCESSED_DATAPATH = 'data/preprocessed/joint_data_collection.csv'


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
# map_states_gdf = load_shapefile(SHAPEFILE_PATH)

# population_map_gdf = merge_map_population(map_states_gdf, population_df)

#vis_ger_map(SHAPEFILE_PATH)
#fig, ax = vis_ger_population_map(population_map_gdf)

def get_line_params(df):
    slope, intercept = np.polyfit(df['x_t-2'], df['x_t-1'], 1)
    return slope, intercept

def scatter_plot_population_over_years():
    
    preprocessed_df = pd.read_csv(PREPROCESSED_DATAPATH)
    df = preprocessed_df[['x_t-1', 'x_t-2', 'bundesland']].copy()
    print(df.head())


    # create scatter plots with regression lines for each Bundesland
    for land in df['bundesland'].unique():
        land_data = df[df['bundesland'] == land]
        slope, intercept = get_line_params(land_data)

        x_sorted = np.sort(land_data['x_t-2'])
        y_line = slope * x_sorted + intercept
        plt.xlabel('normalized population in year y')
        plt.ylabel('normalized population in year y-1')
        plt.title('Scattered Population from 1990 to 2024 in ' + land)
        plt.legend()
        plt.scatter(land_data['x_t-2'], land_data['x_t-1'], label=land)
        plt.plot(x_sorted, y_line, color='red', linestyle='-', linewidth=1.5, label='Regression Line')
        plt.savefig(OUTPUT_PATH + 'scatterplots/' + land + '_population_over_years.png', dpi=300)
        plt.clf()
    return population_df

# scatter = scatter_plot_population_over_years()



def plot_diagnostics():
    preprocessed_df = pd.read_csv(PREPROCESSED_DATAPATH)
    df = preprocessed_df[['x_t-1', 'x_t-2']].copy().rename(columns={'x_t-1': 'x_t1', 'x_t-2': 'x_t0'})
    
    results = smf.ols('x_t1 ~ x_t0', data=df).fit()
    diagnostics = d_plots.LinearRegDiagnostic(results)
    diagnostics(output_path=OUTPUT_PATH + "diagnostic_plots.png", high_leverage_threshold=True)
    # fig, ax = plt.subplots()
    #diagnostic_plots = d_plots.LinearRegDiagnostic(results)
    #diagnostic_plots.leverage_plot(df, OUTPUT_PATH + 'diagnostic_plots/leverage_plot.png')
    return results

diagnostics = plot_diagnostics()