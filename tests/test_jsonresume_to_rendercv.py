from scripts import jsonresume_to_rendercv


def test_build_rendercv_document_maps_basics_and_sections():
    source = {
        "basics": {
            "name": "Ada Lovelace",
            "label": "Engineer",
            "email": "ada@example.com",
            "profiles": [
                {
                    "network": "GitHub",
                    "username": "ada",
                    "url": "https://github.com/ada",
                }
            ],
            "summary": "Builds analytical engines.",
        },
        "work": [
            {
                "name": "Analytical Engines Ltd",
                "position": "Programmer",
                "startDate": "1843",
                "endDate": "1846",
            }
        ],
        "education": [
            {
                "institution": "University of London",
                "area": "Mathematics",
                "studyType": "Coursework",
            }
        ],
        "skills": [{"name": "Languages", "keywords": ["Mathematics", "Logic"]}],
    }

    output = jsonresume_to_rendercv.build_rendercv_document(source, "moderncv")

    assert output["cv"]["name"] == "Ada Lovelace"
    assert output["design"]["theme"] == "moderncv"
    assert "experience" in output["cv"]["sections"]
    assert "education" in output["cv"]["sections"]
    assert "skills" in output["cv"]["sections"]
