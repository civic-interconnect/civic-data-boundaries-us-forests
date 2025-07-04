#!/usr/bin/env python3
"""
src/civic_data_boundaries_us_forests/export.py

Export US Forest boundaries and districts from downloaded shapefiles into GeoJSON files.

This step:
- reads shapefiles
- optionally splits features by attribute (e.g. one file per forest or district)
- optionally simplifies geometries
- writes .geojson files into data-in-geojson/

It does NOT chunk files.

MIT License — maintained by Civic Interconnect
"""

import sys

import yaml
from civic_lib_core import log_utils

from civic_data_boundaries_us_forests.utils.export_utils import (
    export_split_geojson,
    should_skip_file,
)
from civic_data_boundaries_us_forests.utils.get_paths import (
    get_data_in_geojson_dir,
    get_layer_in_dir,
    get_layer_in_geojson_dir,
    get_repo_root,
)

__all__ = [
    "load_all_layer_configs",
    "export_forest_layer",
    "main",
]

logger = log_utils.logger


def load_all_layer_configs() -> list[dict]:
    """
    Loads and merges all YAML layer configs into a list of layers.

    Returns:
        list[dict]: List of layer configuration dictionaries.
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


def export_forest_layer(layer: dict) -> None:
    """
    Export GeoJSONs from a single forest or district layer.

    Depending on the config:
    - may split by attribute (e.g. FORESTNAME)
    - may simplify geometries

    Outputs:
        GeoJSON files into:
            data-in-geojson/{layer.output_dir}/

    Args:
        layer (dict): Layer configuration dictionary.
    """
    name = layer["name"]
    output_dir = get_layer_in_geojson_dir(layer["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    input_dir = get_layer_in_dir(layer["output_dir"])
    logger.debug(f"Looking for shapefiles in {input_dir}")

    if not input_dir.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        return

    candidates = list(input_dir.glob("*.shp")) or list(input_dir.glob("*/*.shp"))

    if not candidates:
        logger.warning(f"No shapefile found for layer: {name} in {input_dir}")
        return

    for shapefile_path in candidates:
        if should_skip_file(shapefile_path):
            continue

        logger.info(f"Exporting layer: {name}")
        logger.info(f"  Reading shapefile: {shapefile_path}")

        export_split_geojson(
            shapefile_path,
            output_dir,
            split_by=layer.get("split_by"),
            simplify_tolerance=layer.get("simplify_tolerance", 0.01),
        )

    logger.info(f"Finished exporting layer: {name}")


def main() -> int:
    """
    CLI entry point to export forest-related layers to GeoJSON.

    Returns:
        int: Exit code (0 if successful, 1 if failed).
    """
    try:
        logger.info("=== Starting EXPORT process for Forest layers ===")

        geojson_dir = get_data_in_geojson_dir()
        geojson_dir.mkdir(parents=True, exist_ok=True)

        layers = load_all_layer_configs()

        for layer in layers:
            export_forest_layer(layer)

        logger.info("=== EXPORT complete ===")
        return 0

    except Exception as e:
        logger.error(f"Export process failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
