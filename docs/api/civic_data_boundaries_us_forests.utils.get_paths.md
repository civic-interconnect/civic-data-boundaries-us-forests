# Module `civic_data_boundaries_us_forests.utils.get_paths`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `get_data_in_dir() -> pathlib.Path`

Return the root data-in directory for raw downloads
(zip files and extracted shapefiles).

Returns:
    Path: data-in directory.

### `get_data_in_geojson_dir() -> pathlib.Path`

Return the root data-in-geojson directory for intermediate exported GeoJSONs
before chunking.

Returns:
    Path: data-in-geojson directory.

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
