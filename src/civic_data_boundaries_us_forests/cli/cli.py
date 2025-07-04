#!/usr/bin/env python3
"""
cli.py

Command-line interface (CLI) for civic-data-boundaries-us-forests.

Provides commands for:
- Fetching TIGER/Line shapefiles
- Exporting and chunking all GeoJSON files
- Generating spatial indexes and summaries

Run `civic-usa --help` for usage.
"""

import sys

import typer
from civic_lib_core import log_utils

from civic_data_boundaries_us_forests import chunk, cleanup, export, fetch, index

log_utils.init_logger()
logger = log_utils.logger

app = typer.Typer(help="Civic USA CLI — boundary export and indexing.")


@app.command("fetch")
def fetch_command():
    """
    Download required shapefiles into data-in/.
    Skips download if files already exist.
    """
    fetch.main()


@app.command("export")
def export_command():
    """
    Export all data into data-in-geojson/.
    """
    export.main()


@app.command("chunk")
def chunk_command():
    """
    Chunk all data from data-in-geojson/ to data-out/.
    """
    chunk.main()


@app.command("index")
def index_command():
    """
    Generate index.json and other summary metadata files in data-out/.
    """
    index.main()


@app.command("cleanup")
def cleanup_command():
    """
    Cleanup temporary files and directories created during export.

    Deletes all .zip files and extracted shapefiles from data-in/,
    and all intermediate content in data-in-geojson/.
    Keeps chunked GeoJSONs safe in data-out/.
    """
    cleanup.main()


def main() -> int:
    app()
    return 0


if __name__ == "__main__":
    sys.exit(main())
