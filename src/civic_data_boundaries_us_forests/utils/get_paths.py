"""
civic_data_boundaries_us_forests.utils.get_paths

Utilities for resolving paths to various data directories
in the civic_data_boundaries_us_forests package.
"""

from pathlib import Path

__all__ = [
    "get_repo_root",
    "get_data_in_dir",
    "get_data_in_geojson_dir",
    "get_data_out_dir",
    "get_layer_in_dir",
    "get_layer_in_geojson_dir",
    "get_layer_out_dir",
]


def get_repo_root(levels_up: int = 3) -> Path:
    """
    Return the root directory of the repo by walking up parent folders.

    Args:
        levels_up (int): How many levels up to go from this file.
            Defaults to 3, assuming this file is under:
            src/civic_data_boundaries_us_forests/utils/

    Returns:
        Path: Root directory of the repository.
    """
    return Path(__file__).resolve().parents[levels_up]


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
