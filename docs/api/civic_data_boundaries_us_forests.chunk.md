# Module `civic_data_boundaries_us_forests.chunk`

## Functions

### `chunk_geojson_folder(input_folder: pathlib.Path, max_features: int, output_folder: pathlib.Path) -> None`

Chunk all eligible GeoJSON files in a folder.

Args:
    input_folder (Path): Folder containing GeoJSON files.
    max_features (int): Maximum features per chunk.
    output_folder (Path): Destination folder for chunked files.

### `chunk_layers() -> None`

Chunk all exported GeoJSONs from data-in-geojson, based on YAML configs.

Writes all final chunked (or copied) GeoJSONs into data-out/.

### `chunk_or_copy_file(geojson_file: pathlib.Path, max_features: int, output_dir: pathlib.Path) -> None`

Decide whether to chunk a GeoJSON file or simply copy it.

Args:
    geojson_file (Path): The file to process.
    max_features (int): Threshold for chunking.
    output_dir (Path): Destination folder.

### `export_forest_layer(layer: dict) -> None`

Export GeoJSONs from a single forest or district layer.

Reads shapefiles from data-in/ and writes either single
or split GeoJSONs into data-out/.

Args:
    layer (dict): Configuration dictionary for the layer.

### `export_split_geojson(shp_path: pathlib.Path, output_dir: pathlib.Path, split_by: str | None = None, simplify_tolerance: float = 0.01) -> None`

Export a shapefile to one or more GeoJSON files.

If split_by is provided, saves one file per unique attribute value.

Args:
    shp_path (Path): Path to the .shp file.
    output_dir (Path): Output folder.
    split_by (str, optional): Attribute to split on.
    simplify_tolerance (float, optional): Simplification tolerance in degrees.

### `get_chunking_params() -> dict`

Load chunking and simplification parameters from YAML layer configs.

Returns:
    dict: Dictionary with chunking parameters.

### `get_data_out_dir() -> pathlib.Path`

Return the root data-out directory for the final committed GeoJSONs
(chunked and ready for deployment).

Returns:
    Path: data-out directory.

### `get_layer_in_dir(layer_output_dir: str) -> pathlib.Path`

Return the input folder for a specific layer's shapefiles.

Args:
    layer_output_dir (str): Subdirectory under data-in/ where this layer's
        downloaded and extracted shapefiles live.

Returns:
    Path: Full path to that layer's folder under data-in/.

### `get_layer_in_geojson_dir(layer_output_dir: str) -> pathlib.Path`

Return the intermediate GeoJSON folder for a specific layer.

Args:
    layer_output_dir (str): Subdirectory under data-in-geojson/ where this layer's
        exported (but not yet chunked) GeoJSONs are stored.

Returns:
    Path: Full path to that layer's folder under data-in-geojson/.

### `get_layer_out_dir(layer_output_dir: str) -> pathlib.Path`

Return the output folder for a specific layer's final chunked GeoJSONs.

Args:
    layer_output_dir (str): Subdirectory under data-out/ for this layer.

Returns:
    Path: Full path to that layer's folder under data-out/.

### `load_all_layer_configs() -> list[dict]`

Load and merge all YAML layer configs into a single list.

Returns:
    list[dict]: List of all configured layers.

### `main() -> int`

CLI entry point for chunking all GeoJSON files as needed.
