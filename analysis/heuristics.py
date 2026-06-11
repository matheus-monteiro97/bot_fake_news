import re
from urllib.parse import urlparse

def analyze_links(text):

    reasons = []
    score = 0

    urls = re.findall(
        r"https?://[^\s]+",
        text.lower()
    )

    suspicious_words = [

        "seguranca",
        "verificacao",
        "atualizacao",
        "login",
        "pix",
        "banco",
        "caixa",
        "cpf"

    ]

    for url in urls:

        domain = urlparse(url).netloc

        for word in suspicious_words:

            if word in domain:

                reasons.append(

                    f"Domínio suspeito ({domain})"

                )

                score += 8

                break

    return score, reasons

def analyze_heuristics(text):

    reasons = []
    score = 0

    text_upper = text.upper()
    text_lower = text.lower()

    # palavras alarmistas
    alarm_words = [
        "URGENTE",
        "ATENÇÃO",
        "COMPARTILHE",
        "REPASSE",
        "IMPERDÍVEL",
        "ÚLTIMA CHANCE",
        "NÃO DEIXE DE VER"
    ]

    for word in alarm_words:

        if word in text_upper:

            reasons.append(
                f"Linguagem alarmista ({word})"
            )

            score += 1

    # caixa alta excessiva
    upper_count = sum(c.isupper() for c in text)

    if len(text) > 0:

        ratio = upper_count / len(text)

        if ratio > 0.30:

            reasons.append(
                "Uso excessivo de letras maiúsculas"
            )

            score += 1

    # pedido de compartilhamento
    pattern = (
        r"compartilhe|repasse|envie para todos|"
        r"mande para seus contatos"
    )

    if re.search(pattern, text_lower):

        reasons.append(
            "Pedido de compartilhamento em massa"
        )

        score += 1

    # excesso de exclamações
    if text.count("!") >= 3:

        reasons.append(
            "Excesso de pontuação emocional"
        )

        score += 1

    # --------------------
    # Golpes financeiros
    # --------------------

    scam_words = [
        "pix",
        "indenização",
        "r$",
        "prêmio",
        "ganhou",
        "saque",
        "receba",
        "receber",
        "dinheiro",
        "gratuito",
        "grátis"
    ]

    for word in scam_words:

        if word in text_lower:

            reasons.append(
                f"Possível golpe financeiro ({word.upper()})"
            )

            score += 2

    # combinação muito suspeita
    if "pix" in text_lower and "indenização" in text_lower:

        reasons.append(
            "Promessa de indenização com pagamento via PIX"
        )

        score += 4

    if "receber" in text_lower and (
        "agora" in text_lower or
        "24h" in text_lower
    ):

        reasons.append(
            "Tentativa de induzir ação imediata"
        )

        score += 3

    bank_words = [
        "conta será bloqueada",
        "bloqueada",
        "acesso incomum",
        "clique aqui",
        "atualize seus dados",
        "confirme seus dados",
        "24 horas",
        "senha",
        "cpf",
        "banco",
        "caixa",
        "pix",
        "conta suspensa",
        "bloqueio definitivo",
        "atividade suspeita",
        "confirme seus dados",
        "regularize",
        "cancelamento da conta",
        "central de segurança",
        "clique no link",
        "clique aqui"
    ]

    if (
        "15 minutos" in text_lower
        or "24 horas" in text_lower
        or "imediatamente" in text_lower
        or "prazo" in text_lower
    ):

        reasons.append(
            "Tentativa de gerar senso de urgência"
        )

        score += 5


    for word in bank_words:

        if word in text_lower:

            reasons.append(
                f"Possível golpe bancário ({word.upper()})"
            )

            score += 3
    
    link_score, link_reasons = analyze_links(text)

    score += link_score

    reasons.extend(link_reasons)
    return score, reasons

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