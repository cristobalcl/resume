#!/usr/bin/env python3
"""Translate a JSON Resume document into RenderCV YAML."""

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default="build/resume.json",
        help="Path to JSON Resume input JSON",
    )
    parser.add_argument(
        "--output",
        default="build/rendercv.yaml",
        help="Path to output RenderCV YAML",
    )
    parser.add_argument(
        "--theme",
        default="moderncv",
        help="RenderCV theme name",
    )
    return parser.parse_args()


def compact_text(value: str) -> str:
    return " ".join((value or "").split())


def compose_location(location: dict) -> str:
    if not isinstance(location, dict):
        return ""

    parts = [
        location.get("city", ""),
        location.get("region", ""),
        location.get("countryCode", ""),
    ]
    return ", ".join(part for part in parts if part)


def build_social_networks(profiles: list) -> list:
    social_networks = []
    for profile in profiles:
        if not isinstance(profile, dict):
            continue

        network = profile.get("network")
        if not network:
            continue

        username = profile.get("username")
        if not username:
            url = profile.get("url", "")
            if url:
                parsed = urlparse(url)
                path = parsed.path.strip("/")
                username = path.rsplit("/", 1)[-1] if path else parsed.netloc

        if not username:
            continue

        social_networks.append({"network": network, "username": username})

    return social_networks


def format_date_range(start: str, end: str) -> str:
    if start and end:
        return f"{start} - {end}"
    if start:
        return f"Since {start}"
    return end or ""


def work_to_experience(work_items: list) -> list:
    experience = []
    for item in work_items:
        if not isinstance(item, dict):
            continue

        company = item.get("name")
        position = item.get("position")
        if not company or not position:
            continue

        highlights = item.get("highlights") or []
        if isinstance(highlights, str):
            highlights = [highlights]

        start = item.get("startDate", "")
        end = item.get("endDate", "") or ("present" if item.get("startDate") else "")
        summary = compact_text(item.get("summary", ""))

        entry = {
            "company": company,
            "position": position,
            "start_date": start,
            "end_date": end,
            "date": format_date_range(start, end),
            "location": item.get("location", ""),
            "summary": summary,
            "highlights": [compact_text(point) for point in highlights if point],
        }

        experience.append({k: v for k, v in entry.items() if v})

    return experience


def education_to_entries(items: list) -> list:
    entries = []
    for item in items:
        if not isinstance(item, dict):
            continue

        institution = item.get("institution")
        area = item.get("area")
        if not institution or not area:
            continue

        start = item.get("startDate", "")
        end = item.get("endDate", "")
        summary = item.get("score", "")
        highlights = item.get("courses") or []

        entry = {
            "institution": institution,
            "area": area,
            "degree": item.get("studyType", ""),
            "start_date": start,
            "end_date": end,
            "date": format_date_range(start, end),
            "summary": compact_text(summary),
            "highlights": [compact_text(course) for course in highlights if course],
        }

        entries.append({k: v for k, v in entry.items() if v})

    return entries


def projects_to_entries(items: list) -> list:
    entries = []
    for item in items:
        if not isinstance(item, dict):
            continue

        name = item.get("name")
        if not name:
            continue

        highlights = item.get("highlights") or []
        if isinstance(highlights, str):
            highlights = [highlights]

        start = item.get("startDate", "")
        end = item.get("endDate", "")
        summary = item.get("description", "")
        url = item.get("url", "")
        if url:
            summary = f"{summary} ({url})" if summary else url

        entry = {
            "name": name,
            "start_date": start,
            "end_date": end,
            "date": format_date_range(start, end),
            "summary": compact_text(summary),
            "highlights": [compact_text(point) for point in highlights if point],
        }
        entries.append({k: v for k, v in entry.items() if v})

    return entries


def certificates_to_entries(items: list) -> list:
    entries = []
    for item in items:
        if not isinstance(item, dict):
            continue

        name = item.get("name")
        if not name:
            continue

        issuer = item.get("issuer", "")
        summary = f"Issued by {issuer}" if issuer else ""
        url = item.get("url", "")
        if url:
            summary = f"{summary}. {url}" if summary else url

        date = item.get("date", "")
        entry = {
            "name": name,
            "date": date,
            "summary": compact_text(summary),
        }
        entries.append({k: v for k, v in entry.items() if v})

    return entries


def skills_to_entries(items: list) -> list:
    entries = []
    for item in items:
        if not isinstance(item, dict):
            continue

        name = item.get("name")
        keywords = item.get("keywords") or []
        if not name or not keywords:
            continue

        entries.append(
            {
                "label": name,
                "details": ", ".join(compact_text(keyword) for keyword in keywords if keyword),
            }
        )

    return entries


def languages_to_entries(items: list) -> list:
    entries = []
    for item in items:
        if not isinstance(item, dict):
            continue

        language = item.get("language")
        fluency = item.get("fluency", "")
        if not language:
            continue

        entries.append({"label": language, "details": compact_text(fluency) or ""})

    return entries


def publications_to_entries(items: list) -> list:
    entries = []
    for item in items:
        if not isinstance(item, dict):
            continue

        title = item.get("name")
        if not title:
            continue

        authors = item.get("authors") or []
        if isinstance(authors, str):
            authors = [authors]

        entry = {
            "title": title,
            "authors": [compact_text(author) for author in authors if author],
            "date": item.get("releaseDate", ""),
            "url": item.get("website", ""),
            "journal": item.get("publisher", ""),
            "summary": compact_text(item.get("summary", "")),
        }
        entries.append({k: v for k, v in entry.items() if v})

    return entries


def volunteer_to_entries(items: list) -> list:
    entries = []
    for item in items:
        if not isinstance(item, dict):
            continue

        organization = item.get("organization")
        position = item.get("position")
        if not organization or not position:
            continue

        highlights = item.get("highlights") or []
        if isinstance(highlights, str):
            highlights = [highlights]

        start = item.get("startDate", "")
        end = item.get("endDate", "")
        entry = {
            "name": f"{organization} - {position}",
            "start_date": start,
            "end_date": end,
            "date": format_date_range(start, end),
            "summary": compact_text(item.get("summary", "")),
            "highlights": [compact_text(point) for point in highlights if point],
        }
        entries.append({k: v for k, v in entry.items() if v})

    return entries


def build_sections(data: dict) -> dict:
    basics = data.get("basics", {})
    sections = {}

    summary = compact_text(basics.get("summary", ""))
    if summary:
        sections["summary"] = [summary]

    experience = work_to_experience(data.get("work", []))
    if experience:
        sections["experience"] = experience

    education = education_to_entries(data.get("education", []))
    if education:
        sections["education"] = education

    projects = projects_to_entries(data.get("projects", []))
    if projects:
        sections["projects"] = projects

    certificates = certificates_to_entries(data.get("certificates", []))
    if certificates:
        sections["certificates"] = certificates

    volunteer = volunteer_to_entries(data.get("volunteer", []))
    if volunteer:
        sections["volunteer"] = volunteer

    publications = publications_to_entries(data.get("publications", []))
    if publications:
        sections["publications"] = publications

    skills = skills_to_entries(data.get("skills", []))
    if skills:
        sections["skills"] = skills

    languages = languages_to_entries(data.get("languages", []))
    if languages:
        sections["languages"] = languages

    return sections


def build_rendercv_document(data: dict, theme: str) -> dict:
    basics = data.get("basics", {})
    cv = {
        "name": basics.get("name", ""),
        "headline": basics.get("label", ""),
        "location": compose_location(basics.get("location", {})),
        "email": basics.get("email", ""),
        "phone": basics.get("phone", ""),
        "website": basics.get("url", ""),
        "social_networks": build_social_networks(basics.get("profiles", [])),
        "sections": build_sections(data),
    }

    document = {
        "cv": {k: v for k, v in cv.items() if v},
        "design": {"theme": theme},
    }
    return document


def main() -> int:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as stream:
        data = json.load(stream)

    if not isinstance(data, dict):
        raise ValueError("Input JSON Resume must be a JSON object")

    document = build_rendercv_document(data, args.theme)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(document, stream, sort_keys=False, allow_unicode=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
