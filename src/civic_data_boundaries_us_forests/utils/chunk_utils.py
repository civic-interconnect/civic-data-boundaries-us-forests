"""
civic_data_boundaries_us_forests.utils.chunk_utils

Utilities for chunking and managing GeoJSON files.

- Handles chunking of large GeoJSON files into smaller pieces.
- Copies smaller files as-is.
- Provides utility functions for file management and configuration loading.
"""

import shutil
from pathlib import Path

import geopandas as gpd
import yaml
from civic_lib_core import log_utils
from civic_lib_geo.cli.chunk_geojson import chunk_one

from civic_data_boundaries_us_forests.utils.get_paths import get_repo_root

__all__ = [
    "chunk_geojson_file",
    "chunk_geojson_folder",
    "chunk_or_copy_file",
    "copy_geojson_file",
    "get_chunking_params",
    "geojson_feature_count",
    "is_chunked_file",
    "load_all_layer_configs",
    "should_skip_file",
]

logger = log_utils.logger


def chunk_geojson_file(
    geojson_file: Path,
    output_dir: Path,
    max_features: int,
) -> None:
    """
    Chunk a single GeoJSON file into smaller pieces in the output_dir.

    Skips the file if it's a directory or already chunked.
    """
    if should_skip_file(geojson_file):
        return

    chunked_folder = output_dir / f"{geojson_file.stem}_chunked.geojson"
    chunked_folder.mkdir(parents=True, exist_ok=True)

    logger.info(f"Chunking file: {geojson_file} → {chunked_folder}")
    chunk_one(
        geojson_file,
        max_features=max_features,
        output_dir=chunked_folder,
    )


def chunk_geojson_folder(
    input_folder: Path,
    max_features: int,
    output_folder: Path,
) -> None:
    """
    Chunk all eligible GeoJSON files in a folder.

    Args:
        input_folder (Path): Folder containing GeoJSON files.
        max_features (int): Maximum features per chunk.
        output_folder (Path): Destination folder for chunked files.
    """
    geojson_files = list(input_folder.glob("*.geojson"))
    logger.debug(f"Found {len(geojson_files)} GeoJSON files in {input_folder}")

    if not geojson_files:
        logger.warning(f"No GeoJSON files found in {input_folder}")
        return

    for geojson_file in geojson_files:
        chunk_or_copy_file(
            geojson_file,
            max_features,
            output_folder,
        )


def chunk_or_copy_file(
    geojson_file: Path,
    max_features: int,
    output_dir: Path,
) -> None:
    """
    Decide whether to chunk a GeoJSON file or simply copy it.

    Args:
        geojson_file (Path): The file to process.
        max_features (int): Threshold for chunking.
        output_dir (Path): Destination folder.
    """
    feature_count = geojson_feature_count(geojson_file)

    if feature_count > max_features:
        chunked_folder = output_dir / f"{geojson_file.stem}_chunked.geojson"
        chunked_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Chunking file: {geojson_file} → {chunked_folder}")
        chunk_one(
            geojson_file,
            max_features=max_features,
            output_dir=chunked_folder,
        )
    else:
        dest = output_dir / geojson_file.name
        copy_geojson_file(geojson_file, dest)


def copy_geojson_file(src: Path, dest: Path) -> None:
    """
    Copy a GeoJSON file from src to dest.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    logger.info(f"Copied unchunked file to: {dest}")


def get_chunking_params() -> dict:
    """
    Load chunking and simplification parameters from YAML layer configs.

    Returns:
        dict: Dictionary with chunking parameters.
    """
    chunk_max_features = 500
    simplify_tolerance = 0.01

    yaml_dir = get_repo_root() / "data-config"
    yaml_files = list(yaml_dir.glob("*.yaml"))

    for yaml_file in yaml_files:
        with open(yaml_file, encoding="utf-8") as f:
            logger.debug(f"Loading config from: {yaml_file.name}")
            config = yaml.safe_load(f) or {}
            for layer in config.get("layers", []):
                chunk_max_features = layer.get("chunk_max_features", chunk_max_features)
                simplify_tolerance = layer.get("simplify_tolerance", simplify_tolerance)

    return dict(
        chunk_max_features=chunk_max_features,
        simplify_tolerance=simplify_tolerance,
    )


def geojson_feature_count(path: Path) -> int:
    """
    Return the number of features in a GeoJSON file.

    Args:
        path (Path): Path to the GeoJSON file.

    Returns:
        int: Feature count or 0 if reading fails.
    """
    try:
        gdf = gpd.read_file(path)
        count = len(gdf)
        logger.debug(f"{path} has {count} features.")
        return count
    except Exception as e:
        logger.error(f"Could not read {path}: {e}")
        return 0


def is_chunked_file(path: Path) -> bool:
    """
    Return True if the file is already a chunked GeoJSON.

    Args:
        path (Path): Path to the file.

    Returns:
        bool: True if the file ends with '_chunked.geojson'.
    """
    return path.is_file() and path.name.endswith("_chunked.geojson")


def load_all_layer_configs() -> list[dict]:
    """
    Load and merge all YAML layer configs into a single list.

    Returns:
        list[dict]: List of all configured layers.
    """
    yaml_dir = get_repo_root() / "data-config"
    yaml_files = sorted(yaml_dir.glob("*.yaml"))

    all_layers = []
    for yaml_file in yaml_files:
        logger.info(f"Processing YAML config: {yaml_file.name}")
        with open(yaml_file, encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
            all_layers.extend(config.get("layers", []))

    return all_layers


def should_skip_file(path: Path) -> bool:
    """
    Determine whether a file should be skipped during chunking.

    Args:
        path (Path): Path to the file or directory.

    Returns:
        bool: True if the path is a directory or already chunked.
    """
    if path.is_dir():
        logger.debug(f"Skipping directory: {path}")
        return True
    if is_chunked_file(path):
        logger.debug(f"Skipping already-chunked file: {path}")
        return True
    return False
