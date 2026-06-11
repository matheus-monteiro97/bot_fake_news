from analysis.source_search import search_sources


FACT_CHECK_DOMAINS = [
    "aosfatos",
    "lupa",
    "comprova",
    "boatos.org"
]

FALSE_KEYWORDS = [
    "é falso",
    "fake",
    "boato",
    "enganoso",
    "desinformação",
    "não é verdade",
    "checamos",
    "golpe",
    "fraude"
]

SCAM_KEYWORDS = [
    "pix",
    "indenização",
    "r$",
    "receber agora",
    "24h",
    "confirmação dos dados",
    "saque",
    "prêmio",
    "ganhou",
    "clique aqui"
]


def fact_check(text):

    sources = search_sources(text)

    fact_check_found = False

    fact_check_sources = []

    corroborated_sources = []

    suspicious_score = 0

    text_lower = text.lower()

    # Detecta sinais típicos de golpe
    for keyword in SCAM_KEYWORDS:

        if keyword in text_lower:
            suspicious_score += 15

    for source in sources:

        titulo = source["titulo"].lower()
        url = source["url"].lower()

        is_fact_check = any(
            domain in url
            for domain in FACT_CHECK_DOMAINS
        )

        has_false_keyword = any(
            keyword in titulo
            for keyword in FALSE_KEYWORDS
        )

        if is_fact_check and has_false_keyword:

            fact_check_found = True

            suspicious_score += 50

            fact_check_sources.append(
                source
            )

        else:

            corroborated_sources.append(
                source
            )

    # Limita a pontuação
    suspicious_score = min(
        suspicious_score,
        100
    )

    return (
        fact_check_found,
        suspicious_score,
        fact_check_sources,
        corroborated_sources
    )