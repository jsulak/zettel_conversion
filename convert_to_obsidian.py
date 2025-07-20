"""
convert_to_obsidian.py

Purpose:
    Convert Zettelkasten-style Markdown files (from The Archive) into Obsidian-compatible format.

Features:
    - Reads files named as "<ID> <Title>.md" from input directory.
    - Extracts `Title`, `Date`, and `Keywords` from note body metadata.
    - Converts `Keywords` (in #tag form) into YAML `tags` list.
    - Automatically populates an Obsidian front matter section with:
        • title       — from metadata or filename title.
        • date        — original timestamp.
        • tags        — list of keywords.
        • aliases     — includes the numeric ID, allowing [[ID]]-style links.
    - Optionally retains an `id:` field if required for custom workflows.
    - Preserves note body content intact.
    - Outputs converted files to specified output directory, keeping original filenames.

Usage:
    python3 convert_to_obsidian.py <input_dir> <output_dir>

Notes:
    - The `aliases:` field is essential for Obsidian to resolve ID-based links.
    - Including `id:` is optional and only useful for custom metadata queries.
    - Script assumes the first non-body metadata lines are Title, Date, and Keywords.
    - Filenames must match the pattern: "<ID> <Title>.md" (e.g., "202504211559 Ask first and summarize last.md").
"""





import os, re, yaml
from pathlib import Path

def parse_filename(filename: Path):
    """Extract ID and title from Zettelkasten filename.
    
    Args:
        filename: Path object with stem matching pattern "<ID> <Title>"
        
    Returns:
        tuple: (id_string, title_string)
        
    Raises:
        ValueError: If filename doesn't match expected pattern
    """
    name = filename.stem
    m = re.match(r"(\d+)\s+(.*)", name)
    if not m:
        raise ValueError(f"Bad filename: {filename}")
    return m.group(1), m.group(2)

def parse_metadata(lines):
    """Extract metadata from note content lines.
    
    Parses Title, Date, and Keywords from the beginning of note content.
    Keywords in #tag format are converted to a tags list.
    
    Args:
        lines: List of strings representing file content lines
        
    Returns:
        tuple: (metadata_dict, remaining_body_lines)
    """
    md, body_start = {}, 0
    for i, L in enumerate(lines):
        if L.startswith("Title:"):
            md["title"] = L.split(":",1)[1].strip()
        elif L.startswith("Date:"):
            md["date"] = L.split(":",1)[1].strip()
        elif L.startswith("Keywords:"):
            md["tags"] = re.findall(r"#(\w+)", L)
            body_start = i + 1
            break
    return md, lines[body_start:]

def build_frontmatter(md):
    """Generate YAML frontmatter block from metadata dictionary.
    
    Args:
        md: Dictionary containing metadata fields
        
    Returns:
        str: YAML frontmatter wrapped in --- delimiters
    """
    return "---\n" + yaml.safe_dump(md, sort_keys=False) + "---\n"

def convert_note(in_path: Path, out_path: Path):
    """Convert a single Zettelkasten note to Obsidian format.
    
    Reads the input file, extracts metadata and content, then writes
    an Obsidian-compatible file with YAML frontmatter.
    
    Args:
        in_path: Path to input Zettelkasten file
        out_path: Path where converted file should be written
    """
    file_id, file_title = parse_filename(in_path)
    lines = in_path.read_text(encoding="utf-8").splitlines(keepends=True)
    md, body = parse_metadata(lines)

    md["id"] = file_id
    md.setdefault("title", file_title)
    md["aliases"] = [file_id]

    front = build_frontmatter(md)
    out_path.write_text(front + "\n" + "".join(body), encoding="utf-8")

def main(in_dir, out_dir):
    """Convert all Markdown files in input directory to Obsidian format.
    
    Args:
        in_dir: Path to directory containing Zettelkasten files
        out_dir: Path to directory where converted files will be written
    """
    in_dir, out_dir = Path(in_dir), Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    for f in in_dir.glob("*.md"):
        convert_note(f, out_dir / f.name)
        print("Converted:", f.name)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("input_dir"); p.add_argument("output_dir")
    args = p.parse_args()
    main(args.input_dir, args.output_dir)
