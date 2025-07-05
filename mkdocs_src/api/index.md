# Module `index`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `build_index_main() -> int`

Build index.json summarizing exported GeoJSONs from data-out and data-out-chunked.
Adds file size in MB (2 decimal places) to each index entry.

### `compute_bbox(geojson_path: pathlib.Path) -> list[float] | None`

Compute bounding box [minx, miny, maxx, maxy] for a GeoJSON file.

Args:
    geojson_path (Path): Path to the GeoJSON file.

Returns:
    list[float] | None: Bounding box, or None if read fails.

### `get_data_out_dir() -> pathlib.Path`

Return the root data-out directory for the final committed GeoJSONs
(chunked and ready for deployment).

Returns:
    Path: data-out directory.

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

### `index_geojsons_in_folder(base_dir: pathlib.Path, relative_prefix: str) -> list[dict]`

Scan a folder recursively for GeoJSON files and return index entries.

Args:
    base_dir (Path): Folder to scan.
    relative_prefix (str): e.g. "data-out" or "data-out-chunked"

Returns:
    list[dict]: Index entries for each GeoJSON found.

### `main() -> int`

CLI entry point for index generation.
