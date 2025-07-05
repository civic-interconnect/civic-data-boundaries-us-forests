# Module `fetch`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `download_file(url: str, dest_path: pathlib.Path) -> bool`

No description available.

### `extract_zip(zip_path: pathlib.Path, extract_to: pathlib.Path) -> bool`

No description available.

### `get_data_in_dir() -> pathlib.Path`

Return the root data-in directory for raw downloads
(zip files and extracted shapefiles).

Returns:
    Path: data-in directory.

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

### `main() -> int`

No description available.

### `process_layer(layer: dict) -> bool`

No description available.
