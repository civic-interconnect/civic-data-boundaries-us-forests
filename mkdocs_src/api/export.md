# Module `export`

## Functions

### `export_forest_layer(layer: dict) -> None`

Export GeoJSONs from a single forest or district layer.

Depending on the config:
- may split by attribute (e.g. FORESTNAME)
- may simplify geometries

Outputs:
    GeoJSON files into:
        data-in-geojson/{layer.output_dir}/

Args:
    layer (dict): Layer configuration dictionary.

### `export_split_geojson(shp_path: pathlib.Path, output_dir: pathlib.Path, split_by: str | None = None, simplify_tolerance: float = 0.01) -> None`

Export a shapefile to one or more GeoJSON files.

If split_by is provided, saves one file per unique attribute value.

Args:
    shp_path (Path): Path to the .shp file.
    output_dir (Path): Output folder.
    split_by (str, optional): Attribute to split on.
    simplify_tolerance (float, optional): Simplification tolerance in degrees.

### `get_data_in_geojson_dir() -> pathlib.Path`

Return the root data-in-geojson directory for intermediate exported GeoJSONs
before chunking.

Returns:
    Path: data-in-geojson directory.

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

### `get_repo_root() -> pathlib.Path`

Return the root directory of the civic-data-boundaries-us-forests repository.

This function first checks whether the file path is running from
a cloned source repo (using __file__ as a reference), and if that
does not locate the repo, searches upward from the current working
directory until it finds a folder containing a data-config directory.

Returns:
    Path: Path to the repository root.

Raises:
    RuntimeError: If the repo root cannot be found.

### `load_all_layer_configs() -> list[dict]`

Loads and merges all YAML layer configs into a list of layers.

Returns:
    list[dict]: List of layer configuration dictionaries.

### `main() -> int`

CLI entry point to export forest-related layers to GeoJSON.

Returns:
    int: Exit code (0 if successful, 1 if failed).

### `should_skip_file(path: pathlib.Path) -> bool`

Determine whether this path should be skipped.

Skips directories and files with unexpected extensions.
