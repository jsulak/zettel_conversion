# "The Archive" Zettelkasten to Obsidian Converter

A Python script to convert "The Archive" Zettelkasten-style Markdown files (from The Archive) into Obsidian-compatible format.

## Features

- Converts files named `<ID> <Title>.md` to Obsidian format
- Extracts metadata (Title, Date, Keywords) from note content
- Converts hashtag keywords (#tag) to YAML tags list
- Generates Obsidian frontmatter with:
  - `title` — from metadata or filename
  - `date` — original timestamp
  - `tags` — list of keywords
  - `aliases` — includes numeric ID for [[ID]]-style links
  - `id` — original zettel ID
- Preserves note body content
- Removes backlink references (e.g., `Backlinks: [[202507121559]]`)
- Copies media directory recursively
- Clears output directory before conversion

## Requirements

- Python 3.6+
- PyYAML

## Installation

```bash
pip install PyYAML
```

## Usage

```bash
python3 convert_to_obsidian.py <input_dir> <output_dir>
```

Or run directly (if executable):

```bash
./convert_to_obsidian.py <input_dir> <output_dir>
```

### Example

```bash
./convert_to_obsidian.py ~/Documents/Zettel ~/Documents/ObsidianVault
```

## Input Format

Files should follow the pattern: `<ID> <Title>.md`

Example filename: `202504211559 Ask first and summarize last.md`

Content should include metadata at the beginning:
```
Title: Ask first and summarize last
Date: 2025-04-21T15:59
Keywords: #productivity #communication

Note content goes here...
```

## Output Format

The script generates Obsidian-compatible files with YAML frontmatter:

```yaml
---
id: 202504211559
title: Ask first and summarize last
date: 2025-04-21T15:59
tags:
- productivity
- communication
aliases:
- 202504211559
---

Note content goes here...
```

## Error Handling

- Skips files that don't match the expected filename pattern
- Prints informative messages for converted and skipped files
- Continues processing even if individual files fail

## Media Files

If a `media` directory exists in the input directory, it will be recursively copied to the output directory to preserve image and attachment references.
