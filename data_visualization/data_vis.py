import shapefile
import matplotlib.pyplot as plt
import pandas as pd

shapefile_path = '/workspace/data_visualization/shapefile_states_ger/NUTS250_N1.shp'
data_path = '/workspace/data/raw/population_states_ger_data.csv'

def import_data(shapefile_path, data_path):
    shapefile_states = shapefile.Reader(shapefile_path)
    shapes = shapefile_states.shapes()
    points = [shape.points for shape in shapes]

    data = pd.read_csv(data_path, sep=';', encoding='utf-8', skiprows=5)

    return points, shapes, data


points, shapes, data = import_data(shapefile_path, data_path)
print(data.head())