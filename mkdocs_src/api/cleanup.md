# Module `cleanup`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `clean_data_in_dir(data_in_dir: pathlib.Path) -> None`

Delete all .zip files and extracted shapefiles from data-in/.

Leaves the folder structure intact if empty folders remain.

### `clean_data_in_geojson_dir(data_in_geojson_dir: pathlib.Path) -> None`

Delete all files under data-in-geojson/.

Removes intermediate GeoJSON exports but leaves data-out/ untouched.

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

### `main() -> int`

CLI entry point for cleanup of all intermediate files.
