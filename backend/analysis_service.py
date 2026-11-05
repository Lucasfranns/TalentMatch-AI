def analyze_resume(requirements: list[str], resume_text: str) -> dict:
    """
    Compara los requisitos de una oferta laboral
    con el texto extraído de un currículum.
    """

    normalized_text = resume_text.lower()

    matched_requirements = []
    missing_requirements = []

    for requirement in requirements:
        if requirement.lower() in normalized_text:
            matched_requirements.append(requirement)
        else:
            missing_requirements.append(requirement)

    total_requirements = len(requirements)
    matched_count = len(matched_requirements)

    match_percentage = round(
        (matched_count / total_requirements) * 100
    )

    summary = (
        f"El CV cumple con {matched_count} de "
        f"{total_requirements} requisitos de la oferta."
    )

    return {
        "match_percentage": match_percentage,
        "matched_requirements": matched_requirements,
        "missing_requirements": missing_requirements,
        "summary": summary,
    }