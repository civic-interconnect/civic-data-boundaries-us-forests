#!/usr/bin/env python3
"""
src/civic_data_boundaries_us_forests/cleanup.py

Cleanup routines for the US Forest boundaries pipeline.

Removes:
- downloaded zip files and extracted shapefiles from data-in/
- intermediate exported GeoJSONs from data-in-geojson/

Keeps:
- final chunked GeoJSONs safe in data-out/.

MIT License — maintained by Civic Interconnect
"""

import shutil
import sys
from pathlib import Path

from civic_lib_core import log_utils

from civic_data_boundaries_us_forests.utils.get_paths import (
    get_data_in_dir,
    get_data_in_geojson_dir,
)

__all__ = [
    "clean_data_in_dir",
    "clean_data_in_geojson_dir",
    "main",
]

logger = log_utils.logger


def clean_data_in_dir(data_in_dir: Path) -> None:
    """
    Delete all .zip files and extracted shapefiles from data-in/.

    Leaves the folder structure intact if empty folders remain.
    """
    if not data_in_dir.exists():
        logger.info(f"No cleanup needed. Folder does not exist: {data_in_dir}")
        return

    deleted_files = 0
    deleted_dirs = 0

    for path in data_in_dir.rglob("*"):
        if path.is_file() and path.suffix == ".zip":
            path.unlink()
            logger.info(f"Deleted zip file: {path}")
            deleted_files += 1
        elif path.is_dir():
            if any(p.suffix == ".shp" for p in path.rglob("*.shp")):
                shutil.rmtree(path)
                logger.info(f"Deleted extracted shapefiles folder: {path}")
                deleted_dirs += 1

    logger.info(
        f"Cleanup complete in data-in/. Deleted {deleted_files} zip(s) "
        f"and {deleted_dirs} shapefile folder(s)."
    )


def clean_data_in_geojson_dir(data_in_geojson_dir: Path) -> None:
    """
    Delete all files under data-in-geojson/.

    Removes intermediate GeoJSON exports but leaves data-out/ untouched.
    """
    if not data_in_geojson_dir.exists():
        logger.info(f"No cleanup needed. Folder does not exist: {data_in_geojson_dir}")
        return

    shutil.rmtree(data_in_geojson_dir)
    logger.info(f"Deleted entire data-in-geojson folder: {data_in_geojson_dir}")


def main() -> int:
    """
    CLI entry point for cleanup of all intermediate files.
    """
    try:
        data_in = get_data_in_dir()
        data_in_geojson = get_data_in_geojson_dir()

        clean_data_in_dir(data_in)
        clean_data_in_geojson_dir(data_in_geojson)

        logger.info("Cleanup completed successfully.")
        return 0

    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
