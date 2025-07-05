# Module `utils.chunk_utils`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `chunk_geojson_file(geojson_file: pathlib.Path, output_dir: pathlib.Path, max_features: int) -> None`

Chunk a single GeoJSON file into smaller pieces in the output_dir.

Skips the file if it's a directory or already chunked.

### `chunk_geojson_folder(input_folder: pathlib.Path, max_features: int, output_folder: pathlib.Path) -> None`

Chunk all eligible GeoJSON files in a folder.

Args:
    input_folder (Path): Folder containing GeoJSON files.
    max_features (int): Maximum features per chunk.
    output_folder (Path): Destination folder for chunked files.

### `chunk_one(path: pathlib.Path, max_features: int, output_dir: pathlib.Path)`

Chunk a single GeoJSON file and write the output files.

Args:
    path (Path): Path to input GeoJSON file.
    max_features (int): Max features per chunk.
    output_dir (Path): Output folder to store chunks.

### `chunk_or_copy_file(geojson_file: pathlib.Path, max_features: int, output_dir: pathlib.Path) -> None`

Decide whether to chunk a GeoJSON file or simply copy it.

Args:
    geojson_file (Path): The file to process.
    max_features (int): Threshold for chunking.
    output_dir (Path): Destination folder.

### `copy_geojson_file(src: pathlib.Path, dest: pathlib.Path) -> None`

Copy a GeoJSON file from src to dest.

### `geojson_feature_count(path: pathlib.Path) -> int`

Return the number of features in a GeoJSON file.

Args:
    path (Path): Path to the GeoJSON file.

Returns:
    int: Feature count or 0 if reading fails.

### `get_chunking_params() -> dict`

Load chunking and simplification parameters from YAML layer configs.

Returns:
    dict: Dictionary with chunking parameters.

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

### `is_chunked_file(path: pathlib.Path) -> bool`

Return True if the file is already a chunked GeoJSON.

Args:
    path (Path): Path to the file.

Returns:
    bool: True if the file ends with '_chunked.geojson'.

### `load_all_layer_configs() -> list[dict]`

Load and merge all YAML layer configs into a single list.

Returns:
    list[dict]: List of all configured layers.

### `should_skip_file(path: pathlib.Path) -> bool`

Determine whether a file should be skipped during chunking.

Args:
    path (Path): Path to the file or directory.

Returns:
    bool: True if the path is a directory or already chunked.
