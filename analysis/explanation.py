def generate_explanation(text, reasons, sources, fact_check_found=False):

    if not reasons:
        return "Nenhum sinal suspeito encontrado."

    # separa motivos positivos dos negativos
    positive_keywords = [
        "corroborada",
        "múltiplas fontes"
    ]

    negative_reasons = [
        r for r in reasons
        if not any(kw in r for kw in positive_keywords)
    ]

    positive_reasons = [
        r for r in reasons
        if any(kw in r for kw in positive_keywords)
    ]

    parts = []

    if negative_reasons:
        parts.append(
            "O conteúdo apresenta alguns padrões "
            "frequentes em fake news:\n"
            + "\n".join(f"- {r}" for r in negative_reasons)
        )

    if positive_reasons:
        parts.append(
            "Sinais de credibilidade encontrados:\n"
            + "\n".join(f"- {r}" for r in positive_reasons)
        )

    if sources:
        parts.append(
            "Foram encontradas fontes confiáveis "
            "relacionadas ao tema."
        )

    return "\n\n".join(parts) if parts else "Análise concluída."