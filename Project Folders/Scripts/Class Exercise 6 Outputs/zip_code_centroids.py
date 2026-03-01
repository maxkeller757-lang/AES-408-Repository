"""Create a shapefile of ZIP code centroid points from the
2025 Gazeteer file downloaded from the Census.

This script reads the pipe-delimited text file, constructs Shapely
Point objects for each centroid, and writes a shapefile containing the
ZIP code (as a string to preserve leading zeros) and the geometry.

Usage
-----
python zip_code_centroids.py

Adjust the ``GAZETTEER_FILE`` constant below if the file is located
somewhere else or has a different name.  The output shapefile will be
written to the current working directory by default.
"""

import pathlib
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# path to the unzipped gazetteer text file; change if necessary
GAZETTEER_FILE = pathlib.Path(r"C:\Users\maxke\Downloads\2025_Gaz\2025_Gaz_zcta_national.txt")

# output shapefile base name (".shp" and associated files will be created)
OUTPUT_SHP = "zip_code_centroids.shp"


def main():
    # read with pandas; the file uses "|" as the delimiter
    # read everything as string initially so leading zeros are preserved
    df = pd.read_csv(GAZETTEER_FILE, delimiter="|", dtype=str)

    # the ZIP code (ZCTA) is in the GEOID column; keep as string
    df["ZIP"] = df["GEOID"].astype(str)

    # latitude/longitude columns exist as strings; convert to float
    # INTPTLAT is latitude, INTPTLONG is longitude
    df["INTPTLAT"] = pd.to_numeric(df["INTPTLAT"], errors="coerce")
    df["INTPTLONG"] = pd.to_numeric(df["INTPTLONG"], errors="coerce")

    # drop rows with invalid coordinates (if any)
    df = df.dropna(subset=["INTPTLAT", "INTPTLONG"])

    # construct Shapely Point geometries (lon, lat order)
    geometry = [Point(xy) for xy in zip(df["INTPTLONG"], df["INTPTLAT"])]

    # create a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # keep only ZIP and geometry in output
    gdf = gdf[["ZIP", "geometry"]]

    # write to a shapefile
    print(f"Writing {len(gdf)} centroids to {OUTPUT_SHP}...")
    gdf.to_file(OUTPUT_SHP)
    print("Done.")

    # read the shapefile back in and display it using GeoPandas
    print("Loading shapefile for display...")
    gdf2 = gpd.read_file(OUTPUT_SHP)
    gdf2.plot(marker='o', color='red', markersize=2)
    print("Display complete. Close the plot window to continue.")


if __name__ == "__main__":
    main()
