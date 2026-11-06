import re

# Equivalencias entre nombres de tecnologías y sus abreviaturas.
TECHNOLOGY_ALIASES = {
    "javascript": ["js"],
    "postgresql": ["postgres"],
    "node.js": ["nodejs", "node js"],
}


def normalize_text(text: str) -> str:
    """
    Normaliza un texto para facilitar la comparación.
    """
    return text.lower().replace("-", " ").strip()




def requirement_is_present(requirement: str, resume_text: str) -> bool:
    """
    Comprueba si un requisito aparece en el CV,
    reconociendo nombres alternativos en ambos sentidos.
    """
    normalized_requirement = normalize_text(requirement)
    normalized_resume = normalize_text(resume_text)

    possible_names = [normalized_requirement]

    # Buscar si el requisito es un nombre principal.
    for main_name, aliases in TECHNOLOGY_ALIASES.items():
        normalized_main = normalize_text(main_name)
        normalized_aliases = [
            normalize_text(alias) for alias in aliases
        ]

        if normalized_requirement == normalized_main:
            possible_names.extend(normalized_aliases)

        # También reconocer cuando el requisito es un alias.
        elif normalized_requirement in normalized_aliases:
            possible_names.append(normalized_main)
            possible_names.extend(normalized_aliases)

    for name in possible_names:
        pattern = r"(?<!\w)" + re.escape(name) + r"(?!\w)"

        if re.search(pattern, normalized_resume):
            return True

    return False



def analyze_resume(requirements: list[str], resume_text: str) -> dict:
    """
    Compara los requisitos de una oferta laboral
    con el texto extraído de un currículum.
    """

    matched_requirements = []
    missing_requirements = []

    for requirement in requirements:
        if requirement_is_present(requirement, resume_text):
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
