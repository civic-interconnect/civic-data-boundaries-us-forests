#!/usr/bin/env python3
"""
src/civic_data_boundaries_us_forests/fetch.py

Fetch and process shapefiles for US Forests data.

Supports:
- National Forest boundaries
- Ranger District boundaries
- Future nationwide Forest Service layers

Reads layer definitions from YAML files under data-config/.
"""

import sys
import zipfile
from pathlib import Path

import requests
import yaml
from civic_lib_core import log_utils

from civic_data_boundaries_us_forests.utils.get_paths import (
    get_data_in_dir,
    get_repo_root,
)

__all__ = [
    "download_file",
    "extract_zip",
    "process_layer",
    "main",
]

logger = log_utils.logger


def download_file(url: str, dest_path: Path) -> bool:
    logger.debug(f"Preparing to download file from URL: {url}")
    logger.debug(f"Destination path: {dest_path}")

    if dest_path.exists():
        logger.info(f"Skipping download. File already exists: {dest_path}")
        return True

    logger.info(f"Downloading: {url}")

    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        dest_path.parent.mkdir(parents=True, exist_ok=True)

        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        logger.info(f"Downloaded file saved to: {dest_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to download {url}. Error: {e}")
        return False


def extract_zip(zip_path: Path, extract_to: Path) -> bool:
    logger.debug(f"Preparing to extract zip: {zip_path}")
    logger.debug(f"Extraction target: {extract_to}")

    if not zip_path.exists():
        logger.error(f"Zip file does not exist: {zip_path}")
        return False

    if extract_to.exists():
        logger.info(f"Skipping extraction. Folder already exists: {extract_to}")
        return True

    logger.info(f"Extracting {zip_path} to {extract_to}")

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        logger.info(f"Extraction complete: {extract_to}")
        return True

    except Exception as e:
        logger.error(f"Failed to extract {zip_path}. Error: {e}")
        return False


def process_layer(layer: dict) -> bool:
    logger.debug(f"Processing layer config: {layer}")

    required_keys = ["output_dir"]
    for key in required_keys:
        if key not in layer:
            logger.error(f"Missing required key '{key}' in layer config: {layer}")
            return False

    data_in_root = get_data_in_dir()
    output_dir = data_in_root / layer["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory ensured: {output_dir}")

    if "url" not in layer:
        logger.error(f"Missing 'url' for layer: {layer}")
        return False

    url = layer["url"]
    filename = Path(url).name
    zip_path = output_dir / filename
    extract_path = output_dir / filename.replace(".zip", "")

    if not download_file(url, zip_path):
        return False

    return extract_zip(zip_path, extract_path)


def main() -> int:
    try:
        logger.info("Starting data download process for Forest layers...")
        logger.info("Searching for YAML configs in data-config folder...")

        yaml_dir = get_repo_root() / "data-config"
        yaml_files = list(yaml_dir.glob("*.yaml"))

        if not yaml_files:
            logger.error(f"No YAML configs found in: {yaml_dir}")
            return 1

        logger.info(f"Found {len(yaml_files)} YAML config file(s) in: {yaml_dir}")

        for yaml_file in yaml_files:
            logger.info(f"Processing config file: {yaml_file.name}")

            with yaml_file.open("r", encoding="utf-8") as f:
                try:
                    config = yaml.safe_load(f)
                except Exception as e:
                    logger.error(f"Error parsing YAML file {yaml_file}: {e}")
                    return 1

                if not config or "layers" not in config:
                    logger.error(f"YAML config file is empty or missing 'layers': {yaml_file}")
                    return 1

                for layer in config["layers"]:
                    if not process_layer(layer):
                        logger.error(f"Failed processing layer: {layer.get('name', 'Unknown')}")
                        return 1

        logger.info("All forest layers fetched and extracted successfully.")
        return 0

    except Exception as e:
        logger.error(f"Fetch process failed unexpectedly: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
