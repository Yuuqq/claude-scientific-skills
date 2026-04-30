# Geospatial CSS: Spatial Statistics & Mapping

**Goal**: Analyze social phenomena (Inequality, Polarization, Voting) through the lens of **Space**.

## 1. Core Concepts
*   **Coordinate Reference System (CRS)**: The math mapping specific points on the 3D earth to a 2D plane.
    *   *Rule*: Always re-project to a "Projected CRS" (e.g., EPSG:3857 or Albers) before calculating Area or Distance.
    *   *Pitfall*: Calculating Euclidean distance on Lat/Lon (Degrees) is mathematically wrong.
*   **Spatial Autocorrelation**: "Everything is related to everything else, but near things are more related than distant things" (Tobler's First Law).
    *   *Metric*: Global Moran's I.

---

## 2. Python Pattern: Geopandas & PySAL

### A. Load & Visualize (Choropleth)

```python
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# 1. Load Data (Shapefile / GeoJSON)
gdf = gpd.read_file("data/raw/precincts.geojson")
gdf = gdf.to_crs(epsg=3857) # Project to Web Mercator

# 2. Plotting (The "Nature" Aesthetic)
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(column='vote_share', 
         cmap='Viridis', 
         legend=True,
         legend_kwds={'label': "Vote Share (%)", 'orientation': "horizontal"},
         ax=ax,
         alpha=0.9,
         edgecolor='white',
         linewidth=0.1)

# Add Basemap (optional context)
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
ax.set_axis_off() # Remove lat/lon box
plt.savefig("figures/vote_map_nature.png", dpi=300)
```

### B. Spatial Autocorrelation (Moran's I)

"Is the vote clustered or random?"

```python
from libpysal.weights import Queen
from esda.moran import Moran

# 1. Define Weights Matrix (Who is my neighbor?)
# Queen: Neighbors sharing a border or corner point
w = Queen.from_dataframe(gdf)
w.transform = 'r' # Row-standardize

# 2. Calculate Global Moran's I
y = gdf['vote_share'].values
moran = Moran(y, w)

print(f"Moran's I: {moran.I:.3f}")
print(f"P-value: {moran.p_norm:.4f}")
# Result: I > 0 means Clustering. I < 0 means Dispersion.
```

### C. Geographically Weighted Regression (GWR)

"Does the relationship between Income and Voting vary by Neighborhood?"

```python
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW

# Define variables
coords = list(zip(gdf.centroid.x, gdf.centroid.y))
X = gdf[['median_income']].values
y = gdf['vote_share'].values.reshape((-1,1))

# Select Bandwidth
bw = Sel_BW(coords, y, X).search()
model = GWR(coords, y, X, bw)
results = model.fit()

# Map the local coefficients
gdf['local_beta_income'] = results.params[:, 1]
gdf.plot(column='local_beta_income', cmap='RdBu', legend=True)
```

## 3. Data Sources (High Quality)
*   **GADM**: Global administrative boundaries.
*   **OSM (OpenStreetMap)**: Roads, buildings, amenities (via `osmnx`).
*   **US Census TIGER**: Strict standard for US boundaries.
