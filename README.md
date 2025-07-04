# civic-data-boundaries-us-forests

[![Version](https://img.shields.io/badge/version-v0.0.1-blue)](https://github.com/civic-interconnect/civic-data-boundaries-us/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/civic-interconnect/civic-data-boundaries-us/actions/workflows/tests.yml/badge.svg)](https://github.com/civic-interconnect/civic-data-boundaries-us/actions)

> U.S. National Forests Boundary Data for [Civic Interconnect](https://github.com/civic-interconnect)

This repository provides and hosts standardized GeoJSON boundaries for:

- United States National Forests

Data is extracted, transformed, and exported for use in civic data pipelines and mapping applications, such as the [Civic Interconnect Geo Explorer](https://civic-interconnect.github.io/geo-explorer/).

GeoJSON files are chunked and optimized for delivery via GitHub Pages.

## Local Development

This repo supports the same pattern as other Civic Interconnect data projects. Use Python scripts to:

- Download official national datasets
- Process and simplify geometries
- Export per-state and nationwide GeoJSONs
- Build indexes and manifests

## Development

See [DEVELOPER.md](./DEVELOPER.md)

## Pipeline

- civic-usa fetch      Download shapefiles into data-in/.
- civic-usa export     Export GeoJSON into data-in-geojson/.
- civic-usa chunk      Chunk data from data-in-geojson/ to data-out.
- civic-usa index      Generate index.json.
- civic-usa cleanup    Cleanup temporary files and directories.

## Space Requirements

civic-data-boundaries-us-forests
- x Files, y Folders
- ~xy MB

For:

- Chunked GeoJSON exports
- manifests and index.json
- Any remaining raw shapefiles
- Project source, YAML, etc.


## References

- [USDA Forest Service Geospatial Data](https://data.fs.usda.gov/geodata/edw/datasets.php)
  - [boundaries](https://data.fs.usda.gov/geodata/edw/datasets.php?dsetCategory=boundaries)
  - Administrative Forest Boundaries
  - Ranger District Boundaries

- [USGS Protected Areas Database (PAD-US)](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-download)
