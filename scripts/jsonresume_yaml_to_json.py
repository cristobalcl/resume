#!/usr/bin/env python3
"""Convert a JSON Resume YAML file into JSON."""

import argparse
import json
from pathlib import Path

import yaml


REQUIRED_TOP_LEVEL_KEYS = (
    "basics",
    "work",
    "education",
    "skills",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default="resume.jsonresume.yaml",
        help="Path to JSON Resume YAML file",
    )
    parser.add_argument(
        "--output",
        default="build/resume.json",
        help="Path to output JSON file",
    )
    return parser.parse_args()


def validate_resume_schema(data: dict) -> None:
    missing = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in data]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Missing required top-level keys: {joined}")

    basics = data.get("basics")
    if not isinstance(basics, dict):
        raise ValueError("'basics' must be a mapping")

    for key in REQUIRED_TOP_LEVEL_KEYS[1:]:
        value = data.get(key)
        if not isinstance(value, list):
            raise ValueError(f"'{key}' must be a list")


def main() -> int:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    if not isinstance(data, dict):
        raise ValueError("Top-level resume document must be a mapping")

    validate_resume_schema(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
