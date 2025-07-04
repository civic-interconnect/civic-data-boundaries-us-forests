"""
civic_data_boundaries_us_forests.utils.export_utils

Shared export utilities for the US Forest boundaries pipeline.

MIT License — maintained by Civic Interconnect
"""

import json
from pathlib import Path

import geopandas as gpd
from civic_lib_core import log_utils

__all = [
    "export_split_geojson",
    "load_layer",
    "remove_crs_field",
    "should_skip_file",
    "validate_columns",
]


logger = log_utils.logger


def export_split_geojson(
    shp_path: Path,
    output_dir: Path,
    split_by: str | None = None,
    simplify_tolerance: float = 0.01,
) -> None:
    """
    Export a shapefile to one or more GeoJSON files.

    If split_by is provided, saves one file per unique attribute value.

    Args:
        shp_path (Path): Path to the .shp file.
        output_dir (Path): Output folder.
        split_by (str, optional): Attribute to split on.
        simplify_tolerance (float, optional): Simplification tolerance in degrees.
    """
    logger.info(f"Reading shapefile: {shp_path}")
    gdf = gpd.read_file(shp_path)

    if simplify_tolerance > 0:
        gdf["geometry"] = gdf["geometry"].simplify(simplify_tolerance, preserve_topology=True)
        logger.info(f"Simplified geometries with tolerance {simplify_tolerance}")

    if split_by:
        validate_columns(gdf, [split_by], label=shp_path.name)

        unique_vals = gdf[split_by].dropna().unique()
        logger.info(f"Splitting layer by '{split_by}' → {len(unique_vals)} groups")

        for val in unique_vals:
            sub_gdf = gdf[gdf[split_by] == val]
            if sub_gdf.empty:
                logger.warning(f"Skipped empty group for {split_by}={val}")
                continue
            logger.debug(f"Processing group: {val} with {len(sub_gdf)} features")

            # Safe filename
            safe_val = (
                str(val).strip().lower().replace(" ", "_").replace("/", "-").replace("\\", "-")
            )
            filename = f"{safe_val}.geojson"
            filepath = output_dir / filename
            output_dir.mkdir(parents=True, exist_ok=True)

            sub_gdf.to_file(filepath, driver="GeoJSON", index=False)
            remove_crs_field(filepath)
            logger.info(f"Saved split GeoJSON: {filepath}")
    else:
        filename = shp_path.stem + ".geojson"
        filepath = output_dir / filename
        gdf.to_file(filepath, driver="GeoJSON", index=False)
        remove_crs_field(filepath)
        logger.info(f"Saved GeoJSON: {filepath}")


def load_layer(source: Path, required_cols: list[str]) -> gpd.GeoDataFrame:
    """
    Load a shapefile layer and validate required columns.

    Args:
        source (Path): Path to .shp file.
        required_cols (list[str]): Required column names.

    Returns:
        gpd.GeoDataFrame: Loaded GeoDataFrame.
    """
    gdf = gpd.read_file(source)
    validate_columns(gdf, required_cols, label=source.name)
    return gdf


def remove_crs_field(geojson_path: Path) -> None:
    """
    Remove the 'crs' property from a GeoJSON file, if present.

    Args:
        geojson_path (Path): Path to the GeoJSON file.
    """
    try:
        with geojson_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if "crs" in data:
            del data["crs"]
            with geojson_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Removed 'crs' property from {geojson_path}")
    except Exception as e:
        logger.warning(f"Could not remove 'crs' from {geojson_path}: {e}")


def should_skip_file(path: Path) -> bool:
    """
    Determine whether this path should be skipped.

    Skips directories and files with unexpected extensions.
    """
    if path.is_dir():
        logger.debug(f"Skipping directory: {path}")
        return True
    return False


def validate_columns(gdf: gpd.GeoDataFrame, columns: list[str], label: str) -> None:
    """
    Check if required columns exist in a GeoDataFrame.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame to check.
        columns (list[str]): Required column names.
        label (str): Name to show in error messages.
    """
    missing = [col for col in columns if col not in gdf.columns]
    if missing:
        logger.debug(f"All columns in {label}: {gdf.columns.tolist()}")
        raise ValueError(f"{label} is missing columns: {missing}")
