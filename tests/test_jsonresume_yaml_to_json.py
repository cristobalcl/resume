import json
import sys

from scripts import jsonresume_yaml_to_json


def test_validate_resume_schema_accepts_minimal_document():
    data = {
        "basics": {"name": "Test"},
        "work": [],
        "education": [],
        "skills": [],
    }

    jsonresume_yaml_to_json.validate_resume_schema(data)


def test_build_json_from_repo_yaml(tmp_path):
    output = tmp_path / "resume.json"

    args = [
        "--input",
        "resume.jsonresume.yaml",
        "--output",
        str(output),
    ]

    original = sys.argv
    sys.argv = ["jsonresume_yaml_to_json.py"] + args
    try:
        jsonresume_yaml_to_json.main()
    finally:
        sys.argv = original

    content = json.loads(output.read_text(encoding="utf-8"))
    assert "basics" in content
    assert isinstance(content["work"], list)
