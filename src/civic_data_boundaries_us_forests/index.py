#!/usr/bin/env python3
"""
src/civic_data_boundaries_us_forests/index.py

Generate index.json and summary metadata in data-out/ and data-out-chunked/.

Used by civic-usa CLI:
    civic-usa index

Currently builds:
- index.json with bounding boxes
- Optional: summary manifest

MIT License — maintained by Civic Interconnect
"""

import json
import sys
from pathlib import Path

import geopandas as gpd
from civic_lib_core import log_utils

from civic_data_boundaries_us_forests.utils.get_paths import (
    get_data_out_dir,
    get_repo_root,
)

__all__ = [
    "build_index_main",
    "compute_bbox",
    "index_geojsons_in_folder",
    "main",
]

logger = log_utils.logger


def build_index_main() -> int:
    """
    Build index.json summarizing exported GeoJSONs from data-out and data-out-chunked.
    Adds file size in MB (2 decimal places) to each index entry.
    """
    out_dir = get_data_out_dir()
    chunked_dir = get_repo_root() / "data-out-chunked"

    index = []

    # Index data-out
    index += index_geojsons_in_folder(out_dir, "data-out")

    # Index data-out-chunked
    if chunked_dir.exists():
        index += index_geojsons_in_folder(chunked_dir, "data-out-chunked")
    else:
        logger.info(f"No chunked data found at {chunked_dir}")

    # Compute file sizes for all entries
    for entry in index:
        absolute_path = get_repo_root() / entry["path"]
        if absolute_path.exists():
            size_bytes = absolute_path.stat().st_size
            size_mb = round(size_bytes / (1024 * 1024), 2)
            entry["size_mb"] = size_mb
        else:
            logger.warning(f"File listed in index not found: {absolute_path}")
            entry["size_mb"] = None

    # Write combined index
    index_output_path = out_dir / "index.json"
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(index_output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    logger.info(f"index.json written to {index_output_path}")
    logger.info(f"Indexed {len(index)} GeoJSON files.")

    # Write chunked-only index
    chunked_index = [i for i in index if i["path"].startswith("data-out-chunked/")]
    if chunked_index:
        chunked_index_path = chunked_dir / "index.json"
        with open(chunked_index_path, "w", encoding="utf-8") as f:
            json.dump(chunked_index, f, indent=2)
        logger.info(f"Chunked-only index.json written to {chunked_index_path}")

    return 0


def compute_bbox(geojson_path: Path) -> list[float] | None:
    """
    Compute bounding box [minx, miny, maxx, maxy] for a GeoJSON file.

    Args:
        geojson_path (Path): Path to the GeoJSON file.

    Returns:
        list[float] | None: Bounding box, or None if read fails.
    """
    try:
        gdf = gpd.read_file(geojson_path)
        bounds = gdf.total_bounds
        bbox = [round(float(x), 6) for x in bounds]
        logger.debug(f"Computed bounds for {geojson_path.name}: {bbox}")
        return bbox
    except Exception as e:
        logger.warning(f"Could not read {geojson_path}: {e}")
        return None


def index_geojsons_in_folder(base_dir: Path, relative_prefix: str) -> list[dict]:
    """
    Scan a folder recursively for GeoJSON files and return index entries.

    Args:
        base_dir (Path): Folder to scan.
        relative_prefix (str): e.g. "data-out" or "data-out-chunked"

    Returns:
        list[dict]: Index entries for each GeoJSON found.
    """
    index_entries = []

    geojson_files = list(base_dir.rglob("*.geojson"))
    if not geojson_files:
        logger.info(f"No geojson files found in {base_dir}")
        return []

    logger.info(f"Found {len(geojson_files)} geojson files in {base_dir}")

    for geojson in geojson_files:
        logger.debug(f"Indexing: {geojson}")
        bbox = compute_bbox(geojson)
        if bbox is not None:
            relative_path = geojson.relative_to(base_dir)
            index_entries.append({
                "path": f"{relative_prefix}/{str(relative_path).replace('\\', '/')}",
                "bbox": bbox,
            })
        else:
            logger.warning(f"Skipping {geojson} because bounding box could not be computed.")

    return index_entries


def main() -> int:
    """
    CLI entry point for index generation.
    """
    try:
        return build_index_main()
    except Exception as e:
        logger.error(f"Index build failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
