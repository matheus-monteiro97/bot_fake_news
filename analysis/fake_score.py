def calculate_fake_score(
        heuristic_score,
        hf_score,
        fact_check_found,
        corroborated_count):

    score = 0

    # heurísticas têm peso maior
    score += heuristic_score * 5

    # confiança da IA
    score += hf_score * 30

    # agências de checagem encontraram desinformação
    if fact_check_found:
        score += 40

    # fontes reais diminuem a suspeita, mas não anulam
    if corroborated_count >= 2:
        score -= 10

    score = max(0, min(100, score))

    return round(score)

def classify_score(score):

    if score >= 85:
        return "MUITO PROVÁVEL SER FALSO"

    elif score >= 60:
        return "PARCIALMENTE FALSO"

    elif score >= 35:
        return "SUSPEITO"

    else:
        return "BAIXO RISCO"