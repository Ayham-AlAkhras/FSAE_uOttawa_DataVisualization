# FSAE_uOttawa_DataVisualization

Small DearPyGui tool for loading and validating **MoTeC CSV logs** before using them for analysis or visualization.

The goal is to catch broken or corrupted logs early and standardize how CSVs are loaded across the team.

---

## What it does
- Loads MoTeC-style CSV files  
- Extracts metadata (session, car, date, comments, etc.)  
- Handles **multiline metadata fields** (e.g. comments with newlines)  
- Validates:
  - file exists
  - data is not empty
  - data is not all zeros
  - sensors show variation (not frozen)
- Displays:
  - metadata
  - preview of numeric data
- Can batch-test CSVs in `debugging_files/` to verify the loader