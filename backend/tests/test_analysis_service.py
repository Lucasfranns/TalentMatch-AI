from backend.analysis_service import analyze_resume


def test_analyze_resume_with_all_requirements():
    requirements = ["Python", "SQL", "FastAPI"]
    resume_text = "Tengo experiencia con Python, SQL y FastAPI."

    result = analyze_resume(requirements, resume_text)

    assert result["match_percentage"] == 100
    assert result["matched_requirements"] == requirements
    assert result["missing_requirements"] == []


def test_analyze_resume_with_some_missing_requirements():
    requirements = ["Python", "SQL", "FastAPI", "Docker"]
    resume_text = "Tengo experiencia con Python, SQL y FastAPI."

    result = analyze_resume(requirements, resume_text)

    assert result["match_percentage"] == 75
    assert result["matched_requirements"] == ["Python", "SQL", "FastAPI"]
    assert result["missing_requirements"] == ["Docker"]


def test_analyze_resume_with_no_matching_requirements():
    requirements = ["Python", "SQL"]
    resume_text = "Tengo experiencia desarrollando aplicaciones web."

    result = analyze_resume(requirements, resume_text)

    assert result["match_percentage"] == 0
    assert result["matched_requirements"] == []
    assert result["missing_requirements"] == ["Python", "SQL"]