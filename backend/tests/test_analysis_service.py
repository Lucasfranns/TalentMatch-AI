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


def test_analyze_resume_with_technology_aliases():
    requirements = [
        "JavaScript",
        "PostgreSQL",
        "Node.js",
    ]

    resume_text = """
    Experiencia desarrollando aplicaciones con JS,
    Postgres y NodeJS.
    """

    result = analyze_resume(requirements, resume_text)

    assert result["match_percentage"] == 100
    assert result["matched_requirements"] == requirements
    assert result["missing_requirements"] == []



def test_analyze_resume_does_not_match_partial_technology_names():
    requirements = ["Java", "SQL"]

    resume_text = """
    Tengo experiencia con JavaScript y NoSQL.
    """

    result = analyze_resume(requirements, resume_text)

    assert result["match_percentage"] == 0
    assert result["matched_requirements"] == []
    assert result["missing_requirements"] == requirements



def test_analyze_resume_with_aliases_in_requirements():
    requirements = [
        "JS",
        "Postgres",
        "NodeJS",
    ]

    resume_text = """
    Experiencia desarrollando aplicaciones con
    JavaScript, PostgreSQL y Node.js.
    """

    result = analyze_resume(requirements, resume_text)

    assert result["match_percentage"] == 100
    assert result["matched_requirements"] == requirements
    assert result["missing_requirements"] == []
