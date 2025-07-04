# Module `civic_data_boundaries_us_forests.cli.cli`

## Functions

### `chunk_command()`

Chunk all data from data-in-geojson/ to data-out/.

### `cleanup_command()`

Cleanup temporary files and directories created during export.

Deletes all .zip files and extracted shapefiles from data-in/,
and all intermediate content in data-in-geojson/.
Keeps chunked GeoJSONs safe in data-out/.

### `export_command()`

Export all data into data-in-geojson/.

### `fetch_command()`

Download required shapefiles into data-in/.
Skips download if files already exist.

### `index_command()`

Generate index.json and other summary metadata files in data-out/.

### `main() -> int`

No description available.
