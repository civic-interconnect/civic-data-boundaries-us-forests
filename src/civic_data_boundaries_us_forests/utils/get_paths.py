"""
civic_data_boundaries_us_forests.utils.get_paths

Utilities for resolving paths to various data directories
in the civic_data_boundaries_us_forests package.

Ensures that the pipeline works when run directly
from source code and when invoked via the installed CLI.
"""

from pathlib import Path

__all__ = [
    "get_data_in_dir",
    "get_data_in_geojson_dir",
    "get_data_out_dir",
    "get_layer_in_dir",
    "get_layer_in_geojson_dir",
    "get_layer_out_dir",
    "get_repo_root",
]


def get_data_in_dir() -> Path:
    """
    Return the root data-in directory for raw downloads
    (zip files and extracted shapefiles).

    Returns:
        Path: data-in directory.
    """
    return get_repo_root() / "data-in"


def get_data_in_geojson_dir() -> Path:
    """
    Return the root data-in-geojson directory for intermediate exported GeoJSONs
    before chunking.

    Returns:
        Path: data-in-geojson directory.
    """
    return get_repo_root() / "data-in-geojson"


def get_data_out_dir() -> Path:
    """
    Return the root data-out directory for the final committed GeoJSONs
    (chunked and ready for deployment).

    Returns:
        Path: data-out directory.
    """
    return get_repo_root() / "data-out"


def get_layer_in_dir(layer_output_dir: str) -> Path:
    """
    Return the input folder for a specific layer's shapefiles.

    Args:
        layer_output_dir (str): Subdirectory under data-in/ where this layer's
            downloaded and extracted shapefiles live.

    Returns:
        Path: Full path to that layer's folder under data-in/.
    """
    return get_data_in_dir() / layer_output_dir


def get_layer_in_geojson_dir(layer_output_dir: str) -> Path:
    """
    Return the intermediate GeoJSON folder for a specific layer.

    Args:
        layer_output_dir (str): Subdirectory under data-in-geojson/ where this layer's
            exported (but not yet chunked) GeoJSONs are stored.

    Returns:
        Path: Full path to that layer's folder under data-in-geojson/.
    """
    return get_data_in_geojson_dir() / layer_output_dir


def get_layer_out_dir(layer_output_dir: str) -> Path:
    """
    Return the output folder for a specific layer's final chunked GeoJSONs.

    Args:
        layer_output_dir (str): Subdirectory under data-out/ for this layer.

    Returns:
        Path: Full path to that layer's folder under data-out/.
    """
    return get_data_out_dir() / layer_output_dir


def get_repo_root() -> Path:
    """
    Return the root directory of the civic-data-boundaries-us-forests repository.

    This function first checks whether the file path is running from
    a cloned source repo (using __file__ as a reference), and if that
    does not locate the repo, searches upward from the current working
    directory until it finds a folder containing a data-config directory.

    Returns:
        Path: Path to the repository root.

    Raises:
        RuntimeError: If the repo root cannot be found.
    """
    # Check if we’re running from source
    source_root = Path(__file__).resolve().parents[3]
    if (source_root / "data-config").exists():
        return source_root

    # Otherwise search upwards from CWD
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / "data-config").exists():
            return parent

    raise RuntimeError(f"Could not locate repository root from working dir: {Path.cwd()}")
