#!/usr/bin/env python3
"""
src/civic_data_boundaries_us_forests/chunk.py

Chunk US Forest boundaries and districts GeoJSON files
from data-in-geojson as needed, placing the final output
into data-out.

MIT License — maintained by Civic Interconnect
"""

import sys

from civic_lib_core import log_utils

from civic_data_boundaries_us_forests.utils.chunk_utils import (
    chunk_geojson_folder,
    chunk_or_copy_file,
    get_chunking_params,
    load_all_layer_configs,
)
from civic_data_boundaries_us_forests.utils.export_utils import export_split_geojson
from civic_data_boundaries_us_forests.utils.get_paths import (
    get_data_out_dir,
    get_layer_in_dir,
    get_layer_in_geojson_dir,
    get_layer_out_dir,
)

__all__ = [
    "chunk_layers",
    "export_forest_layer",
    "main",
]

logger = log_utils.logger


def export_forest_layer(layer: dict) -> None:
    """
    Export GeoJSONs from a single forest or district layer.

    Reads shapefiles from data-in/ and writes either single
    or split GeoJSONs into data-out/.

    Args:
        layer (dict): Configuration dictionary for the layer.
    """
    name = layer["name"]
    output_dir = get_layer_out_dir(layer["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    input_dir = get_layer_in_dir(layer["output_dir"])
    candidates = list(input_dir.glob("*.shp")) or list(input_dir.glob("*/*.shp"))

    if not candidates:
        logger.warning(f"No shapefiles found for layer: {name} in {input_dir}")
        return

    for shapefile_path in candidates:
        logger.info(f"Exporting layer: {name}")
        logger.info(f"  Reading: {shapefile_path}")
        export_split_geojson(
            shapefile_path,
            output_dir,
            split_by=layer.get("split_by"),
            simplify_tolerance=layer.get("simplify_tolerance", 0.01),
        )

    logger.info(f"Finished exporting layer: {name}")


def chunk_layers() -> None:
    """
    Chunk all exported GeoJSONs from data-in-geojson, based on YAML configs.

    Writes all final chunked (or copied) GeoJSONs into data-out/.
    """
    chunk_params = get_chunking_params()
    max_features = chunk_params["chunk_max_features"]

    geojson_out_root = get_data_out_dir()
    geojson_out_root.mkdir(parents=True, exist_ok=True)

    layers = load_all_layer_configs()

    for layer in layers:
        layer_input_dir = get_layer_in_geojson_dir(layer["output_dir"])
        layer_output_dir = get_layer_out_dir(layer["output_dir"])
        layer_output_dir.mkdir(parents=True, exist_ok=True)

        if not layer_input_dir.exists():
            logger.warning(f"Layer input dir does not exist: {layer_input_dir}")
            continue

        split_by = layer.get("split_by")

        if split_by:
            # Process subfolders created by the split
            subfolders = [p for p in layer_input_dir.iterdir() if p.is_dir()]
            if not subfolders:
                logger.info(f"No subfolders found in {layer_input_dir}")
                continue

            for subfolder in subfolders:
                logger.info(f"Searching for GeoJSONs in {subfolder}")
                geojson_files = list(subfolder.glob("*.geojson"))

                if not geojson_files:
                    logger.info(f"No GeoJSONs found in {subfolder}")
                    continue

                for geojson_file in geojson_files:
                    chunked_subfolder = layer_output_dir / geojson_file.stem
                    chunked_subfolder.mkdir(parents=True, exist_ok=True)

                    logger.info(f"Chunking {geojson_file} into {chunked_subfolder}")

                    chunk_or_copy_file(
                        geojson_file,
                        max_features,
                        chunked_subfolder,
                    )
        else:
            logger.info(f"Checking all files in {layer_input_dir} for chunking or copying...")
            chunk_geojson_folder(
                layer_input_dir,
                max_features,
                layer_output_dir,
            )


def main() -> int:
    """
    CLI entry point for chunking all GeoJSON files as needed.
    """
    try:
        logger.info("Starting chunking process...")
        chunk_layers()
        logger.info("Export and chunking complete.")
        return 0

    except Exception as e:
        logger.error(f"Chunking process failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
