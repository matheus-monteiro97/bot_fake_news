import requests
from bs4 import BeautifulSoup


def extract_text_from_url(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # remove scripts e estilos
        for tag in soup(
            ["script", "style", "header", "footer", "nav"]
        ):
            tag.extract()

        IGNORE_WORDS = [
            "compartilhe",
            "facebook",
            "instagram",
            "whatsapp",
            "telegram",
            "newsletter",
            "assine",
            "seguir",
            "pix",
            "doe",
            "publicidade"
        ]

        paragraphs = []

        for p in soup.find_all("p"):

            text = p.get_text(
                separator=" ",
                strip=True
            )

            text_lower = text.lower()

            # ignora parágrafos muito pequenos
            if len(text) < 40:
                continue

            # ignora textos de menu e compartilhamento
            if any(
                word in text_lower
                for word in IGNORE_WORDS
            ):
                continue

            paragraphs.append(text)

        final_text = "\n".join(paragraphs)

        return final_text[:5000]

    except Exception as e:

        print(
            "Erro ao acessar URL:",
            e
        )

        return ""