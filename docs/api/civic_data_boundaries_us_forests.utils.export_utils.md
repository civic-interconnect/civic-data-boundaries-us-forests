# Module `civic_data_boundaries_us_forests.utils.export_utils`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `export_split_geojson(shp_path: pathlib.Path, output_dir: pathlib.Path, split_by: str | None = None, simplify_tolerance: float = 0.01) -> None`

Export a shapefile to one or more GeoJSON files.

If split_by is provided, saves one file per unique attribute value.

Args:
    shp_path (Path): Path to the .shp file.
    output_dir (Path): Output folder.
    split_by (str, optional): Attribute to split on.
    simplify_tolerance (float, optional): Simplification tolerance in degrees.

### `load_layer(source: pathlib.Path, required_cols: list[str]) -> geopandas.geodataframe.GeoDataFrame`

Load a shapefile layer and validate required columns.

Args:
    source (Path): Path to .shp file.
    required_cols (list[str]): Required column names.

Returns:
    gpd.GeoDataFrame: Loaded GeoDataFrame.

### `remove_crs_field(geojson_path: pathlib.Path) -> None`

Remove the 'crs' property from a GeoJSON file, if present.

Args:
    geojson_path (Path): Path to the GeoJSON file.

### `should_skip_file(path: pathlib.Path) -> bool`

Determine whether this path should be skipped.

Skips directories and files with unexpected extensions.

### `validate_columns(gdf: geopandas.geodataframe.GeoDataFrame, columns: list[str], label: str) -> None`

Check if required columns exist in a GeoDataFrame.

Args:
    gdf (gpd.GeoDataFrame): GeoDataFrame to check.
    columns (list[str]): Required column names.
    label (str): Name to show in error messages.
